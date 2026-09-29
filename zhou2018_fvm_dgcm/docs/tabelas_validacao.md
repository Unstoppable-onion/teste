# Tabelas de validação (geradas automaticamente)

Gerado por `python -m scripts.report_tables` a partir de `results/validation/*.json`.

## T1 – Comparação com as curvas numéricas do artigo (por série)

cov = fração do eixo do tempo em que a série é visível na figura; MedAE_plano = mediana de |ΔH| nas partes planas (tolerância = 3 px); Δt = erro de tempo dos eventos (cruzamento do nível do caso); status conforme `scripts/validate.py`.

| ID | Caso | Modelo/opções | cov | MedAE_plano (m) | tol (m) | Δt médio (ms) | Δt máx 2 primeiros (ms) | falhas | status |
|---|---|---|---|---|---|---|---|---|---|
| fig04a_o1 | case0 | DGCM o1 Ns=32 Cr=1.0 C=1.0 α0=1e-07 | 0.96 | 0.04 | 0.38 | 0.28 | 0.42 | – | **VALIDADO** |
| fig04a_o2 | case0 | DGCM o2 Ns=32 Cr=1.0 C=1.0 α0=1e-07 | 0.96 | 0.04 | 0.38 | 0.28 | 0.42 | – | **VALIDADO** |
| fig04a_exact | case0 | EXACT | 0.02 | 40.40 | 0.38 | 2.79 | 3.06 | T_FLAT, T_EVT1, T_EVT, T_EVTN | **NAO_AVALIAVEL** |
| fig04b_o1 | case0 | DGCM o1 Ns=32 Cr=1.0 C=0.9 α0=1e-07 | 0.94 | 0.05 | 0.38 | 0.21 | 0.26 | – | **VALIDADO** |
| fig04b_o2 | case0 | DGCM o2 Ns=32 Cr=1.0 C=0.9 α0=1e-07 | 0.94 | 0.05 | 0.38 | 0.21 | 0.26 | – | **VALIDADO** |
| fig04b_exact | case0 | EXACT | 0.13 | 0.13 | 0.38 | 0.35 | 0.70 | – | **NAO_AVALIAVEL** |
| fig04c_o1 | case0 | DGCM o1 Ns=32 Cr=1.0 C=0.5 α0=1e-07 | 0.97 | 0.04 | 0.38 | 0.31 | 0.45 | – | **VALIDADO** |
| fig04c_o2 | case0 | DGCM o2 Ns=32 Cr=1.0 C=0.5 α0=1e-07 | 0.97 | 0.04 | 0.38 | 0.31 | 0.45 | – | **VALIDADO** |
| fig04c_exact | case0 | EXACT | 0.40 | 0.13 | 0.38 | 0.38 | 1.04 | – | **VALIDADO** |
| fig04d_o1 | case0 | DGCM o1 Ns=32 Cr=1.0 C=0.0 α0=1e-07 | 0.97 | 0.40 | 0.38 | 0.59 | 0.92 | T_FLAT | **DIVERGENTE** |
| fig04d_o2 | case0 | DGCM o2 Ns=32 Cr=1.0 C=0.0 α0=1e-07 | 0.97 | 0.40 | 0.38 | 0.59 | 0.92 | T_FLAT | **DIVERGENTE** |
| fig04d_exact | case0 | EXACT | 0.86 | 0.13 | 0.38 | 0.32 | 1.12 | – | **VALIDADO** |
| fig05_a1e-7 | case1 | DGCM o2 Ns=32 Cr=1.0 C=0.9 α0=1e-07 | 1.00 | 0.48 | 1.09 | 0.90 | 0.40 | – | **VALIDADO** |
| fig05_a1e-8 | case1 | DGCM o2 Ns=32 Cr=1.0 C=0.9 α0=1e-08 | 0.40 | 1.94 | 1.09 | 2.64 | 2.63 | T_FLAT, T_EVT1, T_EVT | **DIVERGENTE** |
| fig05_a1e-10 | case1 | DGCM o2 Ns=32 Cr=1.0 C=0.9 α0=1e-10 | 0.07 | 3.96 | 1.09 | 3.94 | 4.15 | T_FLAT, T_EVT1, T_EVT | **NAO_AVALIAVEL** |
| fig06a_Ns32 | case1 | DGCM o2 Ns=32 Cr=1.0 C=1.0 α0=1e-07 | 1.00 | 0.17 | 1.16 | 1.19 | 0.38 | T_PEAK | **PARCIAL** |
| fig06a_Ns256 | case1 | DGCM o2 Ns=256 Cr=1.0 C=1.0 α0=1e-07 | 0.24 | 0.34 | 1.16 | 0.75 | 1.13 | T_PEAK | **PARCIAL** |
| fig06b_Ns32 | case1 | DGCM o2 Ns=32 Cr=1.0 C=0.9 α0=1e-07 | 1.00 | 0.24 | 1.16 | 1.02 | 0.85 | – | **VALIDADO** |
| fig06b_Ns256 | case1 | DGCM o2 Ns=256 Cr=1.0 C=0.9 α0=1e-07 | 0.36 | 0.71 | 1.16 | 0.52 | 0.99 | – | **VALIDADO** |
| fig06c_Ns32 | case1 | DGCM o2 Ns=32 Cr=1.0 C=0.8 α0=1e-07 | 1.00 | 0.31 | 1.16 | 0.47 | 0.71 | – | **VALIDADO** |
| fig06c_Ns256 | case1 | DGCM o2 Ns=256 Cr=1.0 C=0.8 α0=1e-07 | 0.38 | 0.31 | 1.16 | 0.74 | 0.88 | – | **VALIDADO** |
| fig06d_Ns32 | case1 | DGCM o2 Ns=32 Cr=1.0 C=0.5 α0=1e-07 | 1.00 | 0.59 | 1.16 | 0.68 | 0.70 | – | **VALIDADO** |
| fig06d_Ns256 | case1 | DGCM o2 Ns=256 Cr=1.0 C=0.5 α0=1e-07 | 0.39 | 0.37 | 1.16 | 0.66 | 0.66 | – | **VALIDADO** |
| fig07_Cap1.0 | case2 | DGCM o2 Ns=32 Cr=1.0 C=1.0 α0=1e-07 | 0.11 | 197.45 | 1.53 | 5.40 | 5.46 | T_FLAT, T_PLAT, T_EVT1, T_EVT | **NAO_AVALIAVEL** |
| fig07_Cap0.9 | case2 | DGCM o2 Ns=32 Cr=1.0 C=0.9 α0=1e-07 | 1.00 | 0.34 | 1.53 | 2.24 | 0.26 | – | **VALIDADO** |
| fig08_Cap1.0 | case3 | DGCM o2 Ns=256 Cr=1.0 C=1.0 α0=1e-07 | 0.30 | 2.70 | 0.99 | 1.27 | 2.32 | T_FLAT, T_PEAK, T_EVT1 | **DIVERGENTE** |
| fig08_Cap0.9 | case3 | DGCM o2 Ns=256 Cr=1.0 C=0.9 α0=1e-07 | 1.00 | 0.35 | 0.99 | 0.20 | 0.38 | – | **VALIDADO** |
| fig09a_Cr1.0 | case1 | DGCM o1 Ns=32 Cr=1.0 C=0.9 α0=1e-07 | 0.54 | 0.47 | 1.10 | 0.96 | 0.91 | – | **VALIDADO** |
| fig09a_Cr0.5 | case1 | DGCM o1 Ns=32 Cr=0.5 C=0.9 α0=1e-07 | 0.49 | 0.34 | 1.10 | – | – | – | **VALIDADO** |
| fig09a_Cr0.1 | case1 | DGCM o1 Ns=32 Cr=0.1 C=0.9 α0=1e-07 | 1.00 | 0.16 | 1.10 | 1.00 | 0.61 | – | **VALIDADO** |
| fig09b_Cr1.0 | case1 | DGCM o2 Ns=32 Cr=1.0 C=0.9 α0=1e-07 | 0.37 | 0.67 | 1.10 | 1.14 | 1.26 | – | **VALIDADO** |
| fig09b_Cr0.5 | case1 | DGCM o2 Ns=32 Cr=0.5 C=0.9 α0=1e-07 | 0.47 | 0.78 | 1.10 | 0.21 | 0.12 | – | **VALIDADO** |
| fig09b_Cr0.1 | case1 | DGCM o2 Ns=32 Cr=0.1 C=0.9 α0=1e-07 | 1.00 | 0.17 | 1.10 | 1.32 | 0.68 | – | **VALIDADO** |
| fig10_Ns32 | case1 | DVCM o2 Ns=32 Cr=1.0 C=1.0 α0=0.0 | 1.00 | 0.28 | 1.09 | 0.36 | 0.35 | T_PEAK | **PARCIAL** |
| fig10_Ns256 | case1 | DVCM o2 Ns=256 Cr=1.0 C=1.0 α0=0.0 | 0.28 | 0.37 | 1.09 | 0.88 | 1.76 | T_PEAK, T_EVT1 | **DIVERGENTE** |
| fig11_Ns32 | case1 | MOC-DGCM Ns=32 α0=1e-07 | 1.00 | 0.46 | 1.09 | 1.17 | 1.51 | T_PEAK, T_EVT1 | **DIVERGENTE** |
| fig11_Ns256 | case1 | MOC-DGCM Ns=256 α0=1e-07 | 0.14 | 3.12 | 1.09 | 1.92 | 1.99 | T_FLAT, T_PEAK, T_EVT1 | **NAO_AVALIAVEL** |

## T2 – Patamares e picos (artigo × reprodução)

| ID | grandeza | artigo (m) | reprodução (m) | Δ (m) |
|---|---|---|---|---|
| fig05_a1e-7 | H_initial | 23.17 | 23.07 | -0.11 |
| fig05_a1e-7 | H_joukowsky | 66.68 | 66.56 | -0.12 |
| fig05_a1e-7 | H_cavity | -8.87 | -9.12 | -0.25 |
| fig05_a1e-7 | peak_2nd_pulse | 89.26 | 89.81 | 0.55 |
| fig05_a1e-7 | peak_3rd_pulse | 65.23 | 62.23 | -3.00 |
| fig05_a1e-7 | peak_4th_pulse | 57.22 | 56.14 | -1.08 |
| fig05_a1e-8 | peak_2nd_pulse | 91.44 | 90.06 | -1.38 |
| fig05_a1e-8 | peak_3rd_pulse | 68.14 | 62.31 | -5.83 |
| fig05_a1e-8 | peak_4th_pulse | 58.31 | 57.35 | -0.96 |
| fig05_a1e-10 | peak_2nd_pulse | 87.07 | 90.11 | 3.03 |
| fig05_a1e-10 | peak_3rd_pulse | 71.05 | 65.94 | -5.11 |
| fig05_a1e-10 | peak_4th_pulse | 57.58 | 57.18 | -0.40 |
| fig06a_Ns32 | H_initial | 23.05 | 23.07 | 0.02 |
| fig06a_Ns32 | H_joukowsky | 66.61 | 66.54 | -0.07 |
| fig06a_Ns32 | H_cavity | -9.14 | -9.12 | 0.02 |
| fig06a_Ns32 | peak_2nd_pulse | 94.37 | 94.31 | -0.05 |
| fig06a_Ns32 | peak_3rd_pulse | 84.34 | 73.87 | -10.47 |
| fig06a_Ns32 | peak_4th_pulse | 65.45 | 59.81 | -5.64 |
| fig06a_Ns256 | peak_2nd_pulse | 101.69 | 101.96 | 0.27 |
| fig06a_Ns256 | peak_3rd_pulse | 93.98 | 90.23 | -3.75 |
| fig06a_Ns256 | peak_4th_pulse | 80.49 | 121.80 | 41.31 |
| fig06b_Ns32 | H_initial | 23.05 | 23.07 | 0.02 |
| fig06b_Ns32 | H_joukowsky | 66.61 | 66.56 | -0.05 |
| fig06b_Ns32 | H_cavity | -9.14 | -9.12 | 0.02 |
| fig06b_Ns32 | peak_2nd_pulse | 90.13 | 89.81 | -0.32 |
| fig06b_Ns32 | peak_3rd_pulse | 65.84 | 62.23 | -3.61 |
| fig06b_Ns32 | peak_4th_pulse | 57.36 | 56.14 | -1.22 |
| fig06b_Ns256 | peak_2nd_pulse | 100.15 | 99.93 | -0.22 |
| fig06b_Ns256 | peak_3rd_pulse | 78.18 | 78.42 | 0.25 |
| fig06b_Ns256 | peak_4th_pulse | 56.97 | 57.60 | 0.63 |
| fig06c_Ns32 | H_initial | 23.16 | 23.07 | -0.10 |
| fig06c_Ns32 | H_joukowsky | 66.49 | 66.56 | 0.07 |
| fig06c_Ns32 | H_cavity | -9.00 | -9.12 | -0.12 |
| fig06c_Ns32 | peak_2nd_pulse | 87.87 | 86.88 | -0.99 |
| fig06c_Ns32 | peak_3rd_pulse | 61.29 | 60.92 | -0.37 |
| fig06c_Ns32 | peak_4th_pulse | 55.90 | 55.70 | -0.20 |
| fig06c_Ns256 | peak_2nd_pulse | 99.04 | 98.88 | -0.16 |
| fig06c_Ns256 | peak_3rd_pulse | 76.70 | 78.35 | 1.66 |
| fig06c_Ns256 | peak_4th_pulse | 55.90 | 55.41 | -0.49 |
| fig06d_Ns32 | H_initial | 23.16 | 23.07 | -0.10 |
| fig06d_Ns32 | H_joukowsky | 66.49 | 66.54 | 0.05 |
| fig06d_Ns32 | H_cavity | -9.00 | -9.12 | -0.12 |
| fig06d_Ns32 | peak_2nd_pulse | 83.25 | 80.59 | -2.65 |
| fig06d_Ns32 | peak_3rd_pulse | 58.98 | 59.47 | 0.49 |
| fig06d_Ns32 | peak_4th_pulse | 55.52 | 55.12 | -0.39 |
| fig06d_Ns256 | peak_2nd_pulse | 97.88 | 97.96 | 0.08 |
| fig06d_Ns256 | peak_3rd_pulse | 74.39 | 74.88 | 0.49 |
| fig06d_Ns256 | peak_4th_pulse | 56.29 | 58.84 | 2.55 |
| fig07_Cap1.0 | H_cavity | 188.33 | -9.12 | -197.45 |
| fig07_Cap1.0 | peak_2nd_pulse | 148.77 | 146.46 | -2.31 |
| fig07_Cap0.9 | H_initial | 18.61 | 18.86 | 0.25 |
| fig07_Cap0.9 | H_joukowsky | 166.89 | 166.90 | 0.01 |
| fig07_Cap0.9 | H_cavity | -9.46 | -9.12 | 0.34 |
| fig07_Cap0.9 | peak_2nd_pulse | 147.24 | 146.09 | -1.15 |
| fig08_Cap1.0 | peak_2nd_pulse | 95.04 | 94.86 | -0.18 |
| fig08_Cap1.0 | peak_3rd_pulse | 91.41 | 85.77 | -5.64 |
| fig08_Cap1.0 | peak_4th_pulse | 75.57 | 82.40 | 6.83 |
| fig08_Cap1.0 | peak_5th_pulse | 55.44 | 79.19 | 23.75 |
| fig08_Cap0.9 | H_initial | 21.62 | 21.89 | 0.28 |
| fig08_Cap0.9 | H_joukowsky | 62.20 | 62.20 | -0.01 |
| fig08_Cap0.9 | H_cavity | -8.41 | -8.04 | 0.38 |
| fig08_Cap0.9 | peak_2nd_pulse | 94.38 | 93.54 | -0.83 |
| fig08_Cap0.9 | peak_3rd_pulse | 76.23 | 76.72 | 0.49 |
| fig08_Cap0.9 | peak_4th_pulse | 52.80 | 52.62 | -0.18 |
| fig08_Cap0.9 | peak_5th_pulse | 51.48 | 51.43 | -0.05 |
| fig09a_Cr1.0 | peak_2nd_pulse | 89.99 | 89.81 | -0.18 |
| fig09a_Cr1.0 | peak_3rd_pulse | 66.10 | 62.23 | -3.87 |
| fig09a_Cr1.0 | peak_4th_pulse | 57.28 | 56.14 | -1.14 |
| fig09a_Cr0.5 | H_joukowsky | 66.65 | 66.53 | -0.13 |
| fig09a_Cr0.5 | peak_2nd_pulse | 76.02 | 75.63 | -0.40 |
| fig09a_Cr0.5 | peak_3rd_pulse | 60.22 | 59.79 | -0.43 |
| fig09a_Cr0.5 | peak_4th_pulse | 55.44 | 55.01 | -0.43 |
| fig09a_Cr0.1 | H_initial | 23.11 | 23.07 | -0.04 |
| fig09a_Cr0.1 | H_joukowsky | 66.65 | 66.51 | -0.15 |
| fig09a_Cr0.1 | H_cavity | -9.05 | -9.12 | -0.07 |
| fig09a_Cr0.1 | peak_2nd_pulse | 70.88 | 70.19 | -0.69 |
| fig09a_Cr0.1 | peak_3rd_pulse | 59.12 | 59.19 | 0.07 |
| fig09a_Cr0.1 | peak_4th_pulse | 55.08 | 54.09 | -0.98 |
| fig09b_Cr1.0 | peak_2nd_pulse | 90.05 | 89.81 | -0.24 |
| fig09b_Cr1.0 | peak_3rd_pulse | 63.23 | 62.23 | -1.00 |
| fig09b_Cr1.0 | peak_4th_pulse | 55.51 | 56.14 | 0.63 |
| fig09b_Cr0.5 | peak_2nd_pulse | 87.47 | 87.34 | -0.13 |
| fig09b_Cr0.5 | peak_3rd_pulse | 65.43 | 66.84 | 1.41 |
| fig09b_Cr0.5 | peak_4th_pulse | 57.35 | 58.72 | 1.37 |
| fig09b_Cr0.1 | H_initial | 23.00 | 23.07 | 0.07 |
| fig09b_Cr0.1 | H_joukowsky | 66.53 | 66.53 | -0.01 |
| fig09b_Cr0.1 | H_cavity | -8.97 | -9.12 | -0.15 |
| fig09b_Cr0.1 | peak_2nd_pulse | 85.64 | 85.36 | -0.28 |
| fig09b_Cr0.1 | peak_3rd_pulse | 67.27 | 67.12 | -0.15 |
| fig09b_Cr0.1 | peak_4th_pulse | 59.55 | 58.96 | -0.59 |
| fig10_Ns32 | H_initial | 23.23 | 23.07 | -0.16 |
| fig10_Ns32 | H_joukowsky | 66.52 | 66.54 | 0.02 |
| fig10_Ns32 | H_cavity | -8.84 | -9.12 | -0.28 |
| fig10_Ns32 | peak_2nd_pulse | 94.60 | 95.35 | 0.75 |
| fig10_Ns32 | peak_3rd_pulse | 84.46 | 77.34 | -7.11 |
| fig10_Ns32 | peak_4th_pulse | 65.62 | 56.43 | -9.19 |
| fig10_Ns256 | peak_2nd_pulse | 101.85 | 102.20 | 0.35 |
| fig10_Ns256 | peak_3rd_pulse | 94.24 | 98.28 | 4.04 |
| fig10_Ns256 | peak_4th_pulse | 80.83 | 69.76 | -11.07 |
| fig11_Ns32 | H_initial | 23.16 | 23.07 | -0.09 |
| fig11_Ns32 | H_joukowsky | 66.97 | 66.54 | -0.43 |
| fig11_Ns32 | H_cavity | -8.83 | -9.11 | -0.28 |
| fig11_Ns32 | peak_2nd_pulse | 108.96 | 109.38 | 0.41 |
| fig11_Ns32 | peak_3rd_pulse | 82.42 | 107.25 | 24.82 |
| fig11_Ns32 | peak_4th_pulse | 65.34 | 77.58 | 12.24 |
| fig11_Ns256 | peak_2nd_pulse | 110.05 | 109.53 | -0.52 |
| fig11_Ns256 | peak_3rd_pulse | 102.42 | 104.36 | 1.94 |
| fig11_Ns256 | peak_4th_pulse | 72.61 | 88.44 | 15.83 |

## T3 – Comparação com o experimento digitalizado (informativa)

| ID | MedAE_plano (m) | RMSE total (m) | Δt médio (ms) | eventos pareados |
|---|---|---|---|---|
| fig05_a1e-7 | 1.71 | 10.84 | 4.47 | 7/7 |
| fig05_a1e-8 | 1.71 | 10.96 | 4.19 | 7/7 |
| fig05_a1e-10 | 1.71 | 11.02 | 3.97 | 7/7 |
| fig06a_Ns32 | 1.52 | 9.74 | 3.55 | 7/8 |
| fig06a_Ns256 | 1.51 | 13.43 | 3.00 | 8/8 |
| fig06b_Ns32 | 1.52 | 10.30 | 4.24 | 7/7 |
| fig06b_Ns256 | 1.51 | 10.87 | 2.62 | 7/7 |
| fig06c_Ns32 | 1.66 | 11.06 | 4.22 | 7/7 |
| fig06c_Ns256 | 1.65 | 11.12 | 2.81 | 7/7 |
| fig06d_Ns32 | 1.66 | 11.14 | 4.24 | 7/7 |
| fig06d_Ns256 | 1.65 | 11.35 | 2.63 | 7/7 |
| fig07_Cap1.0 | 1.76 | 54.84 | 1.17 | 4/10 |
| fig07_Cap0.9 | 1.76 | 54.90 | 1.61 | 4/10 |
| fig08_Cap1.0 | 1.41 | 14.06 | 3.38 | 8/8 |
| fig08_Cap0.9 | 1.43 | 12.65 | 4.64 | 8/8 |
| fig10_Ns32 | 1.55 | 14.24 | 2.69 | 7/10 |
| fig10_Ns256 | 1.54 | 14.66 | 2.82 | 7/10 |
| fig11_Ns32 | 1.55 | 19.17 | 4.29 | 4/7 |
| fig11_Ns256 | 1.55 | 19.02 | 4.95 | 5/7 |

## T4 – Caso 0: erro frente à solução exata e extremos do último período

| ID | máx |H − H_exata| longe das frentes (m) | máx/mín reprodução (m) | máx/mín artigo (m) |
|---|---|---|---|
| fig04a_o1 | 1.3e-11 | 44.29 / 2.53 | 44.52 / 2.28 |
| fig04a_o2 | 1.3e-11 | 44.29 / 2.53 | 44.52 / 2.28 |
| fig04b_o1 | 1.4e+01 | 44.29 / 2.53 | 44.52 / 2.34 |
| fig04b_o2 | 1.4e+01 | 44.29 / 2.53 | 44.52 / 2.34 |
| fig04c_o1 | 1.8e+01 | 44.26 / 2.57 | 44.35 / 2.33 |
| fig04c_o2 | 1.8e+01 | 44.26 / 2.57 | 44.35 / 2.33 |
| fig04d_o1 | 1.9e+01 | 42.24 / 4.87 | 41.15 / 5.72 |
| fig04d_o2 | 1.9e+01 | 42.24 / 4.87 | 41.15 / 5.72 |

## T5 – Sensibilidade aos parâmetros não informados / escolhas de interpretação

Métricas contra as curvas do artigo: MedAE_plano (m) / Δt médio (ms) [eventos pareados/eventos do artigo].

| Variante | Caso 1 Ns=32 (Fig. 6b) | Caso 1 Ns=256 (Fig. 6b) | Caso 3 Ns=256 (Fig. 8) |
|---|---|---|---|
| baseline | 0.24 / 1.02 [7/7] | 0.71 / 0.52 [5/5] | 0.35 / 0.20 [9/9] |
| f x 0.8 | 0.25 / 1.03 [7/7] | 0.55 / 0.85 [5/5] | 0.35 / 0.40 [9/9] |
| f x 1.2 | 0.27 / 1.02 [7/7] | 0.62 / 0.44 [5/5] | 0.38 / 0.28 [9/9] |
| Hb - 0.3 m (vapour head +0.3 m) | 0.21 / 0.36 [7/7] | 0.35 / 1.28 [5/5] | 0.68 / 1.05 [9/9] |
| Hb + 0.3 m (vapour head -0.3 m) | 0.80 / 2.04 [7/7] | 1.14 / 0.61 [5/5] | 0.29 / 2.44 [9/9] |
| K_valve x 0.1 | 0.16 / 0.41 [7/7] | 0.68 / 1.07 [5/5] | 0.33 / 0.64 [9/9] |
| K_valve x 10 | 0.60 / 2.21 [7/7] | 1.08 / 1.82 [5/5] | 0.36 / 1.54 [9/9] |
| a - 1 % | 0.49 / 0.66 [7/7] | 1.11 / 0.88 [5/5] | 0.38 / 1.52 [9/9] |
| a + 1 % | 0.19 / 2.60 [7/7] | 0.35 / 1.64 [5/5] | 0.44 / 2.06 [9/9] |
| no gas-growth limit (literal Eq. 11) | 0.37 / 0.36 [7/7] | 52.78 / 7.74 [2/5] | 0.68 / 1.31 [2/9] |
| collapse criterion 'pressure' | 0.27 / 1.15 [7/7] | 0.61 / 0.44 [5/5] | 0.35 / 0.20 [9/9] |
| fallback 'collapse' | 0.24 / 1.02 [7/7] | 0.68 / 0.53 [5/5] | 0.35 / 0.20 [9/9] |
| output = boundary state U_N+1/2 | 0.46 / 1.22 [7/7] | 0.70 / 0.51 [5/5] | 0.19 / 0.21 [9/9] |

## T6 – Sensibilidade a perturbações de arredondamento (Hr × (1 + 1e-13))

| Configuração | máx |ΔH| (m) | RMS ΔH (m) | 1º instante com |ΔH| > 1 mm (s) |
|---|---|---|---|
| case1_Ns32_Cap1.0 | 4.21e-11 | 5.05e-12 | – |
| case1_Ns32_Cap0.9 | 4.86e-11 | 6.87e-12 | – |
| case1_Ns256_Cap1.0 | 1.48e+02 | 6.48e+00 | 0.331 |
| case1_Ns256_Cap0.9 | 2.92e+01 | 9.96e-01 | 0.265 |
| case3_Ns256_Cap1.0 | 3.46e+02 | 1.63e+01 | 0.316 |
| case3_Ns256_Cap0.9 | 8.73e-01 | 4.22e-02 | 0.368 |

## T7 – Validação cruzada MATLAB/Octave × Python (séries completas)

| ID | amostras | máx |ΔH| (m) | RMS ΔH (m) | máx |Δt| eventos (ms) |
|---|---|---|---|---|
| fig04a_o1 | 2277 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig04a_o2 | 2277 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig04a_exact | 20001 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig04b_o1 | 2277 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig04b_o2 | 2277 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig04b_exact | 20001 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig04c_o1 | 2277 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig04c_o2 | 2277 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig04c_exact | 20001 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig04d_o1 | 2277 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig04d_o2 | 2277 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig04d_exact | 20001 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig05_a1e-7 | 1025 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig05_a1e-8 | 1025 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig05_a1e-10 | 1025 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig06a_Ns32 | 1025 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig06a_Ns256 | 8193 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig06b_Ns32 | 1025 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig06b_Ns256 | 8193 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig06c_Ns32 | 1025 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig06c_Ns256 | 8193 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig06d_Ns32 | 1025 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig06d_Ns256 | 8193 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig07_Cap1.0 | 1025 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig07_Cap0.9 | 1025 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig08_Cap1.0 | 10349 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig08_Cap0.9 | 10349 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig09a_Cr1.0 | 1025 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig09a_Cr0.5 | 2049 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig09a_Cr0.1 | 10241 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig09b_Cr1.0 | 1025 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig09b_Cr0.5 | 2049 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig09b_Cr0.1 | 10241 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig10_Ns32 | 1025 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig10_Ns256 | 8193 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig11_Ns32 | 257 | 0.0e+00 | 0.0e+00 | 0.0e+00 |
| fig11_Ns256 | 2049 | 0.0e+00 | 0.0e+00 | 0.0e+00 |

## T8 – Inferência da perda de carga da válvula aberta

| Caso | t50 artigo (ms) | K | t50 modelo (ms) | observação |
|---|---|---|---|---|
| case1 | 22.11 | 2.55 | 22.11 | ajustado |
| case2 | 23.81 | 2.55 | 23.86 | previsão independente (erro 0.05 ms) |
| case3 | 8.76 | 18.93 | 8.76 | ajustado |
