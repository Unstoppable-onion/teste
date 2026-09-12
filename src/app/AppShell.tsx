import { useState } from 'react'
import { GuildView } from '../features/city-builder/GuildView'
import { ArenaView } from '../features/combat/ArenaView'

type Tab = 'guild' | 'arena'

/**
 * Shell de navegação de topo. Alterna entre as duas fases do jogo:
 * Base (GuildView) e Batalha (ArenaView). Cada fase é um módulo
 * independente em src/features/, sem conhecimento uma da outra —
 * a única ponte entre elas é o estado compartilhado em core/store.
 */
export function AppShell() {
  const [tab, setTab] = useState<Tab>('guild')

  return (
    <div className="min-h-screen bg-stone-950">
      <header className="border-b border-stone-800 bg-stone-900/40">
        <div className="mx-auto flex max-w-4xl items-center justify-between px-4 py-4">
          <h1 className="text-xl font-bold tracking-tight text-amber-400">
            Gladiator Guild
          </h1>
          <nav className="flex gap-2">
            <TabButton active={tab === 'guild'} onClick={() => setTab('guild')}>
              Guilda
            </TabButton>
            <TabButton active={tab === 'arena'} onClick={() => setTab('arena')}>
              Arena
            </TabButton>
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-4 py-8">
        {tab === 'guild' ? <GuildView /> : <ArenaView />}
      </main>
    </div>
  )
}

function TabButton({
  active,
  onClick,
  children,
}: {
  active: boolean
  onClick: () => void
  children: React.ReactNode
}) {
  return (
    <button
      onClick={onClick}
      className={`rounded-md px-4 py-2 text-sm font-medium transition-colors ${
        active
          ? 'bg-amber-500 text-stone-950'
          : 'text-stone-300 hover:bg-stone-800'
      }`}
    >
      {children}
    </button>
  )
}
