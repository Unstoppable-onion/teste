import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { Gladiator, GuildResources } from '../types'
import { INITIAL_RESOURCES } from '../types'
import { generateRecruitPool, getFameRewardForRarity } from '../generators/gladiatorGenerator'

const DEFAULT_POOL_SIZE = 3

/**
 * Store central da Guilda (fase de Base/City Builder).
 *
 * Mantém apenas estado persistente entre runs: recursos, roster de
 * gladiadores, o pool de candidatos ao recrutamento e construções.
 * O estado de um combate em andamento NÃO vive aqui — ver
 * core/store/useCombatStore.ts (Passo 4), que é efêmero e descartado ao
 * fim da run.
 *
 * Fatiado por domínio para manter o store legível conforme o jogo cresce;
 * cada fatia expõe suas próprias actions.
 */

interface GuildState {
  resources: GuildResources
  roster: Gladiator[]
  /** Candidatos disponíveis para recrutamento no momento (ainda não pertencem à guilda) */
  recruitmentPool: Gladiator[]

  addResources: (delta: Partial<GuildResources>) => void
  spendResources: (cost: Partial<GuildResources>) => boolean
  markGladiatorDead: (gladiatorId: string) => void

  /** Gera um novo pool de candidatos, descartando os anteriores não recrutados */
  refreshRecruitmentPool: (size?: number) => void
  /** Move um candidato do pool para o roster, cobrando seu recruitCost em ouro */
  recruitFromPool: (candidateId: string) => boolean
}

export const useGuildStore = create<GuildState>()(
  persist(
    (set, get) => ({
      resources: INITIAL_RESOURCES,
      roster: [],
      recruitmentPool: [],

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

      refreshRecruitmentPool: (size = DEFAULT_POOL_SIZE) =>
        set({ recruitmentPool: generateRecruitPool(size) }),

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
    }),
    { name: 'gladiator-guild-save' },
  ),
)
