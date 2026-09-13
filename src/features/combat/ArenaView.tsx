import { useEffect, useState } from 'react'
import { useGuildStore } from '../../core/store/useGuildStore'
import { generateRunWaves, getWaveRewards } from '../../core/generators/enemyGenerator'
import { simulateRun } from '../../core/engine/runEngine'
import type { Enemy, RunResult } from '../../core/types'
import { GladiatorCard } from '../../components/GladiatorCard'
import { CombatStage } from './CombatStage'
import { CombatLogView } from './CombatLogView'
import { RunResultSummary } from './RunResultSummary'

const MAX_TEAM_SIZE = 3
const REVEAL_INTERVAL_MS = 500
const WAVE_PAUSE_MS = 900

type ArenaStep = 'select' | 'running' | 'result'

/**
 * Tela principal da fase de Batalha (Roguelike / Arena).
 *
 * A run inteira é simulada de uma vez (motor de combate é puro/headless —
 * ver core/engine) assim que o jogador confirma a equipe; o resultado já
 * é aplicado à guilda (permadeath + recompensas) naquele momento. As
 * etapas 'running' apenas reproduzem visualmente, turno a turno, um log
 * que já existe — trocar essa reprodução por animações mais ricas (ou
 * por Phaser/Canvas) no futuro não exige tocar nas regras de combate.
 */
export function ArenaView() {
  const roster = useGuildStore((state) => state.roster)
  const applyRunResults = useGuildStore((state) => state.applyRunResults)

  const [step, setStep] = useState<ArenaStep>('select')
  const [selectedIds, setSelectedIds] = useState<string[]>([])
  const [runResult, setRunResult] = useState<RunResult | null>(null)
  const [waves, setWaves] = useState<Enemy[][]>([])
  const [waveIndex, setWaveIndex] = useState(0)
  const [revealedCount, setRevealedCount] = useState(0)

  // Revela um evento do log por vez, no ritmo de REVEAL_INTERVAL_MS.
  useEffect(() => {
    if (step !== 'running' || !runResult) return
    const currentLog = runResult.logsByWave[waveIndex] ?? []
    if (revealedCount >= currentLog.length) return

    const timer = setTimeout(() => setRevealedCount((c) => c + 1), REVEAL_INTERVAL_MS)
    return () => clearTimeout(timer)
  }, [step, runResult, waveIndex, revealedCount])

  // Ao terminar de revelar uma wave, avança pra próxima ou encerra a run.
  useEffect(() => {
    if (step !== 'running' || !runResult) return
    const currentLog = runResult.logsByWave[waveIndex] ?? []
    if (revealedCount < currentLog.length) return

    const timer = setTimeout(() => {
      const hasNextWave = waveIndex + 1 < runResult.logsByWave.length
      if (hasNextWave) {
        setWaveIndex((i) => i + 1)
        setRevealedCount(0)
      } else {
        setStep('result')
      }
    }, WAVE_PAUSE_MS)
    return () => clearTimeout(timer)
  }, [step, runResult, waveIndex, revealedCount])

  function toggleSelected(id: string) {
    setSelectedIds((current) => {
      if (current.includes(id)) return current.filter((c) => c !== id)
      if (current.length >= MAX_TEAM_SIZE) return current
      return [...current, id]
    })
  }

  function handleStartRun() {
    const party = roster.filter((g) => selectedIds.includes(g.id))
    if (party.length === 0) return

    const runWaves = generateRunWaves()
    const rewards = getWaveRewards()
    const result = simulateRun(party, runWaves, rewards.gold, rewards.materials)

    applyRunResults(result)
    setRunResult(result)
    setWaves(runWaves)
    setWaveIndex(0)
    setRevealedCount(0)
    setStep('running')
  }

  function handleReturnToGuild() {
    setStep('select')
    setSelectedIds([])
    setRunResult(null)
  }

  if (step === 'result' && runResult) {
    return <RunResultSummary result={runResult} onReturn={handleReturnToGuild} />
  }

  if (step === 'running' && runResult) {
    const revealedEvents = (runResult.logsByWave[waveIndex] ?? []).slice(0, revealedCount)
    return (
      <div className="space-y-4">
        <CombatStage
          initialParty={runResult.partyByWave[waveIndex] ?? []}
          initialEnemies={waves[waveIndex] ?? []}
          revealedEvents={revealedEvents}
        />
        <CombatLogView
          totalWaves={runResult.totalWaves}
          waveIndex={waveIndex}
          events={revealedEvents}
          onSkip={() => setStep('result')}
        />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <section className="rounded-lg border border-stone-800 bg-stone-900/60 p-6">
        <h2 className="text-lg font-semibold text-amber-400">Arena</h2>
        <p className="mt-2 text-sm text-stone-400">
          Escolha até {MAX_TEAM_SIZE} gladiadores para enfrentar 3 waves de inimigos.
          Quem morrer em combate é perdido permanentemente — mas o ouro e os
          materiais conquistados voltam para a guilda mesmo se a equipe cair.
        </p>
      </section>

      {roster.length === 0 ? (
        <p className="text-sm text-stone-400">
          Sua guilda ainda não tem gladiadores. Recrute alguém na aba Guilda primeiro.
        </p>
      ) : (
        <>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            {roster.map((gladiator) => {
              const selected = selectedIds.includes(gladiator.id)
              return (
                <GladiatorCard
                  key={gladiator.id}
                  gladiator={gladiator}
                  action={{
                    label: selected ? 'Selecionado ✓' : 'Selecionar',
                    onClick: () => toggleSelected(gladiator.id),
                    disabled: !selected && selectedIds.length >= MAX_TEAM_SIZE,
                  }}
                />
              )
            })}
          </div>

          <div className="flex items-center justify-between rounded-lg border border-stone-800 bg-stone-900/60 p-4">
            <p className="text-sm text-stone-400">
              Equipe selecionada: {selectedIds.length}/{MAX_TEAM_SIZE}
            </p>
            <button
              onClick={handleStartRun}
              disabled={selectedIds.length === 0}
              className="rounded-md bg-amber-500 px-4 py-2 text-sm font-medium text-stone-950 transition-colors hover:bg-amber-400 disabled:cursor-not-allowed disabled:bg-stone-700 disabled:text-stone-400"
            >
              Iniciar Run
            </button>
          </div>
        </>
      )}
    </div>
  )
}
