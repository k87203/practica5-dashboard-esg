# 🌍 ESG Data Explorer

Dashboard interactivo para explorar indicadores ESG (Environmental, Social, Governance) globales: relación entre PIB y emisiones de CO₂ por país, continente y año.

Práctica 5 · Unidad 5 · Visualización de datos.

## Stack

- **Python 3.10+**
- **Streamlit** — interfaz reactiva
- **Plotly Express** — gráficos interactivos (scatter animado, choropleth, líneas)
- **pandas** — manipulación
- **Anthropic Claude** (opcional) — narrativa con IA
- **World Bank Open Data API** — fuente de datos

## Instalación

```powershell
cd "Y:\programacion avanzada cd\ultima u"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecutar

```powershell
streamlit run app.py
```

La primera ejecución descarga ~23 años de datos del Banco Mundial y los cachea en `data/esg_data.csv`. Las siguientes son instantáneas.

## Guía de usuario (3 pasos)

1. **Filtra** en la barra lateral: elige rango de años, continentes y opcionalmente países.
2. **Explora** los KPIs y los gráficos: el scatter animado muestra la evolución PIB↔CO₂, el mapa coroplético colorea por intensidad de emisiones per cápita.
3. **Genera narrativa** con IA: pega tu API key de Anthropic en el panel inferior y haz clic en *Generar resumen* para obtener un resumen ejecutivo automático. Si no tienes key, el modo demo local produce un texto basado en estadísticas.

## Métricas

- **CO₂ per cápita** = `co2_kt * 1000 / population` (toneladas/habitante)
- **PIB per cápita** = `gdp_usd / population` (USD/habitante)
- **Crecimiento interanual** = `(V_actual − V_anterior) / V_anterior × 100`

## Arquitectura de la información

| Visual | Por qué |
|---|---|
| Scatter animado PIB vs CO₂ | Permite observar la curva de Kuznets ambiental: cómo la relación cambia con el desarrollo económico. |
| Choropleth | Comunica intensidad geográfica de forma inmediata; un gráfico de barras con 180 países sería ilegible. |
| Líneas por continente | Tendencia temporal agregada — responde "¿está creciendo el problema?". |
| KPIs en tarjetas | Anclaje numérico rápido antes de explorar lo visual. |

## Reflexión ética

- **Escala log** en PIB per cápita: necesaria por la asimetría del dato (USA vs Burundi), pero se etiqueta explícitamente para no engañar.
- **Paleta secuencial** (rojos) en el mapa solo para una variable continua positiva — evitar paletas divergentes que sugerirían un "punto neutro" inexistente.
- **Per cápita vs total**: mostrar ambas evita culpar a países poblados por emisiones absolutas que en realidad son bajas por persona.
- **Datos faltantes**: se filtran con `dropna` y se muestra el conteo de países filtrados para que el usuario sepa qué tan completa es la muestra.

## Estructura

```
ultima u/
├── app.py              # Dashboard Streamlit
├── data_loader.py      # Descarga datos World Bank
├── requirements.txt
├── README.md
└── data/
    └── esg_data.csv    # Cache (generado en primer run)
```
