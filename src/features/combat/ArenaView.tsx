/**
 * Tela principal da fase de Batalha (Roguelike / Arena).
 * Implementada no Passo 4 — seleção de equipe, combate por turnos,
 * permadeath e recompensas.
 */
export function ArenaView() {
  return (
    <div className="rounded-lg border border-stone-800 bg-stone-900/60 p-6">
      <h2 className="text-lg font-semibold text-amber-400">Arena</h2>
      <p className="mt-2 text-sm text-stone-400">
        O loop de combate chega no Passo 4.
      </p>
    </div>
  )
}
