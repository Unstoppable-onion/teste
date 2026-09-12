import type { CombatState } from '../types'

/**
 * Motor de Combate — lógica pura, sem React e sem dependência de renderização.
 *
 * Implementado no Passo 4. A ideia central: `resolveNextTurn` recebe o
 * estado atual do combate e devolve o próximo estado + os eventos gerados
 * naquele turno, permitindo tanto rodar o combate "headless" (testes,
 * simulação de balanceamento) quanto animá-lo turno a turno na UI.
 */
export function resolveNextTurn(state: CombatState): CombatState {
  // TODO (Passo 4): resolver o turno do ator atual (ataque, defesa,
  // aplicar dano, checar morte, avançar turnOrder, checar vitória/derrota).
  return state
}
