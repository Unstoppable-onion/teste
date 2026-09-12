import type { Enemy, Gladiator, RunResult } from '../types'
import { simulateCombat } from './combatEngine'

/**
 * Orquestra uma run completa: várias waves em sequência, sem cura entre
 * elas (o dano acumula — a única cura acontece ao voltar para a guilda).
 * Para na primeira wave perdida; gladiadores mortos ficam isDead=true e
 * saem da run definitivamente (permadeath), mas os já mortos numa wave
 * anterior simplesmente não voltam a lutar na próxima.
 *
 * As recompensas de cada wave só são contadas se a wave foi vencida —
 * mas mesmo que a run termine em derrota total, o ouro/materiais das
 * waves já vencidas volta para a guilda (meta-progressão).
 */
export function simulateRun(
  initialParty: Gladiator[],
  waves: Enemy[][],
  waveGoldReward: number[],
  waveMaterialsReward: number[],
): RunResult {
  let currentParty = initialParty
  const logsByWave: RunResult['logsByWave'] = []
  let goldEarned = 0
  let materialsEarned = 0
  let clearedWaves = 0

  for (let i = 0; i < waves.length; i++) {
    const livingParty = currentParty.filter((g) => !g.isDead && g.stats.hp > 0)
    if (livingParty.length === 0) break

    const combatResult = simulateCombat(livingParty, waves[i])
    logsByWave.push(combatResult.log)
    currentParty = mergeParty(currentParty, combatResult.party)

    if (!combatResult.didWin) break

    clearedWaves++
    goldEarned += waveGoldReward[i] ?? 0
    materialsEarned += waveMaterialsReward[i] ?? 0
  }

  return {
    logsByWave,
    finalParty: currentParty,
    clearedWaves,
    totalWaves: waves.length,
    didClearRun: clearedWaves === waves.length,
    goldEarned,
    materialsEarned,
  }
}

/** Reaplica o resultado de uma wave sobre o roster completo (preserva quem não lutou nela). */
function mergeParty(original: Gladiator[], updated: Gladiator[]): Gladiator[] {
  return original.map((g) => updated.find((u) => u.id === g.id) ?? g)
}
