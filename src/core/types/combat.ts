/**
 * Domínio: Combate (Roguelike / Arena)
 *
 * O motor de combate (core/engine) é lógica pura, sem dependência de UI —
 * recebe um estado de combate e retorna o próximo estado + um log de eventos.
 * Isso permite testar o balanceamento sem renderizar nada, e trocar a
 * camada de apresentação (React/CSS -> Phaser/Canvas) sem tocar nas regras.
 *
 * Implementado no Passo 4: turnos alternados por velocidade (iniciativa
 * fixa, sorteada uma vez no início do combate), permadeath (gladiador
 * morto em combate nunca retorna) e runs de múltiplas waves.
 */

import type { Gladiator } from './gladiator'

export interface Enemy {
  id: string
  name: string
  stats: {
    hp: number
    maxHp: number
    attack: number
    defense: number
    speed: number
  }
}

export type CombatEventType = 'attack' | 'death' | 'victory' | 'defeat'

export interface CombatEvent {
  type: CombatEventType
  sourceId: string
  targetId?: string
  amount?: number
  message: string
}

export interface CombatState {
  party: Gladiator[]
  enemies: Enemy[]
  turnOrder: string[]
  currentTurnIndex: number
  log: CombatEvent[]
  isOver: boolean
  didWin: boolean
}

/**
 * Resultado de uma run completa (sequência de waves/combates).
 * `finalParty` reflete permadeath: gladiadores mortos vêm com isDead=true
 * e HP 0; a store da guilda os remove definitivamente do roster ao
 * aplicar o resultado.
 */
export interface RunResult {
  logsByWave: CombatEvent[][]
  /**
   * Estado da equipe (HP, isDead) exatamente ao ENTRAR em cada wave —
   * ou seja, antes daquela wave começar. Só existe uma entrada por wave
   * realmente disputada (se a run acabou antes, o array é mais curto que
   * totalWaves). Serve pra UI "reproduzir" o log evento a evento e animar
   * o combate; o motor em si já resolveu tudo de uma vez.
   */
  partyByWave: Gladiator[][]
  finalParty: Gladiator[]
  clearedWaves: number
  totalWaves: number
  didClearRun: boolean
  goldEarned: number
  materialsEarned: number
}
