import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { Building, BuildingType, Gladiator, GuildResources, RunResult } from '../types'
import { INITIAL_RESOURCES } from '../types'
import { generateRecruitPool, getFameRewardForRarity } from '../generators/gladiatorGenerator'
import buildingsData from '../../data/buildings.json'

const DEFAULT_POOL_SIZE = 3

function createInitialBuildings(): Record<BuildingType, Building> {
  const lodgingData = buildingsData.lodging
  return {
    lodging: {
      id: 'lodging',
      name: lodgingData.name,
      description: lodgingData.description,
      currentLevel: 1,
      levels: lodgingData.levels,
    },
    // Ferreiro e Campo de Treinamento chegam em passos futuros.
    blacksmith: { id: 'blacksmith', name: '', description: '', currentLevel: 0, levels: [] },
    trainingGrounds: { id: 'trainingGrounds', name: '', description: '', currentLevel: 0, levels: [] },
  }
}

/**
 * Store central da Guilda (fase de Base/City Builder).
 *
 * Mantém apenas estado persistente entre runs: recursos, roster de
 * gladiadores, o pool de candidatos ao recrutamento e as construções.
 * O estado de uma run/combate em andamento NÃO vive aqui — é efêmero,
 * calculado e mantido como estado local da ArenaView (core/engine
 * roda a simulação; só o resultado final chega aqui via
 * `applyRunResults`, que persiste permadeath e recompensas).
 *
 * Fatiado por domínio para manter o store legível conforme o jogo cresce;
 * cada fatia expõe suas próprias actions.
 */

interface GuildState {
  resources: GuildResources
  roster: Gladiator[]
  /** Candidatos disponíveis para recrutamento no momento (ainda não pertencem à guilda) */
  recruitmentPool: Gladiator[]
  buildings: Record<BuildingType, Building>

  addResources: (delta: Partial<GuildResources>) => void
  spendResources: (cost: Partial<GuildResources>) => boolean
  markGladiatorDead: (gladiatorId: string) => void

  /** Gera um novo pool de candidatos com base no nível atual do Alojamento */
  refreshRecruitmentPool: () => void
  /** Move um candidato do pool para o roster, cobrando seu recruitCost em ouro */
  recruitFromPool: (candidateId: string) => boolean
  /** Compra o próximo nível de uma construção, se houver ouro/materiais suficientes */
  upgradeBuilding: (buildingId: BuildingType) => boolean
  /**
   * Aplica o resultado de uma run já simulada: remove definitivamente
   * quem morreu (permadeath), cura os sobreviventes que participaram
   * (recuperam ao voltar pra guilda) e credita ouro/materiais ganhos —
   * mesmo numa run perdida, o que já foi conquistado fica.
   */
  applyRunResults: (result: RunResult) => void
}

export const useGuildStore = create<GuildState>()(
  persist(
    (set, get) => ({
      resources: INITIAL_RESOURCES,
      roster: [],
      recruitmentPool: [],
      buildings: createInitialBuildings(),

      addResources: (delta) =>
        set((state) => ({
          resources: {
            gold: state.resources.gold + (delta.gold ?? 0),
            fame: state.resources.fame + (delta.fame ?? 0),
            materials: state.resources.materials + (delta.materials ?? 0),
          },
        })),

      spendResources: (cost) => {
        const { resources } = get()
        const canAfford =
          resources.gold >= (cost.gold ?? 0) &&
          resources.fame >= (cost.fame ?? 0) &&
          resources.materials >= (cost.materials ?? 0)

        if (!canAfford) return false

        set((state) => ({
          resources: {
            gold: state.resources.gold - (cost.gold ?? 0),
            fame: state.resources.fame - (cost.fame ?? 0),
            materials: state.resources.materials - (cost.materials ?? 0),
          },
        }))
        return true
      },

      markGladiatorDead: (gladiatorId) =>
        set((state) => ({
          roster: state.roster.map((g) =>
            g.id === gladiatorId ? { ...g, isDead: true } : g,
          ),
        })),

      refreshRecruitmentPool: () => {
        const lodging = get().buildings.lodging
        const currentLevelData = lodging.levels.find((l) => l.level === lodging.currentLevel)
        const poolSize = currentLevelData?.poolSize ?? DEFAULT_POOL_SIZE
        const rarityWeights = currentLevelData?.rarityWeights ?? {
          common: 60,
          uncommon: 25,
          rare: 12,
          legendary: 3,
        }

        set({ recruitmentPool: generateRecruitPool(poolSize, rarityWeights) })
      },

      recruitFromPool: (candidateId) => {
        const { recruitmentPool, spendResources } = get()
        const candidate = recruitmentPool.find((g) => g.id === candidateId)
        if (!candidate) return false

        const paid = spendResources({ gold: candidate.recruitCost })
        if (!paid) return false

        const recruited: Gladiator = { ...candidate, recruitedAt: Date.now() }

        set((state) => ({
          roster: [...state.roster, recruited],
          recruitmentPool: state.recruitmentPool.filter((g) => g.id !== candidateId),
        }))

        const fameReward = getFameRewardForRarity(candidate.rarity)
        if (fameReward > 0) get().addResources({ fame: fameReward })

        return true
      },

      upgradeBuilding: (buildingId) => {
        const building = get().buildings[buildingId]
        const nextLevelData = building.levels.find((l) => l.level === building.currentLevel + 1)
        if (!nextLevelData) return false

        const paid = get().spendResources(nextLevelData.cost)
        if (!paid) return false

        set((state) => ({
          buildings: {
            ...state.buildings,
            [buildingId]: { ...building, currentLevel: nextLevelData.level },
          },
        }))

        // O Alojamento reflete o novo nível imediatamente numa nova leva de candidatos.
        if (buildingId === 'lodging') get().refreshRecruitmentPool()

        return true
      },

      applyRunResults: (result) => {
        const deadIds = new Set(result.finalParty.filter((g) => g.isDead).map((g) => g.id))
        const participantIds = new Set(result.finalParty.map((g) => g.id))

        set((state) => ({
          roster: state.roster
            .filter((g) => !deadIds.has(g.id))
            .map((g) =>
              participantIds.has(g.id) ? { ...g, stats: { ...g.stats, hp: g.stats.maxHp } } : g,
            ),
        }))

        get().addResources({ gold: result.goldEarned, materials: result.materialsEarned })
      },
    }),
    { name: 'gladiator-guild-save' },
  ),
)
