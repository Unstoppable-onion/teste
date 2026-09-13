import type { GladiatorRarity } from '../../core/types'

/**
 * "Boneco" 2D de um gladiador: silhueta estilizada em SVG (não pixel art
 * nem sprite raster) — barata de renderizar, escala sem perder nitidez, e
 * fácil de recolorir por dado (raridade) sem precisar de novos assets.
 * A cor de destaque (crista do capacete, borda da armadura, cinto) muda
 * por raridade; a pose é fixa — quem anima é o wrapper (ver sprites.css),
 * não o SVG em si.
 */

const RARITY_ACCENT: Record<GladiatorRarity, string> = {
  common: '#a8a29e',
  uncommon: '#34d399',
  rare: '#38bdf8',
  legendary: '#fbbf24',
}

export function GladiatorSprite({
  rarity,
  facing = 'right',
}: {
  rarity: GladiatorRarity
  facing?: 'left' | 'right'
}) {
  const accent = RARITY_ACCENT[rarity]

  return (
    <svg
      viewBox="0 0 100 140"
      width="72"
      height="100"
      style={{ transform: facing === 'left' ? 'scaleX(-1)' : undefined }}
      aria-hidden
    >
      {/* pernas */}
      <rect x="38" y="100" width="10" height="30" rx="3" fill="#78716c" />
      <rect x="52" y="100" width="10" height="30" rx="3" fill="#78716c" />
      {/* braço com escudo */}
      <rect x="16" y="54" width="16" height="36" rx="4" fill="#57534e" stroke={accent} strokeWidth="2" />
      {/* tronco */}
      <rect x="34" y="48" width="32" height="56" rx="8" fill="#44403c" stroke={accent} strokeWidth="3" />
      {/* cinto */}
      <rect x="34" y="86" width="32" height="6" fill={accent} />
      {/* braço com espada + lâmina */}
      <rect x="66" y="52" width="10" height="30" rx="4" fill="#57534e" />
      <rect x="70" y="26" width="7" height="42" rx="2" fill="#d6d3d1" transform="rotate(35 73.5 47)" />
      {/* cabeça */}
      <circle cx="50" cy="32" r="16" fill="#e7c9a0" />
      {/* capacete */}
      <path d="M32 30 a18 18 0 0 1 36 0 v-6 a18 18 0 0 0 -36 0 z" fill="#57534e" stroke={accent} strokeWidth="2" />
      {/* crista */}
      <rect x="46" y="12" width="8" height="16" fill={accent} />
    </svg>
  )
}
