import type { ReactNode } from 'react'

export type CombatantAnimState = 'idle' | 'attacking' | 'hit' | 'victory'

const ANIM_CLASS: Record<CombatantAnimState, string> = {
  idle: 'sprite-idle',
  attacking: 'sprite-attacking',
  hit: 'sprite-hit',
  victory: 'sprite-victory',
}

/** Um combatente na tela de batalha: sprite + nome + barra de HP, reagindo ao estado da animação atual. */
export function CombatantSlot({
  name,
  hp,
  maxHp,
  isDead,
  animState,
  animKey,
  side,
  children,
}: {
  name: string
  hp: number
  maxHp: number
  isDead: boolean
  animState: CombatantAnimState
  /** Muda a cada evento revelado — força o React a remontar e reiniciar a animação CSS. */
  animKey: number
  /** Define pra que lado o "lunge" de ataque avança (ver index.css). */
  side: 'party' | 'enemy'
  children: ReactNode
}) {
  const hpPct = Math.max(0, Math.min(100, Math.round((hp / maxHp) * 100)))
  const barColor = hpPct > 50 ? 'bg-emerald-500' : hpPct > 20 ? 'bg-amber-500' : 'bg-red-500'

  return (
    <div className="flex flex-col items-center gap-1" data-side={side}>
      <div key={animKey} className={isDead ? 'sprite-dead' : ANIM_CLASS[animState]}>
        {children}
      </div>
      <p className={`text-xs font-medium ${isDead ? 'text-stone-600 line-through' : 'text-stone-300'}`}>
        {name}
      </p>
      <div className="h-1.5 w-16 overflow-hidden rounded-full bg-stone-800">
        <div className={`h-full transition-all duration-300 ${barColor}`} style={{ width: `${hpPct}%` }} />
      </div>
    </div>
  )
}
