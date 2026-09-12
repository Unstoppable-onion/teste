import type { Gladiator } from '../types'

/**
 * Geração procedural de gladiadores recrutáveis.
 *
 * Implementado no Passo 2. A ideia: sortear nome, raridade e status
 * (HP, Ataque, Defesa, Velocidade) a partir de faixas definidas em
 * data/gladiatorTemplates.json, com a raridade influenciando as faixas
 * e o nível das construções (ex: Alojamento) influenciando o pool.
 */
export function generateRandomGladiator(): Gladiator {
  throw new Error('generateRandomGladiator: implementado no Passo 2')
}

export function generateRecruitPool(size: number): Gladiator[] {
  return Array.from({ length: size }, () => generateRandomGladiator())
}
