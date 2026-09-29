# Reprodução computacional — Zhou et al. (2018), FVM-DGCM

Reprodução de **L. Zhou, H. Wang, A. Bergant, A. S. Tijsseling, D. Liu, S. Guo,
"Godunov-Type Solutions with Discrete Gas Cavity Model for Transient Cavitating
Pipe Flow", J. Hydraul. Eng. 144(5): 04018017, 2018.**

Golpe de aríete com cavitação vaporosa num sistema reservatório–tubo–válvula,
resolvido por volumes finitos de Godunov (1ª ordem e MUSCL-Hancock de 2ª ordem)
com cavidades de gás discretas (FVM-DGCM), além dos modelos de referência do
artigo (FVM-DVCM, MOC-DGCM com malha escalonada e solução exata do Caso 0).

* Implementação de referência: **Python/NumPy** (`python/`)
* Conversão integral: **MATLAB** (`matlab/`, testada em GNU Octave 8.4,
  sem toolboxes) — resultados idênticos aos do Python até 1e-9 m em todas
  as 37 séries.

## Documentação

| Documento | Conteúdo |
|---|---|
| [`docs/analise_do_artigo.md`](docs/analise_do_artigo.md) | modelo, equações, hipóteses, métodos numéricos, parâmetros com origem, informações ausentes e deduções, algoritmo, arquitetura |
| [`docs/relatorio_validacao.md`](docs/relatorio_validacao.md) | matriz de reprodução, digitalização, métricas e tolerâncias, resultados por figura, afirmações do artigo, testes, sensibilidade, validação cruzada, divergências e limitações |
| [`docs/tabelas_validacao.md`](docs/tabelas_validacao.md) | tabelas completas geradas automaticamente (T1–T8) |

## Resultado em uma tabela

| Figura | Conteúdo | Estado |
|---|---|---|
| 4a–c | Caso 0, C_-ap = 1; 0,9; 0,5 (1ª/2ª ordem, exata) | Validado |
| 4d | Caso 0, C_-ap = 0 | Divergente (amortecimento do artigo ≈ 1,5× maior) |
| 5 | efeito de α0 | α0 = 1e-7 validado; 1e-8 divergente (Δt 2,6 ms); 1e-10 oculto na figura |
| 6 | C_-ap e Ns, Caso 1 | C_-ap = 0,9; 0,8; 0,5 validados (Ns = 32 e 256); C_-ap = 1 parcial (picos espúrios) |
| 7 | Caso 2 | Validado (C_-ap = 0,9) |
| 8 | Caso 3, Ns = 256 | Validado (C_-ap = 0,9); C_-ap = 1 divergente (picos mal condicionados) |
| 9 | efeito de Cr, 1ª e 2ª ordem | Validado |
| 10 | FVM-DVCM | parcial (dinâmica ok, picos espúrios diferem) |
| 11 | MOC-DGCM | divergente moderado (colapsos 1,5 ms adiantados, picos espúrios) |

Detalhes e números: [`docs/relatorio_validacao.md`](docs/relatorio_validacao.md).

## Estrutura

```
zhou2018_fvm_dgcm/
├── python/
│   ├── fvmdgcm/        solver (params, godunov, boundaries, cavity, fvm_solver,
│   │                   moc_dgcm, exact, experiments, metrics)
│   ├── digitize/       extração e digitalização das figuras do PDF
│   ├── scripts/        run_all, validate, verify_claims, sensitivity,
│   │                   roundoff_sensitivity, calibrate_valve, make_figures,
│   │                   compare_implementations, report_tables
│   └── tests/          testes de verificação (pytest)
├── matlab/
│   ├── src/            funções (mesma arquitetura do Python)
│   ├── tests/          testes (run_tests.m)
│   ├── main.m          pipeline completo
│   ├── run_all.m, validate_all.m, cross_validate.m, make_figures.m, run_tests.m
├── data/digitized/     curvas digitalizadas do artigo (CSV) + calibração (JSON)
├── results/
│   ├── python/, matlab/          séries temporais de cada simulação (CSV)
│   ├── validation/               métricas, afirmações, sensibilidade, validação cruzada (JSON)
│   ├── figures/                  Figs. 4–11 reproduzidas (+ per_run/)
│   └── figures_matlab/           as mesmas figuras com os dados MATLAB
├── docs/
└── reproduce_all.sh
```

## Como executar

### Python (≥ 3.10)

```bash
cd python
pip install -r requirements.txt
python -m pytest -q tests            # 23 testes de verificação
python -m scripts.run_all            # todas as simulações (~10 s) -> results/python
python -m scripts.validate           # comparação com o artigo -> results/validation/metrics_python.json
python -m scripts.make_figures       # Figs. 4-11 -> results/figures
python -m scripts.verify_claims      # afirmações do texto
python -m scripts.sensitivity        # sensibilidade aos parâmetros não informados
python -m scripts.report_tables      # docs/tabelas_validacao.md
```

Uso direto:

```python
from fvmdgcm.params import CASES, Numerics
from fvmdgcm.fvm_solver import run_fvm
r = run_fvm(CASES["case1"], Numerics(Ns=32, Cr=1.0, C_ap=0.9, order=2, alpha0=1e-7))
# r.t [s], r.H_cellN [m] (cota "na válvula"), r.Vg_total [m^3] ...
case = CASES["case1"].with_(f=0.03, Hr=25.0)   # alterar parâmetros
```

### MATLAB (R2016b ou superior) ou GNU Octave (≥ 7)

```matlab
cd matlab
main                    % testes + simulações + validação + figuras + validação cruzada
% ou, passo a passo:
setup_paths; run_tests; run_all; validate_all; make_figures; cross_validate
% uso direto:
cs  = case_parameters('case1', 'f', 0.03);          % parâmetros (SI) modificáveis
num = numerics_default('Ns', 32, 'Cr', 1, 'C_ap', 0.9, 'order', 2);
r   = run_fvm(cs, num);  plot(r.t, r.H_cellN)
```

Dependências: nenhum toolbox. Funções usadas: `jsonencode`/`jsondecode`
(MATLAB ≥ R2016b, Octave ≥ 7), `dlmread`, gráficos básicos. No Octave sem
monitor as figuras exigem um ambiente gráfico funcional (ver relatório, §9).

### Tudo de uma vez

```bash
./reproduce_all.sh                    # usa os dados digitalizados já incluídos
./reproduce_all.sh caminho/Zhou_et_al._2018.pdf   # refaz também a digitalização
```

O PDF do artigo não é distribuído; as imagens extraídas dele e as sobreposições
de controle da digitalização são ignoradas pelo git.

## Parâmetros principais

Definidos em `python/fvmdgcm/params.py` e `matlab/src/case_parameters.m`,
`fluid_properties.m`, `numerics_default.m`, com unidades e origem
(Tabela 1, texto ou dedução). Os parâmetros **não informados pelo artigo**
(fator de atrito, propriedades da água, pressão barométrica, datum, perda da
válvula aberta, detalhes do algoritmo de cavidade) estão justificados na
seção 8 de [`docs/analise_do_artigo.md`](docs/analise_do_artigo.md).
