import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { Gladiator, GuildResources } from '../types'
import { INITIAL_RESOURCES } from '../types'

/**
 * Store central da Guilda (fase de Base/City Builder).
 *
 * Mantém apenas estado persistente entre runs: recursos, roster de
 * gladiadores e construções. O estado de um combate em andamento NÃO
 * vive aqui — ver core/store/useCombatStore.ts (Passo 4), que é efêmero
 * e descartado ao fim da run.
 *
 * Fatiado por domínio para manter o store legível conforme o jogo cresce;
 * cada fatia expõe suas próprias actions.
 */

interface GuildState {
  resources: GuildResources
  roster: Gladiator[]

  addResources: (delta: Partial<GuildResources>) => void
  spendResources: (cost: Partial<GuildResources>) => boolean
  recruitGladiator: (gladiator: Gladiator) => void
  markGladiatorDead: (gladiatorId: string) => void
}

export const useGuildStore = create<GuildState>()(
  persist(
    (set, get) => ({
      resources: INITIAL_RESOURCES,
      roster: [],

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

      recruitGladiator: (gladiator) =>
        set((state) => ({ roster: [...state.roster, gladiator] })),

      markGladiatorDead: (gladiatorId) =>
        set((state) => ({
          roster: state.roster.map((g) =>
            g.id === gladiatorId ? { ...g, isDead: true } : g,
          ),
        })),
    }),
    { name: 'gladiator-guild-save' },
  ),
)
