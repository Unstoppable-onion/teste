import type { CombatEvent, Enemy, Gladiator } from '../../core/types'

export interface WaveVisualState {
  party: Gladiator[]
  enemies: Enemy[]
}

/**
 * Reconstrói o HP de cada combatente depois de N eventos de uma wave —
 * usado só para animar a tela de combate, que revela o log aos poucos.
 * O resultado da wave já foi calculado de uma vez pelo core/engine (motor
 * autoritativo); isto aqui só espelha a mesma regra de dano (evento
 * 'attack' aplica `amount` ao alvo) para saber o que desenhar a cada
 * passo da animação — não decide nada sobre o jogo.
 */
export function replayWaveState(
  initialParty: Gladiator[],
  initialEnemies: Enemy[],
  revealedEvents: CombatEvent[],
): WaveVisualState {
  const party = initialParty.map((g) => ({ ...g, stats: { ...g.stats } }))
  const enemies = initialEnemies.map((e) => ({ ...e, stats: { ...e.stats } }))

  function findUnit(id: string) {
    return party.find((g) => g.id === id) ?? enemies.find((e) => e.id === id)
  }

  for (const event of revealedEvents) {
    if (event.type !== 'attack' || !event.targetId || event.amount == null) continue

    const target = findUnit(event.targetId)
    if (!target) continue

    target.stats.hp = Math.max(0, target.stats.hp - event.amount)
    if (target.stats.hp <= 0 && 'isDead' in target) target.isDead = true
  }

  return { party, enemies }
}
