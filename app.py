import plotly.express as px
import streamlit as st

import itertools

import plotly.express as px
import streamlit as st

from src.db import load_dataframe, make_connection, read_sql_file, run_query
from src.insights import build_insights

st.set_page_config(page_title="HR Attrition & Workforce Analytics", page_icon="📊", layout="wide")


@st.cache_resource
def get_connection():
    df, using_sample = load_dataframe()
    return make_connection(df), using_sample


conn, using_sample = get_connection()
kpi = run_query(conn, "01_headline_kpis.sql").iloc[0]
company_rate = float(kpi["attrition_rate_pct"])

chart_ids = itertools.count()  # gives every chart its own unique key
def show_sql(name: str) -> None:
    with st.expander("View the SQL behind this"):
        st.code(read_sql_file(name), language="sql")


def rate_bar(df, category: str, title: str, horizontal: bool = False) -> None:
    df = df.copy()
    df[category] = df[category].astype(str)
    if horizontal:
        df = df.iloc[::-1]
        fig = px.bar(df, x="attrition_rate_pct", y=category, orientation="h", text="attrition_rate_pct", title=title)
        fig.add_vline(x=company_rate, line_dash="dash", annotation_text=f"Company {company_rate}%")
        fig.update_layout(xaxis_title="Attrition rate (%)", yaxis_title=None)
    else:
        fig = px.bar(df, x=category, y="attrition_rate_pct", text="attrition_rate_pct", title=title)
        fig.add_hline(y=company_rate, line_dash="dash", annotation_text=f"Company {company_rate}%")
        fig.update_layout(yaxis_title="Attrition rate (%)", xaxis_title=None)
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, key=f"chart_{next(chart_ids)}")

st.title("HR Attrition & Workforce Analytics")
st.caption("Where people leave, and what the data says about why.")

if using_sample:
    st.warning(
        "Showing a synthetic SAMPLE dataset. Add the real file at data/raw/hr_attrition.csv "
        "to see real findings."
    )

tab_overview, tab_where, tab_why, tab_segments, tab_insights = st.tabs(
    ["Overview", "Where people leave", "Why people leave", "High-risk segments", "Insights"]
)

with tab_overview:
    c1, c2, c3 = st.columns(3)
    c1.metric("Headcount", f"{int(kpi['headcount']):,}")
    c2.metric("Leavers", f"{int(kpi['leavers']):,}")
    c3.metric("Attrition rate", f"{kpi['attrition_rate_pct']}%")
    c4, c5, c6 = st.columns(3)
    c4.metric("Avg tenure (years)", kpi["avg_tenure_yrs"])
    c5.metric("Avg monthly income", f"{int(kpi['avg_monthly_income']):,}")
    c6.metric("Low work-life balance (1-2)", f"{kpi['low_work_life_balance_pct']}%")
    show_sql("01_headline_kpis.sql")

    left, right = st.columns(2)
    with left:
        rate_bar(run_query(conn, "02_attrition_by_department.sql"), "department", "Attrition by department")
    with right:
        rate_bar(run_query(conn, "03_attrition_by_tenure_band.sql"), "tenure_band", "Attrition by tenure")

with tab_where:
    st.subheader("By department")
    dept = run_query(conn, "02_attrition_by_department.sql")
    rate_bar(dept, "department", "Attrition by department")
    st.dataframe(dept, hide_index=True)
    show_sql("02_attrition_by_department.sql")

    st.subheader("By tenure")
    tenure = run_query(conn, "03_attrition_by_tenure_band.sql")
    rate_bar(tenure, "tenure_band", "Attrition by tenure band")
    st.dataframe(tenure, hide_index=True)
    show_sql("03_attrition_by_tenure_band.sql")

    st.subheader("By education field")
    fields = run_query(conn, "05_education_field_risk.sql")
    rate_bar(fields, "education_field", "Attrition by education field (groups with 20+ people)", horizontal=True)
    show_sql("05_education_field_risk.sql")

with tab_why:
    st.subheader("Work-life balance")
    rate_bar(run_query(conn, "04_work_life_balance.sql"), "work_life_balance", "Attrition by work-life balance (1 poor, 4 best)")
    show_sql("04_work_life_balance.sql")

    st.subheader("Income")
    rate_bar(run_query(conn, "06_income_band.sql"), "income_band", "Attrition by monthly income quartile")
    show_sql("06_income_band.sql")

    st.subheader("Job satisfaction")
    rate_bar(run_query(conn, "07_job_satisfaction.sql"), "job_satisfaction", "Attrition by job satisfaction (1 low, 4 high)")
    show_sql("07_job_satisfaction.sql")

    st.subheader("Who leaves vs who stays")
    st.dataframe(run_query(conn, "09_leaver_vs_stayer_profile.sql"), hide_index=True)
    show_sql("09_leaver_vs_stayer_profile.sql")

with tab_segments:
    st.subheader("Top 10 riskiest department and tenure combinations")
    st.write("Compared with the company average. Groups under 15 people are left out.")
    st.dataframe(run_query(conn, "08_high_risk_segments.sql"), hide_index=True)
    show_sql("08_high_risk_segments.sql")

with tab_insights:
    st.subheader("What the data shows")
    if using_sample:
        st.info("These come from the sample dataset, so they are not real findings.")
    for line in build_insights(conn):
        st.markdown(f"- {line}")
