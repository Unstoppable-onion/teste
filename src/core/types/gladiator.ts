/**
 * Domínio: Gladiador
 *
 * Representa um gladiador recrutável ou já recrutado pela guilda.
 * Gerado proceduralmente (ver core/generators/gladiatorGenerator.ts)
 * a partir dos templates em data/gladiatorTemplates.json.
 */

export type GladiatorRarity = 'common' | 'uncommon' | 'rare' | 'legendary'

export interface GladiatorStats {
  hp: number
  maxHp: number
  attack: number
  defense: number
  speed: number
}

export interface Gladiator {
  id: string
  name: string
  rarity: GladiatorRarity
  stats: GladiatorStats
  /** true assim que morre em combate — permadeath, nunca é revivido */
  isDead: boolean
  recruitedAt: number | null
  /** Custo em ouro para recrutar este gladiador (relevante só enquanto é um candidato) */
  recruitCost: number
}
