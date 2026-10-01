"""Turns the SQL results into plain-English findings.

Run:  python -m src.insights     (writes INSIGHTS.md)
"""
from pathlib import Path

from .db import ROOT, load_dataframe, make_connection, run_query


def build_insights(conn) -> list[str]:
    kpi = run_query(conn, "01_headline_kpis.sql").iloc[0]
    dept = run_query(conn, "02_attrition_by_department.sql")
    tenure = run_query(conn, "03_attrition_by_tenure_band.sql")
    wlb = run_query(conn, "04_work_life_balance.sql").set_index("work_life_balance")
    fields = run_query(conn, "05_education_field_risk.sql")
    income = run_query(conn, "06_income_band.sql")
    sat = run_query(conn, "07_job_satisfaction.sql").set_index("job_satisfaction")
    segments = run_query(conn, "08_high_risk_segments.sql")
    profile = run_query(conn, "09_leaver_vs_stayer_profile.sql").set_index("status")

    company_rate = kpi["attrition_rate_pct"]
    lines = [
        f"Company-wide attrition is {company_rate}% ({int(kpi['leavers'])} of {int(kpi['headcount'])} employees left)."
    ]

    top = dept.iloc[0]
    low = dept.iloc[-1]
    lines.append(
        f"{top['department']} has the highest department attrition at {top['attrition_rate_pct']}% "
        f"({int(top['leavers'])} of {int(top['headcount'])}); {low['department']} is lowest at {low['attrition_rate_pct']}%."
    )

    t = tenure.sort_values("attrition_rate_pct", ascending=False).iloc[0]
    lines.append(
        f"The {t['tenure_band']} tenure band leaves most often at {t['attrition_rate_pct']}% "
        f"({int(t['leavers'])} of {int(t['headcount'])})."
    )

    if 1 in wlb.index and 3 in wlb.index:
        lines.append(
            f"Attrition is {wlb.loc[1, 'attrition_rate_pct']}% for employees with the poorest work-life balance (1) "
            f"versus {wlb.loc[3, 'attrition_rate_pct']}% at score 3."
        )

    if not fields.empty:
        f = fields.iloc[0]
        lines.append(
            f"{f['education_field']} is the highest-risk education field at {f['attrition_rate_pct']}% "
            f"({int(f['leavers'])} of {int(f['headcount'])})."
        )

    i = income.sort_values("attrition_rate_pct", ascending=False).iloc[0]
    lines.append(f"The '{i['income_band']}' income band has the highest attrition at {i['attrition_rate_pct']}%.")

    if 1 in sat.index and 4 in sat.index:
        lines.append(
            f"Attrition is {sat.loc[1, 'attrition_rate_pct']}% at job satisfaction 1 "
            f"versus {sat.loc[4, 'attrition_rate_pct']}% at satisfaction 4."
        )

    if not segments.empty:
        s = segments.iloc[0]
        lines.append(
            f"Riskiest segment: {s['department']} with {s['tenure_band']} tenure, at "
            f"{s['attrition_rate_pct']}% ({s['times_company_avg']}x the company average)."
        )

    if {"Left", "Stayed"} <= set(profile.index):
        lines.append(
            f"People who left earned about {int(profile.loc['Left', 'avg_monthly_income'])} a month on average "
            f"versus {int(profile.loc['Stayed', 'avg_monthly_income'])} for those who stayed, "
            f"and had {profile.loc['Left', 'avg_tenure_yrs']} years of tenure versus {profile.loc['Stayed', 'avg_tenure_yrs']}."
        )
    return lines


def main() -> None:
    df, sample = load_dataframe()
    conn = make_connection(df)
    lines = build_insights(conn)
    header = "# Key insights\n\n"
    if sample:
        header += "> These numbers come from the synthetic SAMPLE dataset, not real findings.\n\n"
    out = Path(ROOT) / "INSIGHTS.md"
    out.write_text(header + "\n".join(f"- {line}" for line in lines) + "\n", encoding="utf-8")
    print(out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
