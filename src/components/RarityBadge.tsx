import type { GladiatorRarity } from '../core/types'

const RARITY_STYLES: Record<GladiatorRarity, string> = {
  common: 'bg-stone-700 text-stone-200',
  uncommon: 'bg-emerald-800 text-emerald-200',
  rare: 'bg-sky-800 text-sky-200',
  legendary: 'bg-amber-600 text-amber-50',
}

const RARITY_LABELS: Record<GladiatorRarity, string> = {
  common: 'Comum',
  uncommon: 'Incomum',
  rare: 'Raro',
  legendary: 'Lendário',
}

export function RarityBadge({ rarity }: { rarity: GladiatorRarity }) {
  return (
    <span
      className={`rounded px-2 py-0.5 text-xs font-semibold ${RARITY_STYLES[rarity]}`}
    >
      {RARITY_LABELS[rarity]}
    </span>
  )
}
