"""ESG Data Explorer — Dashboard interactivo de sostenibilidad global.

Práctica 5 · Unidad 5 · Visualización de datos
"""
import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import load, download

st.set_page_config(
    page_title="ESG Data Explorer",
    page_icon="🌍",
    layout="wide",
)


@st.cache_data(show_spinner="Cargando indicadores del Banco Mundial...")
def get_data() -> pd.DataFrame:
    df = load()
    df = df.dropna(subset=["gdp_usd", "co2_mt"])
    df["co2_per_capita"] = df["co2_mt"] * 1_000_000 / df["population"]
    df["gdp_per_capita"] = df["gdp_usd"] / df["population"]
    return df


# --- Sidebar ---------------------------------------------------------------
st.sidebar.title("🔎 Filtros")

if st.sidebar.button("🔄 Re-descargar datos"):
    download()
    st.cache_data.clear()
    st.rerun()

df = get_data()

year_min, year_max = int(df["year"].min()), int(df["year"].max())
year_range = st.sidebar.slider(
    "Rango de años", year_min, year_max, (year_min, year_max)
)

continents = sorted(df["continent"].dropna().unique())
sel_continents = st.sidebar.multiselect(
    "Continentes", continents, default=continents
)

countries_pool = sorted(
    df[df["continent"].isin(sel_continents)]["country"].unique()
)
sel_countries = st.sidebar.multiselect(
    "Países (opcional, vacío = todos)", countries_pool
)

# --- Filtro reactivo -------------------------------------------------------
mask = (
    df["year"].between(*year_range)
    & df["continent"].isin(sel_continents)
)
if sel_countries:
    mask &= df["country"].isin(sel_countries)
fdf = df[mask].copy()

# --- Header ----------------------------------------------------------------
st.title("🌍 ESG Data Explorer")
st.caption(
    "Tablero de sostenibilidad global · PIB vs emisiones de CO₂ · "
    "Fuente: World Bank Open Data"
)

if fdf.empty:
    st.warning("Sin datos para los filtros seleccionados.")
    st.stop()

# --- KPIs ------------------------------------------------------------------
latest_year = int(fdf["year"].max())
prev_year = latest_year - 1
cur = fdf[fdf["year"] == latest_year]
prv = fdf[fdf["year"] == prev_year]

avg_co2 = cur["co2_per_capita"].mean()
avg_gdp = cur["gdp_per_capita"].mean()
total_co2_mt = cur["co2_mt"].sum()
growth = (
    ((cur["co2_mt"].sum() - prv["co2_mt"].sum()) / prv["co2_mt"].sum() * 100)
    if not prv.empty and prv["co2_mt"].sum() else 0
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Países filtrados", fdf["country"].nunique())
c2.metric(f"CO₂ per cápita ({latest_year})", f"{avg_co2:,.2f} t")
c3.metric(f"PIB per cápita ({latest_year})", f"${avg_gdp:,.0f}")
c4.metric(
    f"Δ CO₂ total {prev_year}→{latest_year}",
    f"{total_co2_mt:,.0f} Mt",
    f"{growth:+.2f}%",
)

st.divider()

# --- Gráficos --------------------------------------------------------------
left, right = st.columns([3, 2])

with left:
    st.subheader("Evolución PIB vs CO₂ (animado)")
    anim_df = fdf.dropna(subset=["gdp_per_capita", "co2_per_capita", "population"])
    fig_anim = px.scatter(
        anim_df,
        x="gdp_per_capita",
        y="co2_per_capita",
        animation_frame="year",
        animation_group="country",
        size="population",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=55,
        labels={
            "gdp_per_capita": "PIB per cápita (USD, log)",
            "co2_per_capita": "CO₂ per cápita (toneladas)",
        },
    )
    fig_anim.update_layout(height=520, legend_title_text="Continente")
    st.plotly_chart(fig_anim, use_container_width=True)

with right:
    st.subheader(f"Mapa de CO₂ per cápita · {latest_year}")
    map_df = fdf[fdf["year"] == latest_year]
    fig_map = px.choropleth(
        map_df,
        locations="iso3",
        color="co2_per_capita",
        hover_name="country",
        color_continuous_scale="Reds",
        labels={"co2_per_capita": "CO₂ t/hab"},
    )
    fig_map.update_layout(
        height=520,
        margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(showframe=False, showcoastlines=True),
    )
    st.plotly_chart(fig_map, use_container_width=True)

# --- Tendencia por país ----------------------------------------------------
st.subheader("Tendencia temporal por continente")
trend = (
    fdf.groupby(["year", "continent"], as_index=False)
    .agg(co2_total=("co2_mt", "sum"), gdp_total=("gdp_usd", "sum"))
)
fig_trend = px.line(
    trend, x="year", y="co2_total", color="continent",
    labels={"co2_total": "Emisiones CO₂ (Mt)", "year": "Año"},
)
st.plotly_chart(fig_trend, use_container_width=True)

# --- Narrativa con IA ------------------------------------------------------
st.divider()
st.subheader("🤖 Resumen ejecutivo con IA")

with st.expander("Configurar IA"):
    provider = st.radio("Proveedor", ["Anthropic (Claude)", "Sin IA (demo local)"], horizontal=True)
    api_key = st.text_input("API key", type="password", help="No se guarda; solo vive en esta sesión.")
    model = st.text_input("Modelo", value="claude-haiku-4-5-20251001")

prompt_base = st.text_area(
    "Prompt",
    value=(
        "Eres un analista ESG. Con base en los siguientes datos agregados, "
        "redacta un resumen ejecutivo de 4-6 líneas para un tomador de decisiones. "
        "Identifica la tendencia principal, países o continentes destacados y un riesgo."
    ),
    height=100,
)

if st.button("Generar resumen", type="primary"):
    resumen_df = (
        fdf.groupby("continent", as_index=False)
        .agg(
            co2_per_capita=("co2_per_capita", "mean"),
            gdp_per_capita=("gdp_per_capita", "mean"),
            co2_total_mt=("co2_mt", "sum"),
        )
        .round(2)
    )
    contexto = (
        f"Rango de años: {year_range[0]}-{year_range[1]}\n"
        f"Continentes: {', '.join(sel_continents)}\n"
        f"Países: {len(fdf['country'].unique())}\n\n"
        f"Agregado por continente:\n{resumen_df.to_string(index=False)}\n\n"
        f"Crecimiento de CO₂ {prev_year}->{latest_year}: {growth:+.2f}%"
    )
    full_prompt = f"{prompt_base}\n\nDATOS:\n{contexto}"

    if provider.startswith("Anthropic") and api_key:
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=api_key)
            msg = client.messages.create(
                model=model,
                max_tokens=600,
                messages=[{"role": "user", "content": full_prompt}],
            )
            st.success(msg.content[0].text)
        except Exception as e:
            st.error(f"Error con la API: {e}")
    else:
        top = resumen_df.sort_values("co2_per_capita", ascending=False).iloc[0]
        bot = resumen_df.sort_values("co2_per_capita").iloc[0]
        st.info(
            f"**Resumen (modo demo local):** Entre {year_range[0]} y {year_range[1]}, "
            f"**{top['continent']}** lidera las emisiones per cápita "
            f"({top['co2_per_capita']:.2f} t/hab) mientras que **{bot['continent']}** "
            f"es el más bajo ({bot['co2_per_capita']:.2f} t/hab). "
            f"El cambio interanual {prev_year}→{latest_year} fue de **{growth:+.2f}%**. "
            f"Riesgo: la correlación entre PIB per cápita y CO₂ sugiere que el crecimiento "
            f"económico aún no se ha desacoplado de las emisiones."
        )
    with st.expander("Ver prompt enviado"):
        st.code(full_prompt)

# --- Datos crudos ----------------------------------------------------------
with st.expander("Ver tabla de datos filtrados"):
    st.dataframe(fdf, use_container_width=True, hide_index=True)
    st.download_button(
        "Descargar CSV",
        fdf.to_csv(index=False).encode("utf-8"),
        "esg_filtrado.csv",
        "text/csv",
    )
