import type { CombatEvent, Enemy, Gladiator } from '../../core/types'
import { GladiatorSprite } from '../../components/sprites/GladiatorSprite'
import { EnemySprite } from '../../components/sprites/EnemySprite'
import { CombatantSlot, type CombatantAnimState } from './CombatantSlot'
import { replayWaveState } from './replayWaveState'

/**
 * Palco visual do combate: reconstrói o HP de cada lado a partir dos
 * eventos já revelados (replayWaveState) e decide, a partir do último
 * evento, quem deve tocar a animação de ataque/dano agora.
 */
export function CombatStage({
  initialParty,
  initialEnemies,
  revealedEvents,
}: {
  initialParty: Gladiator[]
  initialEnemies: Enemy[]
  revealedEvents: CombatEvent[]
}) {
  const { party, enemies } = replayWaveState(initialParty, initialEnemies, revealedEvents)
  const lastEvent = revealedEvents[revealedEvents.length - 1]
  const waveConcluded = lastEvent?.type === 'victory' || lastEvent?.type === 'defeat'
  const waveWon = lastEvent?.type === 'victory'

  function animStateFor(id: string, isDead: boolean, side: 'party' | 'enemy'): CombatantAnimState {
    if (isDead) return 'idle'
    if (lastEvent?.type === 'attack') {
      if (lastEvent.sourceId === id) return 'attacking'
      if (lastEvent.targetId === id) return 'hit'
    }
    if (waveConcluded && waveWon && side === 'party') return 'victory'
    return 'idle'
  }

  return (
    <div className="flex items-center justify-between gap-4 rounded-lg border border-stone-800 bg-stone-950/60 px-4 py-6 sm:px-8">
      <div className="flex flex-1 flex-wrap justify-center gap-4">
        {party.map((g) => (
          <CombatantSlot
            key={g.id}
            name={g.name}
            hp={g.stats.hp}
            maxHp={g.stats.maxHp}
            isDead={g.isDead}
            animState={animStateFor(g.id, g.isDead, 'party')}
            animKey={revealedEvents.length}
            side="party"
          >
            <GladiatorSprite rarity={g.rarity} facing="right" />
          </CombatantSlot>
        ))}
      </div>

      <p className="shrink-0 text-lg font-bold text-stone-700">VS</p>

      <div className="flex flex-1 flex-wrap justify-center gap-4">
        {enemies.map((e) => (
          <CombatantSlot
            key={e.id}
            name={e.name}
            hp={e.stats.hp}
            maxHp={e.stats.maxHp}
            isDead={e.stats.hp <= 0}
            animState={animStateFor(e.id, e.stats.hp <= 0, 'enemy')}
            animKey={revealedEvents.length}
            side="enemy"
          >
            <EnemySprite name={e.name} facing="left" />
          </CombatantSlot>
        ))}
      </div>
    </div>
  )
}
