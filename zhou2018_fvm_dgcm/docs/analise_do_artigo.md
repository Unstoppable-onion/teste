# Documentação técnica — análise do artigo e modelo implementado

**Artigo:** L. Zhou, H. Wang, A. Bergant, A. S. Tijsseling, D. Liu, S. Guo (2018).
*Godunov-Type Solutions with Discrete Gas Cavity Model for Transient Cavitating Pipe Flow.*
J. Hydraul. Eng. 144(5): 04018017. DOI 10.1061/(ASCE)HY.1943-7900.0001463 (9 páginas).

Convenção de rastreabilidade usada em todo o projeto:
`[T1]` Tabela 1 · `[Eq. n]` equação do artigo · `[p. n]` página (04018017-n) ·
`[Fig. n]` figura · `[DED]` informação **não fornecida** pelo artigo e deduzida
(seção 8, com justificativa e análise de sensibilidade).

---

## 1. Objetivo do artigo

Propor o **FVM-DGCM**: acoplar o modelo de cavidade de gás discreta (DGCM) a
esquemas de volumes finitos do tipo Godunov de 1ª e 2ª ordem para simular
golpe de aríete com cavitação vaporosa (separação de coluna), reduzindo os picos
espúrios de pressão dos modelos DVCM/DGCM clássicos (MOC) [p. 1]. O artigo
estuda a influência do coeficiente de ajuste de pressão `C_-ap`, da fração de gás
`α0`, do número de trechos `Ns` e do número de Courant `Cr`, e compara com
FVM-DVCM (Zhou et al. 2017), MOC-DGCM (Wylie et al. 1993) e experimentos
(Simpson 1986; Bergant & Simpson 1999) [p. 2, 4].

## 2. Problema físico

Sistema reservatório–tubo–válvula (Fig. 1, Tabela 1): tubo de cobre inclinado
para cima, com reservatório (pressurizado) a montante (cota inferior) e válvula
de esfera a jusante (cota superior). Escoamento permanente inicial `V0`; a
válvula é fechada rapidamente (tempo efetivo `Tc`), gerando golpe de aríete; a
onda negativa refletida leva a pressão junto à válvula à pressão de vapor,
formando uma cavidade cujo colapso gera pulsos de curta duração [p. 4–5].
O Caso 0 é um problema teórico sem atrito, horizontal, sem cavitação [T1].

## 3. Modelo matemático

**Gás livre (isotérmico), por trecho** [Eq. 1–2]:

    M_g R_g T = p*_g ∀_g = p*_0 α0 ∀                      (1)
    p*_g = ρ g (H − z − H_v),   H_v = p*_v/(ρ g) − H_b     (2)

**Continuidade da cavidade** [Eq. 3]: `d∀_g/dt = Q − Q_u`.

**Golpe de aríete** (termos convectivos desprezados) [Eq. 4]:

    ∂u/∂t + ∂f(u)/∂x = s(u),   f = A u,   u = (H, V)ᵀ,
    A = [[0, a²/g], [g, 0]],   s = (0, −f V|V|/(2D))ᵀ

As variáveis são a cota piezométrica `H` (m) e a velocidade média `V` (m/s).
Consistência dimensional: `a²/g · ∂V/∂x` [m/s], `g ∂H/∂x` [m/s²],
`fV|V|/(2D)` [m/s²] — verificado também por testes de similaridade (seção 7 do
relatório).

## 4. Hipóteses [p. 2]

1. Gás livre concentrado numa cavidade no meio de cada trecho;
2. cada trecho dividido em duas metades iguais (duas células FV);
3. pressão e vazão nas metades calculadas pelo FVM como no golpe de aríete puro;
4. o volume de cada cavidade é governado pelas vazões das metades adjacentes;
5. líquido puro com celeridade constante entre cavidades; gás isotérmico;
   massa de líquido conservada por continuidade local.

## 5. Métodos numéricos

* **Malha** [p. 2, Fig. 2]: `Ns` trechos de comprimento `Δx' = 2Δx`;
  `N = 2Ns` células de comprimento `Δx = L/N`; a cavidade `j` fica na interface
  entre as células `i` (metade de montante, `H_uj`, `Q_uj`) e `i+1 = 2j`
  (metade de jusante, `H_j`, `Q_j`); cota `z(j)` na posição da cavidade.
* **Volumes finitos** [Eq. 5]: `U_iⁿ⁺¹ = U_iⁿ − Δt/Δx (f_{i+1/2} − f_{i−1/2}) + …`
* **Fluxo de Godunov** — solução exata do problema de Riemann linear [Eq. 6]:

      H* = (H_L+H_R)/2 + (a/2g)(V_L−V_R),   V* = (V_L+V_R)/2 + (g/2a)(H_L−H_R),
      f_{i+1/2} = A U*

* **1ª ordem**: reconstrução constante por partes. **2ª ordem**: MUSCL-Hancock
  com limitador MINMOD (Toro 2009) [p. 3]. Na implementação o limitador é
  aplicado componente a componente em (H, V) e os valores de contorno de cada
  célula são evoluídos de Δt/2 com o fluxo homogêneo (sem fonte).
* **Termo fonte** por *splitting* + Runge–Kutta de 2ª ordem [Eq. 7–9]:
  `Ū = Uⁿ − Δt/Δx(Δf)`, `Ū̄ = Ū + Δt/2 s(Ū)`, `Uⁿ⁺¹ = Ū + Δt s(Ū̄)`.
* **Estabilidade** [p. 3]: CFL `Cr = aΔt/Δx ≤ 1` (a constante).
* **Contornos** [p. 3]: células virtuais `I_−1 = I_0 = U_{1/2}` e
  `I_{N+1} = I_{N+2} = U_{N+1/2}`, com `U_{1/2}`, `U_{N+1/2}` obtidos
  acoplando o invariante de Riemann à condição de contorno no instante n:
  * reservatório: `H_B = H_r`, `V_B = V_1 + (g/a)(H_r − H_1)` (característica C−);
  * válvula: `H_B = H_N + (a/g)(V_N − V_B)` (C+) + lei da válvula (seção 8.4).
* **Cavidades** [p. 3–4, Fig. 3]:
  * *Método I* (ambas as metades acima do vapor, sem cavitação):
    `H_g = (H_uj + H_j)/2` [10]; `∀_g = p*_0 α0 ∀ / [ρ g (H_g − z − H_v)]` [11];
    `H_uj ← C H_uj + (1−C) H_g`, `H_j ← C H_j + (1−C) H_g` [12–13].
  * *Método II* (cavitação em t ou alguma metade ≤ vapor):
    `∀_gⁿ⁺¹ = ∀_gⁿ + (Q_j − Q_uj)Δt` [15];
    `H_g = p*_0 α0 ∀ / (ρ g ∀_gⁿ⁺¹) + z + H_v` [16]; `H_uj = H_j = H_g` [17].
  * Fluxograma [Fig. 3]: se a cavitação não existe em t+Δt, volta-se ao Método I.

**Modelos de referência implementados**
* **FVM-DVCM** (Zhou et al. 2017) — limite de vapor puro: cavidade com cota de
  vapor, volume por continuidade, colapso quando `∀ ≤ 0` (sem ajuste de cotas
  fora da cavitação). Reconstruído a partir da descrição [p. 7] (seção 8.8).
* **MOC-DGCM com malha escalonada** (Wylie 1984; Wylie et al. 1993):
  cavidade de gás em todos os nós internos e na válvula; cada nó é atualizado a
  cada 2Δt (nós de paridade alternada); equação quadrática em
  `y = H_P − z − H_v` com ponderação `ψ = 1` (seção 8.7).
* **Solução exata do Caso 0**: onda quadrada de período 4L/a e amplitude
  `aV0/g` na válvula.

## 6. Condições iniciais e de contorno

* Inicial: escoamento permanente `V = V0`, linha piezométrica linear
  `H(x) = H_r − f x V0²/(2gD)` (perdas localizadas e carga cinética
  desprezadas); volumes de gás em equilíbrio [Eq. 11].
* Montante: nível constante `H_r` [T1]. Jusante: válvula de fechamento linear em
  `Tc` [T1, p. 7] (Caso 0: fechamento instantâneo, `Tc = 0`).

## 7. Parâmetros

### 7.1 Tabela 1 e texto

| Símbolo | Caso 0 | Caso 1 | Caso 2 | Caso 3 | Unid. | Fonte |
|---|---|---|---|---|---|---|
| V0 | 0,16 | 0,332 | 1,125 | 0,30 | m/s | T1 |
| H_r | 23,41 | 23,41 | 21,74 | 22,0 | m | T1 |
| T_c | 0,0 | 0,022 | 0,024 | 0,009 | s | T1 |
| D | 19,05 | 19,05 | 19,05 | 22,10 | mm | T1 |
| L | 36,0 | 36,0 | 36,0 | 37,2 | m | T1 |
| a | 1280 | 1280 | 1280 | 1319 | m/s | T1 |
| inclinação | horizontal | 1:36 | 1:36 | 3,2° | – | p. 4 |
| desnível válvula–entrada | 0 | 1,000 | 1,000 | 2,077 | m | p. 4 (37,2 sin 3,2°) |
| atrito | nenhum | Darcy f | Darcy f | Darcy f | – | T1, Eq. 4 |
| t final (eixo das figuras) | 1,0 | 0,45 | 0,45 | 0,57 | s | Figs. 4–11 |

### 7.2 Parâmetros numéricos do artigo

| Figura | Caso | Ordem | Ns | Cr | C_-ap | α0 | Fonte |
|---|---|---|---|---|---|---|---|
| 4 | 0 | 1 e 2 | 32 | 1 | 1; 0,9; 0,5; 0 | 1e-7 | p. 5 |
| 5 | 1 | 2 | 32 | 1 | 0,9 | 1e-7; 1e-8; 1e-10 | p. 5 |
| 6 | 1 | 2 | 32 e 256 | 1 | 1; 0,9; 0,8; 0,5 | 1e-7 | p. 5–6 |
| 7 | 2 | 2 | 32 | 1 | 1; 0,9 | 1e-7 | p. 6 |
| 8 | 3 | 2 | 256 | 1 | 1; 0,9 | 1e-7 | p. 6 |
| 9 | 1 | 1 e 2 | 32 | 1; 0,5; 0,1 | 0,9 | 1e-7 | p. 6–7 |
| 10 | 1 | 2 (FVM-DVCM) | 32 e 256 | 1 | – | – | p. 7 |
| 11 | 1 | MOC-DGCM | 32 e 256 | 1 | – | 1e-7 | p. 7 |

### 7.3 Parâmetros deduzidos `[DED]` (valores usados)

| Grandeza | Valor | Justificativa (seção 8) |
|---|---|---|
| g | 9,81 m/s² | padrão |
| ρ, ν (água 20 °C) | 998,2 kg/m³; 1,004e-6 m²/s | 8.2 |
| p_v (20 °C) | 2339 Pa → 0,239 m | 8.2 |
| p_bar, p*_0 | 101 325 Pa → H_b = 10,347 m | 8.2 |
| H_v | −10,109 m | Eq. 2 |
| f (Blasius, tubo liso) | 0,0355 / 0,0261 / 0,0351 (Casos 1/2/3) | 8.1 |
| datum | entrada do tubo (z = 0 a montante) | 8.3 |
| K da válvula aberta | 2,55 (Casos 1–2); 18,9 (Caso 3) | 8.4 |
| saída "na válvula" | cota da última célula I_N | 8.6 |

## 8. Informações ausentes e deduções

**8.1 Fator de atrito.** Não informado. Os tubos de cobre são hidraulicamente
lisos e Re = 6,3·10³–2,1·10⁴; usou-se Blasius `f = 0,316 Re^−0,25`.
Verificação independente: a cota inicial na válvula lida nas curvas numéricas
do artigo é 18,61 m no Caso 2 (Fig. 7) contra 18,55 m calculado com Blasius
(diferença de 0,06 m ≈ 0,1 px); Caso 1: 23,05–23,23 m (artigo) × 23,03 m.

**8.2 Propriedades da água e pressão barométrica.** Não informadas. Adotou-se
água a 20 °C e atmosfera padrão, sem ajuste. O patamar de vapor resultante na
válvula (−9,11 m nos Casos 1–2; −8,03 m no Caso 3) difere do patamar lido nas
curvas do artigo (−8,8 a −9,5 m; −8,41 m) em ≤ 0,4 m (≈ 1,2 px). O efeito de
±0,3 m está quantificado na tabela T5.

**8.3 Datum.** Não informado explicitamente. Com datum na **entrada do tubo**,
o patamar de cavitação na válvula é `z_válvula + H_v = 1,0 − 10,11 = −9,11 m`,
coerente com as curvas (−8,8 a −9,5 m); com datum na válvula seria −10,1 m,
incompatível. A invariância a mudança de datum (H_r e z deslocados juntos) é
verificada por teste.

**8.4 Lei da válvula.** O artigo diz apenas "fechamento linear" com tempo
efetivo `Tc` [p. 7]. As curvas numéricas do artigo mostram cota constante até
quase `Tc` e subida quase vertical — incompatível com vazão decrescente
linearmente (que daria rampa desde t = 0) e compatível com a lei de orifício
`V = V0 τ √(ΔH/ΔH0)`, `τ = 1 − t/Tc`, com perda de carga da válvula aberta
`ΔH0 = K V0²/(2g)` pequena. `K` foi inferido pelo instante de meia subida
(`t50`) medido nas próprias curvas numéricas do artigo
(`scripts/calibrate_valve.py`): Caso 1 → K = 2,55; **com o mesmo K o Caso 2
(mesma instalação) é previsto com erro de 0,05 ms**, validação independente;
Caso 3 (outra instalação) → K = 18,9 (sem verificação independente possível).
A cota a jusante da válvula é `H_válvula,0 − ΔH0`.

**8.5 Algoritmo de cavidade — pontos não especificados.**
* *"A cavitação existe em t+Δt?"* (Fig. 3): adotado `∀_gⁿ⁺¹ > 0` (critério
  clássico de colapso do DVCM). A alternativa "pressão do gás > média das
  metades" foi testada (T5): resultados equivalentes.
* *Regularização do Método I* (`limit_gas_growth`): com a Eq. (11) literal,
  quando a média das metades se aproxima da cota de vapor o volume de gás
  tende a infinito e esse volume espúrio é herdado pelo Método II. Com Ns = 256
  isso atrasa o 1º colapso em 9–11 ms (Caso 1: 154,0 ms × 144,5 ms do
  artigo; Caso 3: 143,3 ms × 132,0 ms), o que as Figs. 6 e 8 do artigo não
  mostram. Adotou-se: no Método I o volume de gás não pode crescer mais do que a
  continuidade permite, `∀ ≤ ∀ⁿ + max(∀_cont − ∀ⁿ, 0)`. Com isso os colapsos
  ficam a 0,5–1,5 ms do artigo para Ns = 32 e 256. Esta é uma **adaptação
  documentada**, necessária e ligável/desligável (`limit_gas_growth`).
* *Caso impossível* (continuidade dá `∀ ≤ 0` com média das metades ≤ vapor):
  mantém-se a cavidade com o volume anterior (`fallback = "keep"`); a
  alternativa "colapso tipo DVCM" dá resultados equivalentes (T5).

**8.6 Grandeza plotada "na válvula".** O artigo não diz se é o estado de
contorno `U_{N+1/2}` ou a célula `I_N`. No Caso 0 com `C_-ap = 0` o primeiro
ponto do artigo é ≈ 33,7 m e a subida é monotônica; a célula `I_N` dá
33,85 → 41,7 → 43,0 → 43,5 m (igual ao artigo), enquanto o estado de contorno
oscila (33,9 → 52,1 → 40,4 …). Adotou-se a **cota da célula I_N**.

**8.7 MOC-DGCM.** "Malha escalonada" (Wylie et al. 1993) implementada com nós
de paridade alternada e Δt = Δx'/a; ponderação `ψ = 1` (implícita; `ψ = 0,5`
gerou oscilações espúrias); cavidade também no nó da válvula; durante o
movimento da válvula o nó da válvula é resolvido sem cavidade (pressões muito
acima do vapor).

**8.8 FVM-DVCM.** Reconstruído a partir da descrição [p. 7]: mesmo FVM, cavidade
no meio do trecho, cota de vapor imposta às duas metades enquanto `∀ > 0`.

**8.9 Tempos finais.** Iguais ao eixo das abscissas das figuras.

## 9. Resultados a reproduzir

| ID | Resultado | Conteúdo |
|---|---|---|
| R01–R04 | Fig. 4 a–d | Caso 0: 1ª e 2ª ordem × exata, C = 1; 0,9; 0,5; 0 |
| R05 | Fig. 5 | Caso 1: efeito de α0 (1e-7, 1e-8, 1e-10) × experimento |
| R06–R09 | Fig. 6 a–d | Caso 1: C = 1; 0,9; 0,8; 0,5 com Ns = 32 e 256 × experimento |
| R10 | Fig. 7 | Caso 2 (cavidade grande), C = 1 e 0,9 |
| R11 | Fig. 8 | Caso 3, Ns = 256, C = 1 e 0,9 |
| R12–R13 | Fig. 9 a–b | Efeito de Cr (1; 0,5; 0,1) na 1ª e 2ª ordem |
| R14 | Fig. 10 | FVM-DVCM, Ns = 32 e 256 |
| R15 | Fig. 11 | MOC-DGCM, Ns = 32 e 256 |
| R16 | Tabela 1 | condições iniciais (cota inicial, Joukowsky, patamar de vapor) |
| R17 | Texto/conclusões | afirmações quantitativas 1–9 (seção 6 do relatório) |

O artigo **não apresenta tabelas de resultados numéricos**: todos os resultados
estão em gráficos, que foram digitalizados (relatório, seção 3).

## 10. Critérios de validação

Comparação quantitativa com as curvas numéricas do artigo digitalizadas
(principal) e com os experimentos digitalizados (secundária). Métricas e
tolerâncias justificadas pela resolução das figuras: relatório, seção 4.

## 11. Escolha da linguagem e arquitetura

**Python 3 + NumPy** para a implementação de referência: operações vetoriais
idênticas às do MATLAB (conversão direta, mesmas fórmulas e ordem de
operações), depuração rápida, `pytest` para testes automatizados, `matplotlib`
para figuras e ferramentas de processamento de imagem para a digitalização.
Precisão: ponto flutuante IEEE-754 de dupla precisão em ambas as linguagens —
permitiu verificar **igualdade bit a bit (até 1e-9 m no arquivo)** entre as
duas implementações.

```
python/fvmdgcm/params.py        parâmetros (Tabela 1, fluido, numéricos)
python/fvmdgcm/godunov.py       Riemann (Eq. 6), MUSCL-Hancock/MINMOD, fonte RK2 (Eqs. 8-9)
python/fvmdgcm/boundaries.py    reservatório e válvula (invariantes de Riemann)
python/fvmdgcm/cavity.py        Métodos I/II (Eqs. 10-17), DVCM
python/fvmdgcm/fvm_solver.py    laço temporal FVM (Eqs. 5-9, Fig. 3)
python/fvmdgcm/moc_dgcm.py      MOC-DGCM de referência (malha escalonada)
python/fvmdgcm/exact.py         solução exata do Caso 0
python/fvmdgcm/experiments.py   matriz de reprodução (todas as simulações)
python/fvmdgcm/metrics.py       métricas de comparação
python/digitize/                digitalização das figuras
python/scripts/                 execução, validação, sensibilidade, figuras, tabelas
python/tests/                   testes de verificação (pytest)
matlab/src, matlab/*.m          conversão integral para MATLAB (mesma arquitetura)
```

## 12. Algoritmo (por passo de tempo)

```
para n = 0 … nsteps−1:
    U_{1/2}   ← reservatório(H_r, invariante C− da célula 1)
    U_{N+1/2} ← válvula(τ(tⁿ), invariante C+ da célula N)
    células virtuais ← estados de contorno
    (U_L, U_R) nas interfaces ← Godunov (1ª) | MUSCL-Hancock+MINMOD (2ª)
    U* ← Riemann exato (Eq. 6);  f = A U*
    Ū ← Uⁿ − Δt/Δx (f_{i+1/2} − f_{i−1/2})                 (Eq. 7)
    V ← RK2 do atrito (Eqs. 8–9)
    para cada trecho j: Método I ou II (Eqs. 10–17, Fig. 3)   [DGCM]
                        ou cavidade de vapor                    [DVCM]
```
