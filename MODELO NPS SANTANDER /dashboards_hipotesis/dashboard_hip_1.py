import streamlit as st
import pandas as pd
from data_processing_copy import data_processing
import plotly.express as px


#-- Function to extract clean DF --
@st.cache_data
def get_gpd_data(): 

    return data_processing()

df = get_gpd_data()

#Titles
st.set_page_config(page_title="Dashboard H1", layout="wide")

st.markdown("""
# Hypothesis — Digital Channel vs. Satisfaction
### *"Customers whose main channel is the mobile app report higher CES and NPS than those who use ATMs or physical branches."*
""")


#-- Filters --
st.sidebar.header("Filters")

#By institution
instituciones = ["All"] + sorted(df["institucion"].dropna().unique().tolist())
institucion_sel = st.sidebar.multiselect(
    "Institution",
    options=instituciones,
)

#By customer seniority
antiguedades = sorted(df["antiguedad"].dropna().unique().tolist())
antiguedad_sel = st.sidebar.multiselect(
    "Customer seniority at institution",
    options=antiguedades,
)

#By customer age
edades = sorted(df["edad"].dropna().unique().tolist())
edad_sel = st.sidebar.multiselect(
    "Customer age",
    options=edades,
)


#Apply filters
df_filtrado = df.copy()

if institucion_sel:
    df_filtrado = df_filtrado[df_filtrado["institucion"].isin(institucion_sel)]

if antiguedad_sel:
    df_filtrado = df_filtrado[df_filtrado["antiguedad"].isin(antiguedad_sel)]

if edad_sel:
    df_filtrado = df_filtrado[df_filtrado["edad"].isin(edad_sel)]


#-- Key metrics / KPIs --
st.markdown("## Key Metrics")

df_app = df_filtrado[df_filtrado["canal_principal"] == "app móvil"]
df_otros = df_filtrado[df_filtrado["canal_principal"] != "app móvil"]

pct_promotores_app = (
    (df_app["nps_categoria"] == "Promotor (9-10)").sum()
    / len(df_app) * 100
    if len(df_app) > 0 else 0
)

pct_promotores_otros = (
    (df_otros["nps_categoria"] == "Promotor (9-10)").sum()
    / len(df_otros) * 100
    if len(df_otros) > 0 else 0
)

ces_app = df_app["ces"].mean() if len(df_app) > 0 else 0
ces_otros = df_otros["ces"].mean() if len(df_otros) > 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric(
    label="% Promoters — Mobile app",
    value=f"{pct_promotores_app:.1f}%",
    delta=f"{pct_promotores_app - pct_promotores_otros:.1f}% vs other channels"
)

col2.metric(
    label="Average CES — Mobile app",
    value=f"{ces_app:.2f}",
    delta=f"{ces_app - ces_otros:.2f} vs other channels"
)

col3.metric(
    label="Total responses",
    value=f"{len(df_filtrado):,}"
)

st.divider()

col1, col2 = st.columns(2)

with col1:

    #-- Chart 1 - Distribution --
    st.markdown("## NPS Distribution by Main Channel")

    #Calculate percentages
    nps_canal = (
        df_filtrado.groupby(["canal_principal", "nps_categoria"])
        .size()
        .reset_index(name="count")
    )

    nps_canal["pct"] = nps_canal.groupby("canal_principal")["count"].transform(
        lambda x: x / x.sum() * 100 #Percentage of each NPS category per channel
    )

    #Category order (NPS)
    orden_nps = ["Promotor (9-10)", "Pasivo (7-8)", "Detractor (0-6)"]
    colores_nps = {
        "Promotor (9-10)": "#2ecc71",
        "Pasivo (7-8)": "#f39c12",
        "Detractor (0-6)": "#e74c3c"
    }

    #Plot
    fig_bar = px.bar(
        nps_canal,
        x="canal_principal",
        y="pct",
        color="nps_categoria",
        category_orders={"nps_categoria": orden_nps},
        color_discrete_map=colores_nps,
        labels={"pct": "% Customers", "canal_principal": "Main Channel", "nps_categoria": "NPS"},
        text_auto=".1f"
    )

    fig_bar.update_layout(
        barmode="stack",
        legend_title="NPS Category",
        yaxis_ticksuffix="%",
        height=450
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

with col2:

    #-- Chart 2 - Heatmap --
    st.markdown("## % Promoters by Channel and Month")

    df_filtrado["es_promotor"] = df_filtrado["nps_categoria"] == "Promotor (9-10)"

    heatmap_data = (
        df_filtrado.groupby(["canal_principal", "mes"])["es_promotor"]
        .mean()
        .reset_index(name="pct_promotores")
    )
    heatmap_data["pct_promotores"] = heatmap_data["pct_promotores"] * 100

    heatmap_pivot = heatmap_data.pivot(index="canal_principal", columns="mes", values="pct_promotores")

    fig_heat = px.imshow(
        heatmap_pivot,
        color_continuous_scale="RdYlGn",
        labels={"color": "% Promoters", "x": "Month", "y": "Main Channel"},
        text_auto=".1f",
        aspect="auto"
    )

    fig_heat.update_layout(height=450)

    st.plotly_chart(fig_heat, use_container_width=True)
    st.divider()

#-- Chart 3 - CES by channel --
st.markdown("## Average CES by Main Channel")

ces_canal = (
    df_filtrado.groupby("canal_principal")["ces"]
    .mean()
    .reset_index(name="ces_promedio")
    .sort_values("ces_promedio", ascending=True)
)

ces_global = df_filtrado["ces"].mean()

fig_ces = px.bar(
    ces_canal,
    x="ces_promedio",
    y="canal_principal",
    orientation="h",
    labels={"ces_promedio": "Average CES", "canal_principal": "Main Channel"},
    color="ces_promedio",
    color_continuous_scale="RdYlGn",
    text_auto=".2f"
)

fig_ces.add_vline(
    x=ces_global,
    line_dash="dash",
    line_color="white",
    annotation_text=f"Overall average: {ces_global:.2f}",
    annotation_position="top right"
)

fig_ces.update_layout(
    coloraxis_showscale=False,
    height=450
)

st.plotly_chart(fig_ces, use_container_width=True)
st.divider()

st.write("""
### Conclusions

*H3 Partially Confirmed*

The mobile app *does outperform* ATMs and physical branches on both indicators (CES and % Promoters),
which supports the hypothesis in its direct comparison. However, **it is not the channel with the highest
overall satisfaction** — Phone (call center) leads in CES and physical branches are comparable in NPS.

""")