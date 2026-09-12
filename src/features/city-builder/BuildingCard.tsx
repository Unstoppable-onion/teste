import type { Building } from '../../core/types'

/**
 * Card de uma construção da guilda: mostra o nível atual, seu efeito,
 * e — se houver um próximo nível — o custo e efeito da melhoria.
 */
export function BuildingCard({
  building,
  onUpgrade,
  canAfford,
}: {
  building: Building
  onUpgrade: () => void
  canAfford: boolean
}) {
  const currentLevelData = building.levels.find((l) => l.level === building.currentLevel)
  const nextLevelData = building.levels.find((l) => l.level === building.currentLevel + 1)

  return (
    <div className="flex flex-col gap-3 rounded-lg border border-stone-800 bg-stone-900/60 p-5">
      <div className="flex items-start justify-between gap-2">
        <div>
          <h3 className="font-semibold text-stone-100">{building.name}</h3>
          <p className="mt-1 text-sm text-stone-400">{building.description}</p>
        </div>
        <span className="shrink-0 rounded bg-stone-800 px-2 py-0.5 text-xs font-semibold text-stone-300">
          Nível {building.currentLevel}
        </span>
      </div>

      <p className="text-xs text-stone-500">
        Efeito atual: {currentLevelData?.effectDescription}
      </p>

      {nextLevelData ? (
        <div className="mt-1 flex items-center justify-between gap-3 rounded-md bg-stone-800/50 p-3">
          <div>
            <p className="text-xs text-stone-400">
              Próximo nível: {nextLevelData.effectDescription}
            </p>
            <p className="mt-0.5 text-xs text-stone-500">
              Custo: {nextLevelData.cost.gold} ouro
              {nextLevelData.cost.materials > 0 ? ` + ${nextLevelData.cost.materials} materiais` : ''}
            </p>
          </div>
          <button
            onClick={onUpgrade}
            disabled={!canAfford}
            className="shrink-0 rounded-md bg-amber-500 px-3 py-2 text-sm font-medium text-stone-950 transition-colors hover:bg-amber-400 disabled:cursor-not-allowed disabled:bg-stone-700 disabled:text-stone-400"
          >
            Melhorar
          </button>
        </div>
      ) : (
        <p className="text-xs font-medium text-amber-400">Nível máximo alcançado.</p>
      )}
    </div>
  )
}
