import type { Gladiator, GladiatorRarity } from '../types'
import templates from '../../data/gladiatorTemplates.json'

/**
 * Geração procedural de gladiadores recrutáveis.
 *
 * Raridade é sorteada por peso (rarityWeights); a raridade sorteada define
 * as faixas de status, o custo de recrutamento e a chance de ganhar um
 * epíteto no nome — tudo vindo de data/gladiatorTemplates.json, sem nada
 * hardcoded aqui. Isso deixa o balanceamento ajustável sem tocar em código.
 */

type StatRange = [number, number]

interface RarityStatRanges {
  hp: StatRange
  attack: StatRange
  defense: StatRange
  speed: StatRange
  recruitCost: StatRange
  fameOnRecruit: number
}

const RARITIES: GladiatorRarity[] = ['common', 'uncommon', 'rare', 'legendary']

function randomInt([min, max]: StatRange): number {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

function pickRandom<T>(pool: T[]): T {
  return pool[Math.floor(Math.random() * pool.length)]
}

function rollRarity(): GladiatorRarity {
  const weights = templates.rarityWeights as Record<GladiatorRarity, number>
  const totalWeight = RARITIES.reduce((sum, r) => sum + weights[r], 0)
  let roll = Math.random() * totalWeight

  for (const rarity of RARITIES) {
    roll -= weights[rarity]
    if (roll <= 0) return rarity
  }
  return 'common'
}

function rollName(rarity: GladiatorRarity): string {
  const firstName = pickRandom(templates.firstNames)
  const titleChance = (templates.titleChance as Record<GladiatorRarity, number>)[rarity]

  if (Math.random() < titleChance) {
    return `${firstName} ${pickRandom(templates.titles)}`
  }
  return firstName
}

function generateId(): string {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID()
  }
  return `glad-${Date.now()}-${Math.floor(Math.random() * 1e9)}`
}

export function generateRandomGladiator(): Gladiator {
  const rarity = rollRarity()
  const ranges = (templates.statRanges as Record<GladiatorRarity, RarityStatRanges>)[rarity]
  const hp = randomInt(ranges.hp)

  return {
    id: generateId(),
    name: rollName(rarity),
    rarity,
    stats: {
      hp,
      maxHp: hp,
      attack: randomInt(ranges.attack),
      defense: randomInt(ranges.defense),
      speed: randomInt(ranges.speed),
    },
    isDead: false,
    recruitedAt: null,
    recruitCost: randomInt(ranges.recruitCost),
  }
}

export function getFameRewardForRarity(rarity: GladiatorRarity): number {
  return (templates.statRanges as Record<GladiatorRarity, RarityStatRanges>)[rarity].fameOnRecruit
}

export function generateRecruitPool(size: number): Gladiator[] {
  return Array.from({ length: size }, () => generateRandomGladiator())
}
