import { useEffect } from 'react'
import { useGuildStore } from '../../core/store/useGuildStore'
import { GladiatorCard } from '../../components/GladiatorCard'

/**
 * Tela principal da fase de Base (City Builder / Gerenciamento).
 * Recursos + recrutamento chegam neste Passo 2. Construções que afetam
 * o pool de recrutamento (tamanho, raridade mínima, custo de reroll)
 * chegam no Passo 3.
 */
export function GuildView() {
  const resources = useGuildStore((state) => state.resources)
  const roster = useGuildStore((state) => state.roster)
  const recruitmentPool = useGuildStore((state) => state.recruitmentPool)
  const refreshRecruitmentPool = useGuildStore((state) => state.refreshRecruitmentPool)
  const recruitFromPool = useGuildStore((state) => state.recruitFromPool)

  useEffect(() => {
    if (recruitmentPool.length === 0) refreshRecruitmentPool()
  }, [recruitmentPool.length, refreshRecruitmentPool])

  return (
    <div className="space-y-8">
      <section className="grid grid-cols-3 gap-4">
        <ResourceCard label="Ouro" value={resources.gold} />
        <ResourceCard label="Fama" value={resources.fame} />
        <ResourceCard label="Materiais" value={resources.materials} />
      </section>

      <section>
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-amber-400">Recrutamento</h2>
          <button
            onClick={() => refreshRecruitmentPool()}
            className="text-xs font-medium text-stone-400 underline-offset-2 hover:text-amber-400 hover:underline"
          >
            Atualizar candidatos
          </button>
        </div>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          {recruitmentPool.map((candidate) => (
            <GladiatorCard
              key={candidate.id}
              gladiator={candidate}
              action={{
                label: `Recrutar (${candidate.recruitCost} ouro)`,
                onClick: () => recruitFromPool(candidate.id),
                disabled: resources.gold < candidate.recruitCost,
              }}
            />
          ))}
        </div>
      </section>

      <section>
        <h2 className="mb-3 text-lg font-semibold text-amber-400">Sua Guilda</h2>
        {roster.length === 0 ? (
          <p className="text-sm text-stone-400">
            Nenhum gladiador recrutado ainda. Recrute alguém acima para começar.
          </p>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            {roster.map((gladiator) => (
              <GladiatorCard key={gladiator.id} gladiator={gladiator} />
            ))}
          </div>
        )}
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
