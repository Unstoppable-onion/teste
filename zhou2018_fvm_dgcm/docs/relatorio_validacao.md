# Relatório de validação — reprodução de Zhou et al. (2018)

Todos os números deste relatório vêm de arquivos gerados pelo código
(`results/validation/*.json`); as tabelas completas, geradas automaticamente,
estão em [`tabelas_validacao.md`](tabelas_validacao.md) (T1–T8). As figuras
reproduzidas estão em `results/figures/` (Python) e `results/figures_matlab/`
(dados MATLAB/Octave), com a curva digitalizada do artigo sobreposta; uma
figura por simulação está em `results/figures/per_run/`.

## 1. Resumo

* **37 séries simuladas** (todas as curvas das Figs. 4–11) em duas
  implementações independentes (Python e MATLAB/Octave), **idênticas até
  1e-9 m** (precisão de gravação) em todas as 37 séries.
* Contra as curvas numéricas do artigo (digitalizadas):
  **23 VALIDADO**, **3 PARCIAL** (dinâmica global validada, amplitudes de
  picos espúrios diferentes), **6 DIVERGENTE**, **5 NÃO AVALIÁVEL**
  (série quase totalmente escondida por outras curvas na figura).
* As curvas centrais do artigo (FVM-DGCM de 2ª ordem com `C_-ap = 0,9`,
  Casos 1, 2 e 3; efeito de `Cr`; Caso 0 com `C_-ap ≥ 0,5`) estão
  **validadas**: cotas planas com erro mediano de 0,2–0,8 m (tolerância
  1,0–1,5 m) e tempos de colapso/chegada de ondas com erro médio de
  0,2–2,2 ms (tolerância 2,5 ms).
* Divergências remanescentes (seção 8): amortecimento do Caso 0 com
  `C_-ap = 0` (artigo ≈ 1,5× mais dissipativo), sensibilidade a `α0` menor que a
  do artigo, amplitude de picos espúrios (`C_-ap = 1`, DVCM, MOC), atraso de
  ≈ 1,5 ms do MOC-DGCM do artigo e necessidade de uma regularização do
  Método I (documentada) para reproduzir os resultados com Ns = 256.

## 2. Matriz de reprodução

| ID | Resultado | Implementação | Validação | Estado |
|---|---|---|---|---|
| R01 | Fig. 4a — Caso 0, C = 1 (1ª/2ª ordem × exata) | `fvm_solver` + `exact` | erro vs exata 1,3e-11 m; vs artigo MedAE 0,04 m, Δt 0,28 ms | **Validado** |
| R02 | Fig. 4b — C = 0,9 | idem | MedAE 0,05 m, Δt 0,21 ms | **Validado** |
| R03 | Fig. 4c — C = 0,5 | idem | MedAE 0,04 m, Δt 0,31 ms | **Validado** |
| R04 | Fig. 4d — C = 0 | idem | MedAE 0,40 m (tol. 0,38); extremos finais 42,24/4,87 m × 41,15/5,72 m | **Divergente** (amortecimento menor) |
| R05 | Fig. 5 — α0 | idem | α0 = 1e-7: MedAE 0,48 m, Δt 0,90 ms; α0 = 1e-8: Δt 2,6 ms; α0 = 1e-10: série oculta | **Parcial**: 1e-7 validado, 1e-8 divergente, 1e-10 não avaliável |
| R06 | Fig. 6a — C = 1, Ns = 32/256 | idem | dinâmica global OK (MedAE 0,17/0,34 m; Δt 1,19/0,75 ms); picos espúrios diferem até 41 m | **Parcial** |
| R07 | Fig. 6b — C = 0,9 | idem | Ns = 32: MedAE 0,24 m, Δt 1,02 ms; Ns = 256: 0,71 m, 0,52 ms | **Validado** |
| R08 | Fig. 6c — C = 0,8 | idem | 0,31 m / 0,47 ms; 0,31 m / 0,74 ms | **Validado** |
| R09 | Fig. 6d — C = 0,5 | idem | 0,59 m / 0,68 ms; 0,37 m / 1,03 ms | **Validado** |
| R10 | Fig. 7 — Caso 2 | idem | C = 0,9: patamar de Joukowsky 166,90 × 166,89 m; MedAE 0,34 m; Δt 2,24 ms; C = 1 oculta | **Validado** (C = 0,9) |
| R11 | Fig. 8 — Caso 3, Ns = 256 | idem | C = 0,9: MedAE 0,35 m, Δt 0,20 ms, picos ≤ 0,8 m; C = 1: picos espúrios mal condicionados | **Validado** (C = 0,9); C = 1 **divergente** |
| R12 | Fig. 9a — 1ª ordem, Cr | idem | picos do 2º pulso 89,8/75,6/70,2 m × 90,0/76,0/70,9 m | **Validado** |
| R13 | Fig. 9b — 2ª ordem, Cr | idem | picos 89,8/87,3/85,4 m × 90,1/87,5/85,6 m | **Validado** |
| R14 | Fig. 10 — FVM-DVCM | `apply_dvcm` | Ns = 32: MedAE 0,28 m, Δt 0,36 ms, picos espúrios −7/−9 m; Ns = 256: Δt 0,88 ms, picos espúrios diferentes | **Parcial** / **Divergente** (picos) |
| R15 | Fig. 11 — MOC-DGCM | `moc_dgcm` | Ns = 32: MedAE 0,46 m, Δt médio 1,17 ms (colapsos 1,5 ms adiantados), pico espúrio +25 m; Ns = 256 oculto | **Divergente** (moderado) |
| R16 | Tabela 1 — estados iniciais | `params`, `initial_state` | cota inicial, Joukowsky e patamar de vapor ≤ 0,4 m (T2) | **Validado** |
| R17 | Afirmações do texto (conclusões 1–9) | `scripts/verify_claims.py` | seção 6 | 7 confirmadas, 2 parcialmente |

## 3. Digitalização dos gráficos

As figuras do artigo são imagens JPEG de 350 dpi embutidas no PDF, extraídas
sem reamostragem (`digitize/extract_figures.py`; o PDF não é distribuído).

1. **Calibração dos eixos** (`digitize/calibrate.py`): moldura detectada pelas
   linhas escuras mais longas; marcas de escala internas detectadas
   automaticamente; mapa linear pixel→dado ajustado por mínimos quadrados com as
   bordas e as marcas. Resíduo RMS: ≤ 0,15 m e ≤ 1e-4 s.
2. **Classificação por cor** (`digitize/extract_curves.py`): preto
   (experimento; curva Cr = 1 na Fig. 9), vermelho, azul, cinza; franjas cinzas
   de antisserrilhamento das linhas pretas descartadas; legendas e marcas de
   escala mascaradas.
3. **Por coluna de pixels**: extremos `H_min`, `H_max` e mediana do maior
   agrupamento (robusta a pixels espúrios). Frentes verticais aparecem como
   colunas com grande extensão vertical.
4. **Tempos de eventos**: centro da linha (média das colunas cuja extensão
   contém o nível) — elimina o viés de meia espessura de linha (≈ 0,75 ms),
   que inicialmente mascarava a concordância.
5. **Controle de qualidade**: sobreposição dos pontos digitalizados à figura
   original (`digitize/check_overlay.py`, inspeção visual de todas as 15
   figuras/painéis).

**Resolução** (1 px): Fig. 4: 1,18 ms × 0,128 m; Figs. 5, 6, 9, 10, 11:
0,50–0,53 ms × 0,36–0,39 m; Fig. 7: 0,50 ms × 0,51 m; Fig. 8: 0,64 ms × 0,33 m.
Espessura das linhas: 2–5 px. **Incerteza de digitalização** estimada:
±1–1,5 px em cota (0,4–0,6 m) e ±1 px em tempo (0,5 ms) para linhas
isoladas; séries parcialmente cobertas por outras (cobertura < 60 %) só são
comparadas nas partes visíveis, e as com cobertura < 20 % são classificadas
como não avaliáveis.

## 4. Métricas e tolerâncias

| Critério | Métrica | Tolerância | Justificativa |
|---|---|---|---|
| T_FLAT | mediana de \|ΔH\| nas colunas "planas" (extensão ≤ 4 px) | 3 px (0,38–1,53 m) | 1–1,5 px de digitalização + ~1 px de incerteza dos parâmetros não informados (T5) |
| T_PLAT | \|ΔH\| de patamares (inicial, Joukowsky, cavitação) | 3 px | idem |
| T_EVT1 | \|Δt\| dos 2 primeiros eventos | 1,5 ms (3 px) | 1 px de digitalização + Δt numérico (0,44 ms) + válvula |
| T_EVT | média de \|Δt\| de todos os eventos pareados | 2,5 ms | acumulação ao longo de 4–5 ciclos; T5 mostra ±1–2,6 ms para variações plausíveis de H_b, a, K |
| T_EVTN | fração dos eventos do artigo pareados (≤ 10 ms) | ≥ 75 % | impede que eventos não reproduzidos sejam ignorados pela média |
| T_PEAK | \|ΔH\| de picos de pulso | max(5 m; 10 %) | picos estreitos (3–10 px) e sensíveis; ver T6 (mal condicionamento) |

Erros pontuais (RMSE) de curvas com frentes quase verticais são dominados por
deslocamentos sub-milissegundo e por isso não são usados como critério (são
reportados em T1/T3). Nenhuma tolerância foi ajustada após ver os resultados
para mudar um estado (as tolerâncias acima foram definidas a partir da
resolução das figuras; as alterações posteriores da metodologia — pareamento
um-a-um de eventos e o critério T_EVTN, que torna a validação mais exigente —
estão na seção 9).

## 5. Resultados por figura

**Fig. 4 (Caso 0).** Com `C_-ap = 1`, 1ª e 2ª ordem coincidem com a solução
exata a 1,3e-11 m (Cr = 1 transporta exatamente). Para `C_-ap = 0,9` e 0,5 a
forma arredondada das transições é reproduzida (MedAE ≤ 0,05 m, Δt ≤ 0,31 ms).
Para `C_-ap = 0` a fase é reproduzida (Δt médio 0,59 ms), mas o artigo
amortece mais: extremos do último período 41,15/5,72 m (artigo) contra
42,24/4,87 m (reprodução). Investigação: o amortecimento depende apenas do
esquema de média (Eqs. 12–13) e do número de trechos; o do artigo equivale ao
desta implementação com Ns ≈ 27 em vez de 32. Variantes testadas sem sucesso:
cavidades nas fronteiras dos trechos (42,55/4,54 m), saída no estado de
contorno, Cr ligeiramente < 1 (1ª e 2ª ordem deixariam de coincidir, contra a
Fig. 4). Causa não identificada com a informação do artigo → **divergente**.

**Fig. 5 (α0).** α0 = 1e-7 validado (cota inicial 23,07 × 23,17 m, Joukowsky
66,56 × 66,68 m, cavitação −9,12 × −8,87 m, eventos 0,9 ms). O artigo mostra
α0 = 1e-8 e 1e-10 atrasando os eventos a partir do 3º pulso em 1,8 e 3,3–3,8 ms
em relação a α0 = 1e-7; aqui o atraso é 0,5 e 0,9 ms (mesmo sentido, menor
magnitude). A conclusão do artigo ("α0 ≤ 1e-7 resultados basicamente
idênticos") é confirmada qualitativamente; a magnitude das diferenças não.

**Fig. 6 (C_-ap, Ns).** `C_-ap` = 0,9; 0,8; 0,5: validados para Ns = 32 e 256.
`C_-ap = 1`: a dinâmica global é reproduzida (mesmos instantes de colapso), mas
os picos espúrios de alta frequência diferem (ex.: 3º pulso Ns = 32:
73,9 × 84,3 m). A seção 7 (T6) mostra que esses picos são mal condicionados:
perturbar H_r em 1e-13 altera a série em até 148 m (Ns = 256, C = 1).

**Fig. 7 (Caso 2, cavidade grande).** Patamar 166,90 × 166,89 m; cavitação
−9,12 × −9,46 m; colapso previsto com Δt médio de 2,2 ms; pico do 2º pulso
146,1 × 147,2 m → validado. A curva `C_-ap = 1` está oculta pela de 0,9 na
figura (cobertura 11 %).

**Fig. 8 (Caso 3, Ns = 256).** `C_-ap = 0,9`: Joukowsky 62,20 × 62,20 m, picos
dos pulsos 2–5 com |Δ| ≤ 0,83 m, eventos com Δt médio 0,20 ms → validado.
Este resultado depende da regularização do Método I (seção 8.5 da
documentação): sem ela o 1º colapso ocorre 11 ms depois do artigo
(143,3 × 132,0 ms).
`C_-ap = 1`: picos espúrios diferentes (até 24 m) — mal condicionado.

**Fig. 9 (Cr).** Reproduz o efeito central: com Cr < 1 a 1ª ordem é muito
dissipativa (pico do 2º pulso 89,8 → 75,6 → 70,2 m para Cr = 1; 0,5; 0,1;
artigo 90,0 → 76,0 → 70,9 m) enquanto a 2ª ordem quase não é
(89,8 → 87,3 → 85,4 m; artigo 90,1 → 87,5 → 85,6 m). Com Cr = 1 as duas ordens
são idênticas (diferença 0,0 m, também no artigo).

**Fig. 10 (FVM-DVCM).** Instantes reproduzidos (Ns = 32: Δt médio 0,36 ms);
picos espúrios diferem (3º e 4º pulsos 7–11 m abaixo).

**Fig. 11 (MOC-DGCM).** Forma e patamares reproduzidos (Joukowsky 66,54 ×
66,97 m; pico do 2º pulso 109,4 × 109,0 m); colapsos 1,5 ms adiantados em
relação ao MOC do artigo e picos espúrios maiores (3º pulso 107,2 × 82,4 m).
O atraso relativo do MOC em relação ao FVM (afirmado no artigo) é reproduzido:
+2,7 a +14 ms a partir do 2º colapso.

## 6. Verificação das afirmações do texto (`claims_python.json`)

| # | Afirmação do artigo | Resultado desta reprodução | Estado |
|---|---|---|---|
| 1 | `C_-ap < 1` introduz amortecimento artificial | amplitude final 41,75 (C = 1) ≥ 41,69 (0,5) > 37,37 m (0) | Confirmada |
| 2 | Golpe puro: `C_-ap = 1` exato; dissipação máxima com `C_-ap = 0` | erro 1,3e-11 m; ordem de dissipação reproduzida (magnitude: R04) | Confirmada (magnitude parcial) |
| 3 | `C_-ap = 1` gera picos irreais; ≈ 0,5 subestima picos; 0,9 recomendado | máx. após 0,25 s: 73,9/138,6 m (C = 1, Ns 32/256) × 62,2/78,4 m (0,9) × 59,5/74,9 m (0,5) | Confirmada |
| 4 | α0 ≤ 1e-7 praticamente idênticos | deslocamentos de 0,5–0,9 ms (artigo: 1,8–3,8 ms) | Confirmada qualitativamente |
| 5 | 2ª ordem precisa e robusta com Cr ≤ 1 | pico do 2º pulso cai só 5 % com Cr = 0,1 (1ª ordem: 22 %) | Confirmada |
| 6 | 1ª = 2ª ordem com Cr = 1; 1ª ordem dissipativa com Cr < 1 | diferença 0,0 m com Cr = 1 | Confirmada |
| 7 | FVM-DGCM com `C_-ap = 1` ≡ FVM-DVCM | mesmos instantes nos 3 primeiros eventos; a partir do 2º colapso 1,6–1,7 ms de diferença (Ns = 32) | Parcial |
| 8 | FVM-DGCM mais confiável que MOC-DGCM com malhas finas | MOC: picos espúrios de 104–107 m e atraso crescente dos eventos | Confirmada |
| 9 | Picos medidos de alta frequência não reproduzidos | MedAE plano vs. experimento 1,4–1,8 m, mas picos medidos não reproduzidos | Confirmada |

Comparação com o experimento (T3, informativa): erro mediano nas partes planas
1,4–1,8 m e erro médio de tempo 2,6–4,6 ms — semelhante ao que se vê nas
figuras do artigo. Com esta implementação, `C_-ap = 0,9` e `C_-ap = 1` têm
métricas globais equivalentes em relação ao experimento; a vantagem de 0,9
aparece na eliminação dos picos espúrios (afirmação 3), não nas cotas médias.

## 7. Testes de verificação

`python/tests/test_solver.py` (23 testes, `pytest`) e `matlab/run_tests.m`
(15 testes equivalentes) — todos passam:

* invariantes de Riemann (Eq. 6) e limitador MINMOD;
* Caso 0 com `C_-ap = 1`: igual à solução analítica (< 1e-9 m) em 1ª e 2ª ordem;
* monotonicidade do amortecimento com `C_-ap`;
* regime permanente com atrito preservado (deriva ≤ 1e-3 m, erro O(Δt²) do
  *splitting*);
* **conservação** do volume de líquido sem cavidades: erro relativo < 1e-12;
* **convergência** num pulso gaussiano suave (solução de d'Alembert):
  ordem observada 0,97 (1ª ordem) e 1,70 (2ª ordem; o MINMOD corta extremos);
* relações das cavidades: lei do gás (Eq. 11), conservação de ΣH nos
  ajustes (Eqs. 12–13), continuidade e lei do gás (Eqs. 15–17), colapso DVCM;
* lei de orifício da válvula (resíduo < 1e-11);
* MOC-DGCM: solução exata do Caso 0 (< 1e-3 m) e regime permanente;
* **consistência dimensional**: similaridade (L, a) → (2L, 2a) com mesmo aV0/g
  dá H(t) idêntico; invariância a translação do datum com cavitação (< 1e-7 m);
  definição de H_v.

**Sensibilidade (T5)** a parâmetros não informados: variações plausíveis
(f ± 20 %, H_b ± 0,3 m, K × 0,1…10, a ± 1 %) alteram as métricas contra o
artigo em até ~0,6 m e ~1,6 ms — da mesma ordem das diferenças residuais,
que portanto são compatíveis com a incerteza dos parâmetros. As escolhas de
interpretação alternativas (critério de colapso por pressão; *fallback* por
colapso) dão resultados equivalentes; **sem** a regularização do Método I o
caso Ns = 256 degrada (Caso 1: MedAE 52,8 m e só 2 de 5 eventos pareados;
Caso 3: 2 de 9 eventos pareados).

**Arredondamento (T6):** com Ns = 32 perturbações de 1e-13 produzem
diferenças < 1e-10 m; com Ns = 256 produzem até 29 m (C = 0,9) e 148–346 m
(C = 1) após ~0,27–0,33 s. Os picos de alta frequência dessas configurações
são, portanto, **mal condicionados**: nenhuma reprodução independente pode
igualá-los ponto a ponto — só as grandezas globais são comparáveis.

## 8. Validação cruzada MATLAB × Python

`matlab/cross_validate.m` compara as 37 séries: **máx |ΔH| = 0** em todas
(igualdade até a 9ª casa decimal gravada), inclusive nas configurações mal
condicionadas — o que exigiu usar exatamente as mesmas expressões nas duas
linguagens (ex.: `sin(3,2·π/180)` em vez de `sind(3,2)`; com `sind` a
diferença de 1 ulp na cota da válvula crescia até 505 m no Caso 3, C = 1,
ilustrando o item T6). `python -m scripts.compare_implementations` confirma
**37/37 estados de validação iguais** e diferença máxima 0 nas métricas.
Execução: Octave 8.4 (compatível com MATLAB; nenhum toolbox usado).

## 9. Divergências, limitações e decisões

1. **Parâmetros não informados** (f, ρ, p_v, p_bar, datum, lei/perda da
   válvula): deduzidos (documentação, seção 8); efeitos quantificados (T5).
   K da válvula inferido das curvas numéricas do próprio artigo, com
   verificação independente no Caso 2 (erro 0,05 ms).
2. **Regularização do Método I** (crescimento do gás limitado pela
   continuidade): adaptação necessária para os resultados com Ns = 256; muda
   em ≤ 1,3 ms os eventos tardios com Ns = 32. Pode ser desligada
   (`limit_gas_growth=False`).
3. **Caso 0, C = 0**: amortecimento do artigo ≈ 1,5× maior — não explicado.
4. **Sensibilidade a α0** menor que a do artigo (0,5–0,9 × 1,8–3,8 ms).
5. **Picos espúrios** (C = 1, DVCM, MOC, Ns = 256): mal condicionados (T6);
   amplitudes não reproduzíveis ponto a ponto.
6. **MOC-DGCM**: colapsos ≈ 1,5 ms adiantados em relação ao MOC do artigo
   (detalhes de ψ/válvula não informados).
7. **Séries ocultas** nas figuras (exata na Fig. 4a/b, α0 = 1e-10, C = 1 na
   Fig. 7, Ns = 256 nas Figs. 11): não avaliáveis.
8. **Metodologia**: durante a validação o pareamento de eventos passou de
   "vizinho mais próximo" para "um-a-um" (um evento espúrio da curva
   digitalizada da Fig. 6d, Ns = 256, era pareado duas vezes), e foi
   acrescentado o critério T_EVTN (≥ 75 % dos eventos pareados), mais
   exigente. Única mudança de estado: `fig06d_Ns256` DIVERGENTE → VALIDADO.
9. **Figuras MATLAB**: `make_figures.m` usa apenas funções gráficas padrão,
   mas não pôde ser executado neste ambiente (o Octave 8.4 sem monitor falha na
   renderização de fontes, mesmo com Xvfb). As figuras de
   `results/figures_matlab/` foram geradas a partir dos resultados MATLAB
   (`results/matlab/*.csv`) pelo script Python de figuras.

## 10. Conclusão

A implementação reproduz quantitativamente as curvas centrais do artigo
(FVM-DGCM com `C_-ap` entre 0,5 e 0,9 nos três casos experimentais, efeito do
número de Courant, golpe de aríete puro com `C_-ap ≥ 0,5`) dentro de tolerâncias
definidas pela resolução das figuras, e confirma 7 das 9 conclusões do artigo
integralmente e 2 parcialmente. As divergências remanescentes foram
investigadas e estão documentadas; nenhuma foi resolvida por ajuste arbitrário
de parâmetros. A versão MATLAB é equivalente à versão Python até a precisão de
gravação.
