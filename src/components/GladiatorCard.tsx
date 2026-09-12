import type { Gladiator } from '../core/types'
import { RarityBadge } from './RarityBadge'

interface GladiatorCardAction {
  label: string
  onClick: () => void
  disabled?: boolean
}

/**
 * Card de exibição de um gladiador — usado tanto para candidatos no
 * pool de recrutamento (com uma action de "Recrutar") quanto para
 * membros já recrutados do roster (sem action, ou com actions futuras
 * como "Enviar para a Arena").
 */
export function GladiatorCard({
  gladiator,
  action,
}: {
  gladiator: Gladiator
  action?: GladiatorCardAction
}) {
  return (
    <div className="flex flex-col gap-3 rounded-lg border border-stone-800 bg-stone-900/60 p-4">
      <div className="flex items-start justify-between gap-2">
        <h3 className="font-semibold text-stone-100">{gladiator.name}</h3>
        <RarityBadge rarity={gladiator.rarity} />
      </div>

      <dl className="grid grid-cols-4 gap-2 text-center text-xs">
        <Stat label="HP" value={gladiator.stats.maxHp} />
        <Stat label="ATQ" value={gladiator.stats.attack} />
        <Stat label="DEF" value={gladiator.stats.defense} />
        <Stat label="VEL" value={gladiator.stats.speed} />
      </dl>

      {action && (
        <button
          onClick={action.onClick}
          disabled={action.disabled}
          className="mt-1 w-full rounded-md bg-amber-500 px-3 py-2 text-sm font-medium text-stone-950 transition-colors hover:bg-amber-400 disabled:cursor-not-allowed disabled:bg-stone-700 disabled:text-stone-400"
        >
          {action.label}
        </button>
      )}
    </div>
  )
}

function Stat({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded bg-stone-800/60 py-1.5">
      <dt className="text-stone-500">{label}</dt>
      <dd className="font-semibold text-stone-100">{value}</dd>
    </div>
  )
}
