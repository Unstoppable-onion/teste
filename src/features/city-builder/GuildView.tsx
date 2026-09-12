import { useGuildStore } from '../../core/store/useGuildStore'

/**
 * Tela principal da fase de Base (City Builder / Gerenciamento).
 * Conteúdo real (construções, recrutamento) chega no Passo 2 e 3.
 */
export function GuildView() {
  const resources = useGuildStore((state) => state.resources)
  const roster = useGuildStore((state) => state.roster)

  return (
    <div className="space-y-6">
      <section className="grid grid-cols-3 gap-4">
        <ResourceCard label="Ouro" value={resources.gold} />
        <ResourceCard label="Fama" value={resources.fame} />
        <ResourceCard label="Materiais" value={resources.materials} />
      </section>

      <section className="rounded-lg border border-stone-800 bg-stone-900/60 p-6">
        <h2 className="text-lg font-semibold text-amber-400">Sua Guilda</h2>
        <p className="mt-2 text-sm text-stone-400">
          {roster.length === 0
            ? 'Nenhum gladiador recrutado ainda. O recrutamento chega no Passo 2.'
            : `${roster.length} gladiador(es) na guilda.`}
        </p>
      </section>
    </div>
  )
}

function ResourceCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-lg border border-stone-800 bg-stone-900/60 p-4">
      <p className="text-xs uppercase tracking-wide text-stone-500">{label}</p>
      <p className="mt-1 text-2xl font-bold text-stone-100">{value}</p>
    </div>
  )
}
