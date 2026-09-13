/**
 * "Boneco" 2D de um inimigo: mesma ideia da GladiatorSprite (silhueta SVG,
 * sem assets externos), mas com duas variantes de forma pra dar alguma
 * diversidade visual entre as waves sem precisar desenhar um sprite por
 * inimigo — a variante é inferida do nome (que já vem do template em
 * data/enemies.json).
 */

type EnemyKind = 'beast' | 'brute'

function inferEnemyKind(name: string): EnemyKind {
  return /rato|urso/i.test(name) ? 'beast' : 'brute'
}

export function EnemySprite({ name, facing = 'left' }: { name: string; facing?: 'left' | 'right' }) {
  const kind = inferEnemyKind(name)
  const style = { transform: facing === 'left' ? 'scaleX(-1)' : undefined }

  if (kind === 'beast') {
    return (
      <svg viewBox="0 0 120 100" width="80" height="66" style={style} aria-hidden>
        <rect x="20" y="70" width="10" height="22" rx="3" fill="#7f1d1d" />
        <rect x="90" y="70" width="10" height="22" rx="3" fill="#7f1d1d" />
        <ellipse cx="60" cy="55" rx="42" ry="24" fill="#991b1b" stroke="#450a0a" strokeWidth="3" />
        <circle cx="100" cy="38" r="16" fill="#b91c1c" stroke="#450a0a" strokeWidth="3" />
        <path d="M92 26 l6 -12 l6 10 z" fill="#7f1d1d" />
        <path d="M108 26 l6 -10 l4 12 z" fill="#7f1d1d" />
        <circle cx="104" cy="36" r="2.5" fill="#fde047" />
      </svg>
    )
  }

  return (
    <svg viewBox="0 0 100 140" width="72" height="100" style={style} aria-hidden>
      <rect x="38" y="100" width="10" height="30" rx="3" fill="#7f1d1d" />
      <rect x="52" y="100" width="10" height="30" rx="3" fill="#7f1d1d" />
      <rect x="32" y="46" width="36" height="58" rx="10" fill="#991b1b" stroke="#450a0a" strokeWidth="3" />
      <path d="M32 60 l-14 20 l6 6 l14 -18 z" fill="#7f1d1d" />
      <path d="M68 60 l14 20 l-6 6 l-14 -18 z" fill="#7f1d1d" />
      <circle cx="50" cy="30" r="18" fill="#b91c1c" stroke="#450a0a" strokeWidth="3" />
      <path d="M38 18 l-6 -14 l8 4 z" fill="#292524" />
      <path d="M62 18 l6 -14 l-8 4 z" fill="#292524" />
      <circle cx="44" cy="30" r="2.5" fill="#fde047" />
      <circle cx="56" cy="30" r="2.5" fill="#fde047" />
    </svg>
  )
}
