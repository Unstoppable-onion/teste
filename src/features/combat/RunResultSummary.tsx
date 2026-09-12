import type { RunResult } from '../../core/types'

/** Tela final de uma run: waves limpas, recompensas e o custo em permadeath. */
export function RunResultSummary({
  result,
  onReturn,
}: {
  result: RunResult
  onReturn: () => void
}) {
  const fallen = result.finalParty.filter((g) => g.isDead)
  const survivors = result.finalParty.filter((g) => !g.isDead)

  return (
    <div className="space-y-6">
      <section className="rounded-lg border border-stone-800 bg-stone-900/60 p-6 text-center">
        <h2 className={`text-2xl font-bold ${result.didClearRun ? 'text-emerald-400' : 'text-red-400'}`}>
          {result.didClearRun ? 'Run Concluída!' : 'A Run Terminou'}
        </h2>
        <p className="mt-1 text-sm text-stone-400">
          {result.clearedWaves} de {result.totalWaves} waves vencidas.
        </p>

        <div className="mt-4 flex justify-center gap-6">
          <div>
            <p className="text-xs uppercase tracking-wide text-stone-500">Ouro ganho</p>
            <p className="text-xl font-bold text-amber-400">+{result.goldEarned}</p>
          </div>
          <div>
            <p className="text-xs uppercase tracking-wide text-stone-500">Materiais ganhos</p>
            <p className="text-xl font-bold text-amber-400">+{result.materialsEarned}</p>
          </div>
        </div>
      </section>

      {fallen.length > 0 && (
        <section className="rounded-lg border border-red-900/50 bg-red-950/20 p-4">
          <h3 className="text-sm font-semibold text-red-400">Perdidos para sempre</h3>
          <ul className="mt-2 space-y-1 text-sm text-stone-400">
            {fallen.map((g) => (
              <li key={g.id}>💀 {g.name}</li>
            ))}
          </ul>
        </section>
      )}

      {survivors.length > 0 && (
        <section className="rounded-lg border border-stone-800 bg-stone-900/60 p-4">
          <h3 className="text-sm font-semibold text-emerald-400">Voltaram vivos (e curados)</h3>
          <ul className="mt-2 space-y-1 text-sm text-stone-400">
            {survivors.map((g) => (
              <li key={g.id}>🛡️ {g.name}</li>
            ))}
          </ul>
        </section>
      )}

      <button
        onClick={onReturn}
        className="w-full rounded-md bg-amber-500 px-4 py-3 text-sm font-medium text-stone-950 transition-colors hover:bg-amber-400"
      >
        Voltar à Guilda
      </button>
    </div>
  )
}
