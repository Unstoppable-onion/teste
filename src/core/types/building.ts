/**
 * Domínio: Construções da Guilda (City Builder)
 *
 * Cada construção tem níveis; o nível atual determina os efeitos
 * ativos. Por ora só o Alojamento existe (afeta o recrutamento);
 * Ferreiro e Campo de Treinamento entram em passos futuros, cada um
 * usando os campos de efeito que fizerem sentido pro seu domínio
 * (equipamentos, bônus de treino, etc.) — por isso os campos de
 * efeito ficam soltos e opcionais em vez de uma interface rígida.
 */

import type { GladiatorRarity } from './gladiator'

export type BuildingType = 'lodging' | 'blacksmith' | 'trainingGrounds'

export interface BuildingLevelData {
  level: number
  cost: {
    gold: number
    materials: number
  }
  /** Descrição textual do efeito deste nível (balanceado via JSON) */
  effectDescription: string

  // Efeitos específicos do Alojamento sobre o recrutamento:
  poolSize?: number
  rarityWeights?: Record<GladiatorRarity, number>
}

export interface Building {
  id: BuildingType
  name: string
  description: string
  currentLevel: number
  levels: BuildingLevelData[]
}
