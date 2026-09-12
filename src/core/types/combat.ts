/**
 * Domínio: Combate (Roguelike / Arena)
 *
 * O motor de combate (core/engine) é lógica pura, sem dependência de UI —
 * recebe um estado de combate e retorna o próximo estado + um log de eventos.
 * Isso permite testar o balanceamento sem renderizar nada, e trocar a
 * camada de apresentação (React/CSS -> Phaser/Canvas) sem tocar nas regras.
 * Detalhado no Passo 4.
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
