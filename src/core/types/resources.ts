/**
 * Domínio: Recursos da Guilda
 *
 * Recursos são globais e persistem entre runs (meta-progressão).
 * Materiais entram no Passo 3 (City Builder / upgrades).
 */

export interface GuildResources {
  gold: number
  fame: number
  materials: number
}

export const INITIAL_RESOURCES: GuildResources = {
  gold: 500,
  fame: 0,
  materials: 0,
}
