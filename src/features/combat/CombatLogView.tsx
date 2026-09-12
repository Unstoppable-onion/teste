import type { CombatEvent } from '../../core/types'

const EVENT_STYLES: Record<CombatEvent['type'], string> = {
  attack: 'text-stone-300',
  death: 'font-semibold text-red-400',
  victory: 'font-semibold text-emerald-400',
  defeat: 'font-semibold text-red-500',
}

/** Exibe o log de uma wave em andamento, revelado evento a evento pela ArenaView. */
export function CombatLogView({
  totalWaves,
  waveIndex,
  events,
  onSkip,
}: {
  totalWaves: number
  waveIndex: number
  events: CombatEvent[]
  onSkip: () => void
}) {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-amber-400">
          Wave {waveIndex + 1} de {totalWaves}
        </h2>
        <button
          onClick={onSkip}
          className="text-xs font-medium text-stone-400 underline-offset-2 hover:text-amber-400 hover:underline"
        >
          Pular
        </button>
      </div>

      <div className="min-h-[300px] space-y-2 rounded-lg border border-stone-800 bg-stone-900/60 p-4">
        {events.length === 0 && (
          <p className="text-sm text-stone-500">O combate está prestes a começar...</p>
        )}
        {events.map((event, index) => (
          <p key={index} className={`text-sm ${EVENT_STYLES[event.type]}`}>
            {event.message}
          </p>
        ))}
      </div>
    </div>
  )
}
