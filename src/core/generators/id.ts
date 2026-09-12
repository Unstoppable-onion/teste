/** Gera um id único, usado por qualquer gerador procedural (gladiadores, inimigos...). */
export function generateId(prefix: string): string {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID()
  }
  return `${prefix}-${Date.now()}-${Math.floor(Math.random() * 1e9)}`
}
