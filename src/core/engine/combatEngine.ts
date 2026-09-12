import type { CombatEvent, CombatState, Enemy, Gladiator } from '../types'

/**
 * Motor de Combate — lógica pura, sem React e sem dependência de renderização.
 *
 * `createCombatState` monta o encontro e sorteia a ordem de turnos (por
 * velocidade, com empates aleatórios) uma única vez; `resolveNextTurn`
 * avança um turno por vez, imutável (recebe um estado e devolve outro).
 * Isso permite tanto simular o combate inteiro de uma vez (`simulateCombat`
 * em runEngine.ts, usado para calcular o resultado da run) quanto, no
 * futuro, animá-lo turno a turno na UI sem duplicar nenhuma regra.
 */

type Combatant = Gladiator | Enemy

function isAlive(unit: Combatant): boolean {
  return unit.stats.hp > 0
}

function pickRandom<T>(pool: T[]): T {
  return pool[Math.floor(Math.random() * pool.length)]
}

function shuffle<T>(items: T[]): T[] {
  const copy = [...items]
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[copy[i], copy[j]] = [copy[j], copy[i]]
  }
  return copy
}

function cloneCombatState(state: CombatState): CombatState {
  return {
    party: state.party.map((g) => ({ ...g, stats: { ...g.stats } })),
    enemies: state.enemies.map((e) => ({ ...e, stats: { ...e.stats } })),
    turnOrder: [...state.turnOrder],
    currentTurnIndex: state.currentTurnIndex,
    log: [...state.log],
    isOver: state.isOver,
    didWin: state.didWin,
  }
}

/**
 * Monta o estado inicial de um combate (uma wave) e sorteia a iniciativa:
 * ordenado por velocidade descendente, com empates decididos por sorteio
 * (embaralha antes de ordenar, já que sort é estável).
 */
export function createCombatState(party: Gladiator[], enemies: Enemy[]): CombatState {
  const partyClone = party.map((g) => ({ ...g, stats: { ...g.stats } }))
  const enemiesClone = enemies.map((e) => ({ ...e, stats: { ...e.stats } }))

  const allCombatants: Combatant[] = shuffle([...partyClone, ...enemiesClone])
  const turnOrder = allCombatants
    .sort((a, b) => b.stats.speed - a.stats.speed)
    .map((c) => c.id)

  return {
    party: partyClone,
    enemies: enemiesClone,
    turnOrder,
    currentTurnIndex: 0,
    log: [],
    isOver: false,
    didWin: false,
  }
}

function findCombatant(state: CombatState, id: string): { unit: Combatant; side: 'party' | 'enemy' } | null {
  const partyUnit = state.party.find((g) => g.id === id)
  if (partyUnit) return { unit: partyUnit, side: 'party' }
  const enemyUnit = state.enemies.find((e) => e.id === id)
  if (enemyUnit) return { unit: enemyUnit, side: 'enemy' }
  return null
}

/**
 * Resolve um único turno: o próximo ator vivo na ordem de iniciativa
 * ataca um alvo vivo aleatório do lado oposto. Dano = ATQ - DEF, com
 * piso de 1 (nunca "erra" completamente — mantém o MVP previsível).
 * Verifica vitória/derrota ao final de cada ataque.
 */
export function resolveNextTurn(state: CombatState): CombatState {
  if (state.isOver) return state

  const next = cloneCombatState(state)
  const total = next.turnOrder.length

  let idx = next.currentTurnIndex
  let found = findCombatant(next, next.turnOrder[idx])
  let guard = 0
  while ((!found || !isAlive(found.unit)) && guard < total) {
    idx = (idx + 1) % total
    found = findCombatant(next, next.turnOrder[idx])
    guard++
  }

  if (!found || !isAlive(found.unit)) {
    // Não deveria acontecer (vitória/derrota já teria sido detectada),
    // mas evita loop infinito em qualquer estado inesperado.
    next.isOver = true
    return next
  }

  const { unit: actor, side } = found
  const opposing = side === 'party' ? next.enemies : next.party
  const livingTargets = opposing.filter(isAlive)

  if (livingTargets.length === 0) {
    next.isOver = true
    next.didWin = side === 'party'
    return next
  }

  const target = pickRandom(livingTargets)
  const damage = Math.max(1, actor.stats.attack - target.stats.defense)
  target.stats.hp = Math.max(0, target.stats.hp - damage)

  next.log.push({
    type: 'attack',
    sourceId: actor.id,
    targetId: target.id,
    amount: damage,
    message: `${actor.name} ataca ${target.name} causando ${damage} de dano.`,
  })

  if (target.stats.hp <= 0) {
    if ('isDead' in target) target.isDead = true
    next.log.push({
      type: 'death',
      sourceId: target.id,
      message: `${target.name} caiu na arena.`,
    })
  }

  const partyAlive = next.party.some(isAlive)
  const enemiesAlive = next.enemies.some(isAlive)

  if (!enemiesAlive) {
    next.isOver = true
    next.didWin = true
    next.log.push(victoryEvent())
  } else if (!partyAlive) {
    next.isOver = true
    next.didWin = false
    next.log.push(defeatEvent())
  } else {
    next.currentTurnIndex = (idx + 1) % total
  }

  return next
}

function victoryEvent(): CombatEvent {
  return { type: 'victory', sourceId: 'system', message: 'A equipe venceu o combate!' }
}

function defeatEvent(): CombatEvent {
  return { type: 'defeat', sourceId: 'system', message: 'Toda a equipe caiu na arena.' }
}

/** Roda um combate (uma wave) do início ao fim e devolve o estado final. */
export function simulateCombat(party: Gladiator[], enemies: Enemy[]): CombatState {
  let state = createCombatState(party, enemies)
  let guard = 0
  const MAX_TURNS = 500 // rede de segurança contra loops (não deveria disparar)

  while (!state.isOver && guard < MAX_TURNS) {
    state = resolveNextTurn(state)
    guard++
  }

  return state
}
