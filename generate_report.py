"""Genera informe.pdf con el informe tecnico de la Practica 5."""
from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, ListFlowable, ListItem,
)

OUT = Path(__file__).parent / "informe.pdf"
REPO_URL = "https://github.com/k87203/practica5-dashboard-esg"
VIDEO_URL = "(pendiente — pegar URL de YouTube aqui)"

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=18,
                    textColor=colors.HexColor("#0B5345"), spaceAfter=10)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=13,
                    textColor=colors.HexColor("#117A65"), spaceBefore=12, spaceAfter=6)
BODY = ParagraphStyle("Body", parent=styles["BodyText"], fontSize=10.5,
                      leading=15, alignment=TA_JUSTIFY, spaceAfter=6)
SMALL = ParagraphStyle("Small", parent=styles["BodyText"], fontSize=9,
                       textColor=colors.grey, alignment=TA_CENTER)
TITLE = ParagraphStyle("Title", parent=styles["Title"], fontSize=24,
                       textColor=colors.HexColor("#0B5345"), alignment=TA_CENTER,
                       spaceAfter=8)
SUBTITLE = ParagraphStyle("Subtitle", parent=styles["BodyText"], fontSize=13,
                          alignment=TA_CENTER, textColor=colors.HexColor("#5D6D7E"),
                          spaceAfter=30)
CODE = ParagraphStyle("Code", parent=styles["Code"], fontSize=9.5,
                      backColor=colors.HexColor("#F4F6F7"),
                      borderColor=colors.HexColor("#D5D8DC"), borderWidth=0.5,
                      borderPadding=6, leading=13)


def b(t):
    return f"<b>{t}</b>"


def bullet(items, style=BODY):
    return ListFlowable(
        [ListItem(Paragraph(x, style), leftIndent=10) for x in items],
        bulletType="bullet", start="circle", leftIndent=15,
    )


def build():
    doc = SimpleDocTemplate(
        str(OUT), pagesize=LETTER,
        leftMargin=2.2*cm, rightMargin=2.2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="Informe Tecnico - Practica 5", author="Yair Garcia",
    )
    story = []

    # --- PORTADA ---
    story += [
        Spacer(1, 4*cm),
        Paragraph("ESG Data Explorer", TITLE),
        Paragraph("Tablero de sostenibilidad global", SUBTITLE),
        Paragraph("Informe Tecnico - Practica 5", styles["Heading2"]),
        Paragraph("Unidad 5: Visualizacion de datos", BODY),
        Spacer(1, 1.2*cm),
        Table([
            ["Autor:", "Yair Garcia"],
            ["Institucion:", "Instituto Tecnologico de Tlahuac III"],
            ["Carrera:", "Ciencia de Datos"],
            ["Fecha:", date.today().strftime("%d de %B de %Y")],
            ["Repositorio:", REPO_URL],
            ["Video tutorial:", VIDEO_URL],
        ], colWidths=[3.5*cm, 11*cm], style=TableStyle([
            ("FONT", (0,0), (0,-1), "Helvetica-Bold", 10.5),
            ("FONT", (1,0), (1,-1), "Helvetica", 10.5),
            ("TEXTCOLOR", (0,0), (0,-1), colors.HexColor("#566573")),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ])),
        PageBreak(),
    ]

    # --- 1. ESCENARIO ---
    story += [
        Paragraph("1. Escenario y objetivo", H1),
        Paragraph(
            "El presente proyecto desarrolla un <b>dashboard interactivo profesional</b> "
            "que permite a un tomador de decisiones explorar indicadores ESG "
            "(<i>Environmental, Social and Governance</i>) a nivel global. "
            "Particularmente, se analiza la relacion entre el PIB y las emisiones "
            "de CO<sub>2</sub> de los paises del mundo entre los anios 2000 y 2022, "
            "con el fin de comprender si el crecimiento economico esta acoplado o "
            "no a la huella de carbono.",
            BODY),
        Paragraph(
            "La fuente de datos es la <b>World Bank Open Data API</b>, "
            "descargada en tiempo real mediante la libreria <code>requests</code> y cacheada "
            "localmente en un CSV para garantizar reproducibilidad. Los indicadores "
            "utilizados son:", BODY),
        bullet([
            "<code>NY.GDP.MKTP.CD</code> &mdash; PIB en USD corrientes.",
            "<code>EN.GHG.CO2.MT.CE.AR5</code> &mdash; Emisiones de CO<sub>2</sub> en megatoneladas.",
            "<code>SP.POP.TOTL</code> &mdash; Poblacion total.",
        ]),
    ]

    # --- 2. ARQUITECTURA DE INFORMACION ---
    story += [
        Paragraph("2. Arquitectura de la informacion", H1),
        Paragraph(
            "Cada componente visual fue elegido con un proposito narrativo "
            "especifico. La eleccion no es estetica sino comunicacional: "
            "diferentes preguntas requieren diferentes gramaticas visuales.", BODY),
        Table([
            [b("Visual"), b("Pregunta que responde"), b("Justificacion")],
            ["KPIs (tarjetas)",
             "Cuanto y cuanto cambio?",
             "Anclaje numerico inmediato antes de explorar. Reduce carga cognitiva."],
            ["Scatter animado\nPIB vs CO2",
             "Como evoluciona la relacion en el tiempo?",
             "Permite observar la curva de Kuznets ambiental. La animacion comunica trayectoria, no solo estado."],
            ["Choropleth mundial",
             "Donde se concentra el problema?",
             "Mapa coroplético: intensidad geografica inmediata. Un grafico de barras con 180 paises seria ilegible."],
            ["Lineas por continente",
             "La tendencia agregada sube o baja?",
             "Series de tiempo agrupadas: tendencia macro sin perderse en el detalle pais."],
        ], colWidths=[3.5*cm, 5*cm, 7.5*cm], style=TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#117A65")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONT", (0,0), (-1,-1), "Helvetica", 9.5),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#D5D8DC")),
            ("ROWBACKGROUNDS", (0,1), (-1,-1),
             [colors.white, colors.HexColor("#F8F9F9")]),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
            ("RIGHTPADDING", (0,0), (-1,-1), 6),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ])),
        Spacer(1, 8),
        Paragraph(
            "<b>Por que un mapa y no un grafico de barras?</b> "
            "Para datos georreferenciados de ~180 entidades, el mapa aprovecha el "
            "conocimiento espacial previo del usuario: identificar Africa o Asia es "
            "instantaneo. Una barra requiere lectura secuencial de etiquetas. "
            "Ademas, el color codifica intensidad en una dimension que las barras "
            "ya usan para magnitud, evitando redundancia.", BODY),
    ]

    # --- 3. METRICAS ---
    story += [
        Paragraph("3. Calculos y metricas", H1),
        Paragraph("Las metricas reportadas en el dashboard se calculan asi:", BODY),
        Spacer(1, 4),
        Paragraph("CO<sub>2</sub> per capita (toneladas/habitante)", H2),
        Paragraph(
            "co2_per_capita = co2_mt &times; 1,000,000 / poblacion", CODE),
        Paragraph("PIB per capita (USD/habitante)", H2),
        Paragraph("gdp_per_capita = gdp_usd / poblacion", CODE),
        Paragraph("Tasa de crecimiento interanual (%)", H2),
        Paragraph(
            "Crecimiento = ((V_actual - V_anterior) / V_anterior) &times; 100", CODE),
        Paragraph(
            "Esta tasa se aplica al total agregado de CO<sub>2</sub> de los paises filtrados "
            "y permite cuantificar la velocidad del cambio anio contra anio. "
            "Un valor positivo indica aceleracion de emisiones; negativo, "
            "desacople parcial del crecimiento economico.", BODY),
        Paragraph("Agregaciones del resumen ejecutivo (IA)", H2),
        Paragraph(
            "Para el prompt enviado al modelo de lenguaje, los datos filtrados se "
            "agrupan por continente y se calcula el promedio de CO<sub>2</sub> per capita, "
            "promedio de PIB per capita y suma total de CO<sub>2</sub> en Mt. Esto reduce "
            "la cardinalidad antes de la inferencia y mejora el costo y la latencia "
            "de la llamada.", BODY),
    ]

    # --- 4. GUIA DE USUARIO ---
    story += [
        Paragraph("4. Guia de usuario", H1),
        Paragraph(
            "El dashboard fue disenado para que un usuario sin formacion tecnica "
            "obtenga insights en menos de un minuto. Tres pasos:", BODY),
        bullet([
            b("Paso 1 &mdash; Filtrar.") + " En la barra lateral izquierda, ajusta el "
            "<i>rango de anios</i> con el slider, selecciona uno o varios <i>continentes</i> "
            "y opcionalmente acota a paises especificos. Todos los componentes se "
            "actualizan en cascada al instante.",
            b("Paso 2 &mdash; Explorar.") + " Lee primero los cuatro <i>KPIs</i> superiores "
            "para tener una vision agregada. Despues, usa el scatter animado "
            "(boton play) para ver la evolucion historica y el mapa coroplético "
            "para ubicar geograficamente las emisiones del anio mas reciente.",
            b("Paso 3 &mdash; Generar narrativa con IA.") + " En el panel inferior, "
            "abre <i>Configurar IA</i>, pega tu API key de Anthropic y haz clic en "
            "<i>Generar resumen</i>. La IA producira un resumen ejecutivo de "
            "4-6 lineas basado en los datos efectivamente filtrados. Si no "
            "cuentas con API key, el modo demo local genera un resumen "
            "estadistico equivalente.",
        ]),
    ]

    # --- 5. ETICA ---
    story += [
        PageBreak(),
        Paragraph("5. Reflexion etica", H1),
        Paragraph(
            "La visualizacion de datos es persuasiva por naturaleza y puede "
            "facilmente enganar si no se ejerce diligencia. En este proyecto se "
            "tomaron las siguientes decisiones para mitigar sesgos:", BODY),
        bullet([
            b("Escala logaritmica en PIB per capita:") + " indispensable por la "
            "asimetria del dato (EEUU vs Burundi diferen por tres ordenes de "
            "magnitud). Una escala lineal aplastaria visualmente a los paises "
            "pobres. Se etiqueta el eje como '(USD, log)' para que el lector "
            "interprete correctamente.",
            b("Per capita vs total:") + " mostrar CO<sub>2</sub> per capita evita "
            "culpar a paises poblados (China, India) por emisiones absolutas "
            "que, divididas entre su poblacion, son moderadas. Se complementa "
            "con la metrica total agregada para contextualizar el impacto global.",
            b("Paleta secuencial (rojos) en el mapa:") + " adecuada para una "
            "variable continua positiva sin punto neutro natural. Una paleta "
            "divergente (rojo-azul) sugeriria un umbral 'bueno/malo' que no "
            "existe objetivamente.",
            b("Tratamiento de datos faltantes:") + " los registros con NaN en PIB "
            "o CO<sub>2</sub> se descartan, pero se reporta el conteo de paises efectivos "
            "para que el usuario conozca la cobertura. No se imputan valores "
            "para evitar precision falsa.",
            b("Transparencia del prompt de IA:") + " el dashboard muestra "
            "explicitamente el prompt enviado al modelo. La narrativa generada "
            "queda asi auditable: el usuario puede verificar que la conclusion "
            "se deriva de los datos y no de sesgos del modelo.",
            b("API key del usuario:") + " la clave se introduce en un campo "
            "<code>password</code> y vive unicamente en la sesion de Streamlit; no se "
            "persiste a disco ni se transmite a terceros mas alla del proveedor "
            "del modelo.",
        ]),
    ]

    # --- 6. CONCLUSIONES ---
    story += [
        Paragraph("6. Conclusiones", H1),
        Paragraph(
            "El proyecto demuestra que es viable construir, con menos de 200 "
            "lineas de Python, una <i>data app</i> con la calidad de comunicacion "
            "esperada en un entorno profesional. Streamlit reduce la barrera "
            "entre el cientifico de datos y el usuario final, mientras que "
            "Plotly aporta la interactividad necesaria para una exploracion "
            "real (zoom, hover, animacion).", BODY),
        Paragraph(
            "La integracion de un modelo de lenguaje como capa narrativa "
            "convierte el dashboard de una herramienta de consulta en un "
            "asistente analitico: el usuario no solo ve los datos, recibe "
            "una sintesis interpretable adaptada a su seleccion. Este patron "
            "&mdash; <i>dashboard + LLM</i> &mdash; es el estandar emergente en BI moderno.", BODY),
    ]

    # --- STACK ---
    story += [
        Paragraph("Anexo. Stack tecnologico", H1),
        Table([
            [b("Componente"), b("Tecnologia"), b("Version")],
            ["Lenguaje", "Python", "3.12"],
            ["Framework UI", "Streamlit", ">=1.32"],
            ["Graficos", "Plotly Express", ">=5.20"],
            ["Datos", "pandas / requests", ">=2.2 / >=2.31"],
            ["IA", "Anthropic Claude (Haiku 4.5)", ">=0.39"],
            ["Fuente", "World Bank Open Data API", "v2"],
        ], colWidths=[4*cm, 7*cm, 5*cm], style=TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#117A65")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONT", (0,0), (-1,-1), "Helvetica", 10),
            ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#D5D8DC")),
            ("ROWBACKGROUNDS", (0,1), (-1,-1),
             [colors.white, colors.HexColor("#F8F9F9")]),
            ("ALIGN", (0,0), (-1,-1), "LEFT"),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("TOPPADDING", (0,0), (-1,-1), 6),
        ])),
    ]

    doc.build(story)
    print(f"OK -> {OUT}")


if __name__ == "__main__":
    build()
