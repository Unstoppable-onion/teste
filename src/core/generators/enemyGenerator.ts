import type { Enemy } from '../types'
import enemyData from '../../data/enemies.json'
import { generateId } from './id'

/**
 * Geração procedural de inimigos por wave, a partir de
 * data/enemies.json. Cada wave define quantos inimigos aparecem, de
 * quais tiers (dificuldade) e a recompensa em ouro/materiais por
 * limpá-la — puramente dado, sem nada hardcoded aqui.
 */

type StatRange = [number, number]

interface EnemyTemplate {
  name: string
  tier: number
  hp: StatRange
  attack: StatRange
  defense: StatRange
  speed: StatRange
}

interface WaveConfig {
  enemyCount: number
  tiers: number[]
  goldReward: number
  materialsReward: number
}

const waves = enemyData.waves as WaveConfig[]
const enemyPool = enemyData.enemyPool as EnemyTemplate[]

function randomInt([min, max]: StatRange): number {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

function pickRandom<T>(pool: T[]): T {
  return pool[Math.floor(Math.random() * pool.length)]
}

function instantiateEnemy(template: EnemyTemplate): Enemy {
  const hp = randomInt(template.hp)
  return {
    id: generateId('enemy'),
    name: template.name,
    stats: {
      hp,
      maxHp: hp,
      attack: randomInt(template.attack),
      defense: randomInt(template.defense),
      speed: randomInt(template.speed),
    },
  }
}

const ROMAN_NUMERALS = ['I', 'II', 'III', 'IV', 'V', 'VI']

/**
 * Quando o sorteio traz o mesmo tipo de inimigo mais de uma vez na wave
 * (ex: dois "Urso de Combate"), o log de combate ficaria ambíguo — pareceria
 * que um inimigo já morto voltou a atacar. Aqui desambiguamos o nome
 * exibido ("Urso de Combate I" / "Urso de Combate II"); os ids continuam
 * únicos independentemente disso.
 */
function disambiguateNames(enemies: Enemy[]): Enemy[] {
  const totalByName = new Map<string, number>()
  for (const e of enemies) totalByName.set(e.name, (totalByName.get(e.name) ?? 0) + 1)

  const seenByName = new Map<string, number>()
  return enemies.map((e) => {
    if ((totalByName.get(e.name) ?? 1) <= 1) return e

    const occurrence = (seenByName.get(e.name) ?? 0) + 1
    seenByName.set(e.name, occurrence)
    return { ...e, name: `${e.name} ${ROMAN_NUMERALS[occurrence - 1] ?? occurrence}` }
  })
}

export function generateWave(waveIndex: number): Enemy[] {
  const wave = waves[waveIndex]
  const pool = enemyPool.filter((e) => wave.tiers.includes(e.tier))
  const enemies = Array.from({ length: wave.enemyCount }, () => instantiateEnemy(pickRandom(pool)))
  return disambiguateNames(enemies)
}

/** Gera todas as waves de uma nova run, na ordem em que serão enfrentadas. */
export function generateRunWaves(): Enemy[][] {
  return waves.map((_, index) => generateWave(index))
}

export function getWaveRewards(): { gold: number[]; materials: number[] } {
  return {
    gold: waves.map((w) => w.goldReward),
    materials: waves.map((w) => w.materialsReward),
  }
}
