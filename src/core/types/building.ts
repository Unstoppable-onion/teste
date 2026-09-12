/**
 * Domínio: Construções da Guilda (City Builder)
 *
 * Cada construção tem níveis; o nível atual determina os efeitos
 * ativos (ex: aumentar o tamanho do pool de recrutamento).
 * Detalhado no Passo 3.
 */

export type BuildingType = 'lodging' | 'blacksmith' | 'trainingGrounds'

export interface BuildingLevelData {
  level: number
  cost: {
    gold: number
    materials: number
  }
  /** Descrição textual do efeito deste nível (balanceado via JSON) */
  effectDescription: string
}

export interface Building {
  id: BuildingType
  name: string
  currentLevel: number
  levels: BuildingLevelData[]
}
