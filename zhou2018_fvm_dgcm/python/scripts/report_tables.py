"""Generate the Markdown tables of the validation report from the JSON
results (docs/tabelas_validacao.md).  Re-run after any change:

    python -m scripts.report_tables
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VAL = ROOT / "results" / "validation"


def f(x, nd=2):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "–"
    return f"{x:.{nd}f}"


def main():
    m = json.load(open(VAL / "metrics_python.json"))
    L = ["# Tabelas de validação (geradas automaticamente)", "",
         "Gerado por `python -m scripts.report_tables` a partir de `results/validation/*.json`.", "",
         "## T1 – Comparação com as curvas numéricas do artigo (por série)", "",
         "cov = fração do eixo do tempo em que a série é visível na figura; "
         "MedAE_plano = mediana de |ΔH| nas partes planas (tolerância = 3 px); "
         "Δt = erro de tempo dos eventos (cruzamento do nível do caso); "
         "status conforme `scripts/validate.py`.", "",
         "| ID | Caso | Modelo/opções | cov | MedAE_plano (m) | tol (m) | Δt médio (ms) | Δt máx 2 primeiros (ms) | falhas | status |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for rid, e in m.items():
        a = e["vs_paper"]
        ev = a.get("events", {})
        num = e["num"]
        opts = e["solver"].upper()
        if e["solver"] == "fvm":
            opts = (f"{num.get('model', 'DGCM')} o{num.get('order')} Ns={num.get('Ns')} "
                    f"Cr={num.get('Cr')} C={num.get('C_ap')} α0={num.get('alpha0')}")
        elif e["solver"] == "moc":
            opts = f"MOC-DGCM Ns={num.get('Ns')} α0={num.get('alpha0')}"
        fails = ", ".join(k for k, v in a["criteria"].items() if not v) or "–"
        L.append(f"| {rid} | {e['case']} | {opts} | {a['coverage']:.2f} | "
                 f"{f(a['pointwise']['flat']['medae'])} | {f(a['flat_medae_tol'])} | "
                 f"{f(ev.get('mean_abs_ms'))} | {f(ev.get('first2_max_abs_ms'))} | {fails} | **{a['status']}** |")
    L += ["", "## T2 – Patamares e picos (artigo × reprodução)", "",
          "| ID | grandeza | artigo (m) | reprodução (m) | Δ (m) |", "|---|---|---|---|---|"]
    for rid, e in m.items():
        a = e["vs_paper"]
        for n, p in list(a.get("plateaus", {}).items()) + list(a.get("peaks", {}).items()):
            if p["paper"] is None or (isinstance(p["paper"], float) and math.isnan(p["paper"])):
                continue
            L.append(f"| {rid} | {n} | {f(p['paper'])} | {f(p['sim'])} | {f(p['sim'] - p['paper'])} |")
    L += ["", "## T3 – Comparação com o experimento digitalizado (informativa)", "",
          "| ID | MedAE_plano (m) | RMSE total (m) | Δt médio (ms) | eventos pareados |",
          "|---|---|---|---|---|"]
    for rid, e in m.items():
        if "vs_experiment" not in e:
            continue
        a = e["vs_experiment"]
        ev = a.get("events", {})
        L.append(f"| {rid} | {f(a['pointwise']['flat']['medae'])} | {f(a['pointwise']['all']['rmse'])} | "
                 f"{f(ev.get('mean_abs_ms'))} | {ev.get('n_paired', 0)}/{ev.get('n_paper', 0)} |")
    L += ["", "## T4 – Caso 0: erro frente à solução exata e extremos do último período", "",
          "| ID | máx |H − H_exata| longe das frentes (m) | máx/mín reprodução (m) | máx/mín artigo (m) |",
          "|---|---|---|---|"]
    for rid, e in m.items():
        if "vs_exact" in e:
            lp = e["late_period"]
            L.append(f"| {rid} | {e['vs_exact']['max_abs_err_away_from_fronts']:.1e} | "
                     f"{f(lp['sim_max'])} / {f(lp['sim_min'])} | {f(lp['paper_max'])} / {f(lp['paper_min'])} |")
    # sensitivity
    s = json.load(open(VAL / "sensitivity_python.json"))
    L += ["", "## T5 – Sensibilidade aos parâmetros não informados / escolhas de interpretação", "",
          "Métricas contra as curvas do artigo: MedAE_plano (m) / Δt médio (ms) "
          "[eventos pareados/eventos do artigo].", "",
          "| Variante | Caso 1 Ns=32 (Fig. 6b) | Caso 1 Ns=256 (Fig. 6b) | Caso 3 Ns=256 (Fig. 8) |",
          "|---|---|---|---|"]
    for name, r in s.items():
        cells = [f"{f(v['flat_medae_m'])} / {f(v['event_mean_abs_ms'])} "
                 f"[{v['n_events']}/{v['n_paper_events']}]" for v in r.values()]
        L.append(f"| {name} | " + " | ".join(cells) + " |")
    ro = json.load(open(VAL / "roundoff_sensitivity.json"))
    L += ["", "## T6 – Sensibilidade a perturbações de arredondamento (Hr × (1 + 1e-13))", "",
          "| Configuração | máx |ΔH| (m) | RMS ΔH (m) | 1º instante com |ΔH| > 1 mm (s) |", "|---|---|---|---|"]
    for k, v in ro.items():
        L.append(f"| {k} | {v['max_abs_dH']:.2e} | {v['rms_dH']:.2e} | {f(v['first_time_dH_gt_1mm'], 3)} |")
    cv = json.load(open(VAL / "cross_validation.json"))
    L += ["", "## T7 – Validação cruzada MATLAB/Octave × Python (séries completas)", "",
          "| ID | amostras | máx |ΔH| (m) | RMS ΔH (m) | máx |Δt| eventos (ms) |", "|---|---|---|---|---|"]
    for c in cv:
        L.append(f"| {c['id']} | {c['n']} | {c['max_abs_dH']:.1e} | {c['rms_dH']:.1e} | {c['max_evt_dt_ms']:.1e} |")
    cal = json.load(open(ROOT / "results" / "valve_calibration.json"))
    L += ["", "## T8 – Inferência da perda de carga da válvula aberta", "",
          "| Caso | t50 artigo (ms) | K | t50 modelo (ms) | observação |", "|---|---|---|---|---|"]
    for k, v in cal.items():
        K = v.get("K_fit", v.get("K_used"))
        tm = v.get("model_t50", v.get("model_t50_predicted"))
        obs = "ajustado" if "K_fit" in v else f"previsão independente (erro {v['error_ms']:.2f} ms)"
        L.append(f"| {k} | {1e3 * v['paper_t50_mean']:.2f} | {K:.2f} | {1e3 * tm:.2f} | {obs} |")
    out = ROOT / "docs" / "tabelas_validacao.md"
    out.write_text("\n".join(L) + "\n")
    print("written", out)


if __name__ == "__main__":
    main()
