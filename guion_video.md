# Guion del video — ESG Data Explorer

**Duración objetivo:** 12–14 minutos · **Tono:** profesional, claro, conversacional
**Ritmo de lectura:** ~140 palabras/min. Si lees rápido, pausa en los puntos.

---

## ⏱ 0:00 – 1:00 · Pitch (Dashboard en pantalla, ya filtrado)

Hola, soy Yair García, estudiante de Ciencia de Datos en el Instituto Tecnológico de Tláhuac III. Lo que ves en pantalla es **ESG Data Explorer**, un tablero interactivo que permite explorar la relación entre el desarrollo económico y las emisiones de CO₂ de los países del mundo entre los años 2000 y 2022.

La pregunta de fondo es simple: ¿cuándo un país se vuelve más rico, también contamina más? Y si lo hace, ¿en qué medida? Hoy en día, los tomadores de decisiones —ya sea en gobierno, en finanzas sostenibles o en consultoría— necesitan respuestas a este tipo de preguntas en segundos, no en horas. Mandar un PDF con gráficas estáticas ya no alcanza.

Por eso construí esta *data app*: el usuario filtra por año, continente o país, y todo el tablero reacciona al instante. Además, integré un modelo de lenguaje que genera un resumen ejecutivo escrito en lenguaje natural a partir de los datos que se están viendo. En los próximos doce minutos te muestro cómo funciona, cómo está construido y qué decisiones de diseño tomé para que la información no engañe al usuario.

---

## ⏱ 1:00 – 2:30 · Stack y arquitectura general

El stack es 100% Python. La interfaz está hecha con **Streamlit**, que es el estándar actual para construir aplicaciones de datos sin tener que escribir HTML ni JavaScript. Los gráficos son de **Plotly Express**, que es la librería que me da hover, zoom y animaciones de forma gratuita. Los datos los descargo en vivo de la API abierta del **Banco Mundial**, específicamente tres indicadores: PIB en dólares, emisiones de CO₂ en megatoneladas y población total. Y para la narrativa, uso la API de **Anthropic Claude**.

Todo el proyecto vive en menos de 200 líneas de código, está versionado en GitHub y se ejecuta con un solo comando: `streamlit run app.py`. La primera vez descarga los datos del Banco Mundial y los guarda en un CSV local, así las ejecuciones siguientes son instantáneas.

---

## ⏱ 2:30 – 5:00 · Layout y reactividad (mover filtros en vivo)

Déjame mostrarte cómo está organizada la pantalla. A la izquierda tengo el panel de filtros, que es lo primero que ve el usuario. Esto es deliberado: la barra lateral es donde vive el "control", y el resto de la pantalla es donde vive la "respuesta". Tres filtros: un *slider* con el rango de años, un *multiselect* de continentes, y otro de países que se acota dinámicamente al continente elegido.

Arriba a la derecha tengo cuatro **KPIs** en tarjetas: número de países filtrados, CO₂ per cápita promedio, PIB per cápita promedio y el cambio interanual del CO₂ total. Estas tarjetas son lo primero que comunica magnitud al usuario antes de mirar cualquier gráfico.

*[Mover el slider de años, por ejemplo de 2000–2022 a 2015–2022]*

Fíjate lo que acaba de pasar. Moví el slider y **toda la página se recalculó**: los KPIs cambiaron, el scatter ahora solo muestra esos años, el mapa se redibujó con el año más reciente del nuevo rango y la línea temporal se acortó. Esto es lo que Streamlit llama *reactividad por estado*: cada vez que cambia un *widget*, todo el script se vuelve a ejecutar de arriba a abajo, pero usando datos cacheados con el decorador `@st.cache_data`, así que es prácticamente instantáneo aunque el dataset tenga más de cuatro mil registros.

*[Quitar Asia y Europa del multiselect de continentes]*

Aquí mismo, si dejo solo África y Américas, otra vez todo se actualiza coherentemente: la tendencia temporal ya no muestra esas dos líneas, el mapa pinta solo los continentes seleccionados, y los promedios se recalculan sobre la nueva muestra. No tuve que escribir ni una sola línea de "onChange"; Streamlit lo hace por mí.

---

## ⏱ 5:00 – 8:00 · Los gráficos y por qué cada uno

Hablemos de cada gráfico, porque la elección no es estética sino comunicacional.

**El scatter animado de PIB versus CO₂** es el corazón del dashboard. En el eje X tengo PIB per cápita, en escala logarítmica porque la diferencia entre Estados Unidos y Burundi es de tres órdenes de magnitud y una escala lineal aplastaría a los países pobres. En el eje Y, CO₂ per cápita en toneladas. Cada burbuja es un país, su tamaño es proporcional a la población, y su color indica el continente.

Y lo más importante: la animación. Cuando le doy play *[mostrar la animación corriendo]*, podemos ver cómo cada país se desplaza año tras año. Esto es lo que en economía ambiental se llama la **curva de Kuznets ambiental**: la hipótesis de que la contaminación crece con el desarrollo hasta cierto punto y luego empieza a decrecer. Aquí literalmente podemos verla, o no verla, con datos reales.

**El mapa coroplético** responde otra pregunta: ¿dónde está geográficamente el problema? Usé una paleta secuencial de rojos porque la variable —CO₂ per cápita— es estrictamente positiva y no tiene un punto neutro natural. Una paleta divergente sugeriría un umbral "bueno-malo" que no existe objetivamente. ¿Por qué no usé un gráfico de barras? Porque con 180 países, una barra horizontal sería ilegible; el mapa aprovecha el conocimiento geográfico que el usuario ya tiene.

**La gráfica de líneas por continente** es para la tendencia agregada. Aquí se ve clarísimo: las emisiones totales de Asia se duplicaron en estos veinte años, mientras que Europa las redujo. Esa es una historia que las otras dos visualizaciones no cuentan tan directamente.

---

## ⏱ 8:00 – 11:00 · Narrativa con IA

Ahora viene la parte que para mí es más interesante. Bajo de la página y encuentro el panel de **resumen ejecutivo con IA**.

*[Mostrar el panel, expandir "Configurar IA"]*

El usuario tiene dos opciones: usar Anthropic Claude pegando su API key, o usar el modo demo local, que produce un resumen basado en estadísticas calculadas sin necesidad de internet. Esto último lo agregué pensando en quien no tiene acceso a una API de pago.

Lo interesante es **cómo se construye el prompt**. No le mando el dataset crudo al modelo, eso sería caro y lento. Lo que hago es agrupar los datos filtrados por continente, sacar promedios de CO₂ y PIB per cápita, sumar el total de emisiones, calcular el crecimiento interanual, y eso es lo que mando como contexto. Es alrededor de 200 tokens de entrada por consulta.

*[Hacer clic en "Generar resumen"]*

Y este es el resultado. *[Leer en voz alta el resumen generado]* En cuatro líneas, el modelo identificó la tendencia principal, los continentes destacados y un riesgo. Eso, escrito a mano por un analista, tomaría diez o quince minutos. Aquí toma dos segundos.

Importante: en la opción "**Ver prompt enviado**", el usuario puede inspeccionar exactamente qué le mandé al modelo. Esto es transparencia: la narrativa generada queda auditable. Si la IA dice algo raro, el usuario puede verificar si fue por los datos o por un sesgo del modelo.

---

## ⏱ 11:00 – 12:30 · Decisiones éticas

Quiero cerrar con un punto que considero importante: cómo evité que las visualizaciones engañen al usuario.

Primero, la **escala logarítmica** en PIB está explícitamente etiquetada como tal. No es decorativo: es para que el lector sepa que está comparando órdenes de magnitud, no diferencias absolutas.

Segundo, mostré CO₂ **per cápita y no solo total**. Esto evita culpar a países muy poblados como China o India por emisiones absolutas que, divididas entre su población, son moderadas comparadas con otros.

Tercero, los datos faltantes se descartan y se reporta cuántos países quedaron en la muestra. No imputé valores para evitar lo que se llama "precisión falsa".

Cuarto, la **API key** del usuario se introduce en un campo tipo *password* y vive solo en la sesión: no se persiste a disco ni se comparte con nadie más que el proveedor del modelo.

---

## ⏱ 12:30 – 13:30 · Cierre

Para resumir: en menos de 200 líneas de Python construí una *data app* completa con filtros reactivos, KPIs, dos gráficos interactivos, un mapa mundial, una serie de tiempo y un componente de IA que genera narrativa automática.

El código está disponible en GitHub, en **github.com/k87203/practica5-dashboard-esg**, junto con el informe técnico, las capturas y este guion. Cualquier persona puede clonarlo y correrlo en menos de dos minutos.

Lo que aprendí construyendo esto es que el futuro de la visualización de datos no son los PDFs con gráficas: son aplicaciones donde el usuario explora, filtra y obtiene insights por su cuenta, con la IA actuando como un analista junior que le susurra interpretaciones al oído.

Gracias por ver el video. Si tienes preguntas, pueden dejarlas en los comentarios. Nos vemos en la próxima práctica.

---

## Notas de producción

- **Pantalla:** maximiza el navegador, oculta la barra de marcadores (Ctrl+Shift+B en Chrome). Usa el tema oscuro del dashboard para que la presentación se vea uniforme.
- **Audio:** graba en una habitación con cosas blandas (cobijas, ropa colgada) para amortiguar el eco. Si tu micrófono tiene reducción de ruido, actívala.
- **Cortes:** no intentes leer todo de corrido. Graba por bloques (cada `##`) y une después en CapCut, DaVinci Resolve o ClipChamp. Si te trabas, simplemente corta y repite la oración.
- **Subtítulos:** YouTube los genera automáticos, pero revísalos antes de publicar; suelen confundir "CO₂" con "cero dos" o "ESG" con palabras al azar.
- **Miniatura sugerida:** captura del scatter animado en pantalla completa, con un texto grande encima que diga "DASHBOARD ESG EN PYTHON". Alto contraste.
