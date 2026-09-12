# Gladiator Guild

Um híbrido de Gladiator Guild Manager + City Builder + Roguelike. O jogador
gerencia uma guilda de gladiadores (fase de Base) e os envia em runs de
combate por turnos com permadeath (fase de Arena).

## Stack

- **React 19 + TypeScript** — UI de gerenciamento (City Builder)
- **Tailwind CSS 4** — estilização
- **Zustand** (com middleware `persist`) — estado global, persistido em
  `localStorage`
- **Vite** — build tool
- **Motor de combate em TypeScript puro** — sem dependência de motor
  gráfico; roda "headless" e pode ser renderizado por qualquer camada de UI
  (hoje: React/CSS; futuramente, se necessário: Phaser/Canvas)

## Estrutura de pastas

```
src/
├── app/                    # Shell de navegação de topo (troca entre fases)
├── core/
│   ├── types/              # Tipos de domínio compartilhados (Gladiator, Building, Combat...)
│   ├── store/               # Stores Zustand, fatiados por domínio
│   ├── engine/              # Motor de combate — lógica pura, sem UI
│   └── generators/          # Geração procedural (gladiadores, etc.)
├── data/                    # JSON de balanceamento (templates, custos, inimigos)
├── features/
│   ├── city-builder/        # UI da fase de Base (construções, recrutamento)
│   └── combat/               # UI da fase de Arena (batalhas)
└── components/               # Componentes de UI genéricos/compartilhados
```

### Princípios de arquitetura

1. **Estado separado de UI**: todo estado persistente vive em `core/store`.
   As telas em `features/` apenas leem e despacham ações — não guardam
   lógica de negócio.
2. **Motor de combate desacoplado**: `core/engine` não importa React. Isso
   permite testar/simular combates sem renderizar nada, e trocar a
   apresentação visual no futuro sem reescrever as regras.
3. **Balanceamento como dado**: status de gladiadores, custos de
   construções e status de inimigos vivem em JSON (`src/data`), não
   hardcoded na lógica — facilita ajustar o jogo sem mexer em código.
4. **Meta-progressão**: recursos obtidos numa run de Arena são creditados
   na guilda ao final da run, independentemente do resultado. Gladiadores
   mortos em combate são perdidos permanentemente (permadeath).

## Rodando o projeto

```bash
npm install
npm run dev
```

## Roadmap (execução iterativa)

- [x] **Passo 1** — Setup do projeto, stack e estrutura de pastas
- [ ] **Passo 2** — Recursos (Ouro/Fama) e geração procedural de gladiadores
- [ ] **Passo 3** — City Builder: construções que afetam o recrutamento
- [ ] **Passo 4** — MVP do loop de combate (turnos, permadeath, recompensas)
