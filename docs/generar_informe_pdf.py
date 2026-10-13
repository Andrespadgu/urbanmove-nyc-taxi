"""
Genera informe_urbanmove.pdf usando reportlab.
Replica el contenido del .tex sin necesidad de LaTeX instalado.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ── Fuentes Unicode (Arial TrueType — soporta griego, símbolo, etc.) ─────────
_WF = 'C:/Windows/Fonts/'
pdfmetrics.registerFont(TTFont('Arial',            _WF + 'arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold',       _WF + 'arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Italic',     _WF + 'ariali.ttf'))
pdfmetrics.registerFont(TTFont('Arial-BoldItalic', _WF + 'arialbi.ttf'))
pdfmetrics.registerFontFamily('Arial',
    normal='Arial', bold='Arial-Bold',
    italic='Arial-Italic', boldItalic='Arial-BoldItalic')

# ── Paleta ────────────────────────────────────────────────────
AZUL     = colors.HexColor('#1A3A5C')
CIAN     = colors.HexColor('#00B4D8')
NARANJA  = colors.HexColor('#FF9F1C')
VERDE    = colors.HexColor('#4CAF50')
GRIS_BG  = colors.HexColor('#F5F5F5')
GRIS_MED = colors.HexColor('#CCCCCC')
GRIS_TXT = colors.HexColor('#555555')
BLANCO   = colors.white

W, H = A4  # 595.28 x 841.89 pt
MARGIN = 2.5 * cm

OUT_PATH = os.path.join(os.path.dirname(__file__), 'informe_urbanmove.pdf')

# ── Estilos base ──────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

estilo_normal = S('enormal',
    parent=base['Normal'], fontSize=10.5, leading=16,
    alignment=TA_JUSTIFY, textColor=colors.black, spaceAfter=6,
    fontName='Arial')

estilo_h1 = S('eh1',
    parent=base['Heading1'], fontSize=16, leading=22,
    textColor=AZUL, spaceBefore=18, spaceAfter=8,
    fontName='Arial-Bold', borderPadding=(0,0,4,0))

estilo_h2 = S('eh2',
    parent=base['Heading2'], fontSize=13, leading=18,
    textColor=AZUL, spaceBefore=14, spaceAfter=6,
    fontName='Arial-Bold')

estilo_titulo_portada = S('etit',
    fontSize=22, leading=30, alignment=TA_CENTER,
    textColor=AZUL, fontName='Arial-Bold', spaceAfter=12)

estilo_subtitulo = S('esub',
    fontSize=13, leading=18, alignment=TA_CENTER,
    textColor=GRIS_TXT, fontName='Arial', spaceAfter=6)

estilo_miembros = S('emiembros',
    fontSize=11, leading=17, alignment=TA_CENTER,
    textColor=colors.black, fontName='Arial', spaceAfter=4)

estilo_nota = S('enota',
    fontSize=9.5, leading=14, alignment=TA_JUSTIFY,
    textColor=GRIS_TXT, fontName='Arial-Italic')

estilo_hallazgo = S('ehallazgo',
    fontSize=10.5, leading=16, alignment=TA_JUSTIFY,
    textColor=colors.black, fontName='Arial-Italic',
    leftIndent=8, rightIndent=8)

estilo_caption = S('ecap',
    fontSize=9, leading=13, alignment=TA_CENTER,
    textColor=GRIS_TXT, fontName='Arial-Italic',
    spaceBefore=3, spaceAfter=8)

estilo_abstract_title = S('eabtit',
    fontSize=11, leading=15, alignment=TA_CENTER,
    textColor=AZUL, fontName='Arial-Bold', spaceAfter=4)

estilo_abstract_body = S('eabbody',
    fontSize=10, leading=15, alignment=TA_JUSTIFY,
    textColor=colors.black, fontName='Arial',
    leftIndent=18, rightIndent=18, spaceAfter=8)

# ── Header / Footer ───────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont('Arial', 8)
    canvas.setFillColor(GRIS_TXT)
    canvas.drawString(MARGIN, 1.2*cm, 'UrbanMove — NYC Taxi')
    canvas.drawRightString(W - MARGIN, 1.2*cm, f'Página {doc.page}')
    canvas.setStrokeColor(GRIS_MED)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 1.5*cm, W - MARGIN, 1.5*cm)
    canvas.restoreState()

def on_first_page(canvas, doc):
    canvas.saveState()
    canvas.restoreState()

# ── Tabla helper ──────────────────────────────────────────────
def p_cell(text, fs=9, bold=False, center=False):
    """Paragraph para celda de tabla — fuerza wrapping correcto."""
    fn = 'Arial-Bold' if bold else 'Arial'
    al = TA_CENTER if center else TA_LEFT
    s = ParagraphStyle(f'cell_{id(text)}', fontName=fn, fontSize=fs,
                       leading=fs * 1.35, alignment=al, wordWrap='LTR',
                       spaceAfter=0, spaceBefore=0)
    return Paragraph(text, s)

def tabla(data, col_widths, caption_text, header_rows=1):
    """Construye una Table con estilo corporativo."""
    t = Table(data, colWidths=col_widths, repeatRows=header_rows)
    style = [
        # Header (TEXTCOLOR/FONTNAME sólo aplican a celdas con string puro;
        # si la celda es Paragraph, el color lo controla p_cell con bold=True)
        ('BACKGROUND', (0, 0), (-1, header_rows-1), AZUL),
        ('TEXTCOLOR',  (0, 0), (-1, header_rows-1), BLANCO),
        ('FONTNAME',   (0, 0), (-1, header_rows-1), 'Arial-Bold'),
        ('FONTSIZE',   (0, 0), (-1, header_rows-1), 9),
        ('ALIGN',      (0, 0), (-1, header_rows-1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, header_rows-1), 7),
        ('TOPPADDING',    (0, 0), (-1, header_rows-1), 7),
        # Body
        ('FONTNAME',   (0, header_rows), (-1, -1), 'Arial'),
        ('FONTSIZE',   (0, header_rows), (-1, -1), 9),
        ('ALIGN',      (0, header_rows), (-1, -1), 'CENTER'),
        ('VALIGN',     (0, header_rows), (-1, -1), 'MIDDLE'),
        ('TOPPADDING',    (0, header_rows), (-1, -1), 5),
        ('BOTTOMPADDING', (0, header_rows), (-1, -1), 5),
        # Alternating rows
        ('ROWBACKGROUNDS', (0, header_rows), (-1, -1), [BLANCO, GRIS_BG]),
        # Grid
        ('GRID',       (0, 0), (-1, -1), 0.4, GRIS_MED),
        ('LINEBELOW',  (0, header_rows-1), (-1, header_rows-1), 1.2, AZUL),
        ('LINEABOVE',  (0, 0), (-1, 0), 1.5, AZUL),
        ('LINEBELOW',  (0, -1), (-1, -1), 1.5, AZUL),
        # Rounded corners mimic via box
        ('BOX',        (0, 0), (-1, -1), 1.2, AZUL),
    ]
    t.setStyle(TableStyle(style))
    caption = Paragraph(caption_text, estilo_caption)
    return [t, caption]

def hallazgo_box(texto):
    """Caja destacada (simula el entorno mdframed del LaTeX)."""
    inner = Paragraph(texto, estilo_hallazgo)
    data = [[inner]]
    t = Table(data, colWidths=[W - 2*MARGIN])
    t.setStyle(TableStyle([
        ('BOX',        (0,0), (-1,-1), 1.5, AZUL),
        ('BACKGROUND', (0,0), (-1,-1), GRIS_BG),
        ('LEFTPADDING',  (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING',   (0,0), (-1,-1), 8),
        ('BOTTOMPADDING',(0,0), (-1,-1), 8),
    ]))
    return [Spacer(1, 4), t, Spacer(1, 6)]

def hr():
    return HRFlowable(width='100%', thickness=1, color=GRIS_MED,
                      spaceAfter=4, spaceBefore=4)

def titulo_seccion(numero, texto):
    return Paragraph(f'{numero}.&nbsp;&nbsp;{texto}', estilo_h1)

def titulo_subseccion(numero, texto):
    return Paragraph(f'{numero}&nbsp;&nbsp;{texto}', estilo_h2)

def p(texto):
    return Paragraph(texto, estilo_normal)

def sp(n=8):
    return Spacer(1, n)

# ── Construir documento ───────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUT_PATH,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN,  bottomMargin=2*cm,
        title='UrbanMove — Análisis No Supervisado NYC Taxi',
        author='Andrés Padilla',
    )

    story = []

    # ═══════════════════════════════════════════════════════
    # PORTADA
    # ═══════════════════════════════════════════════════════
    story.append(Spacer(1, 3*cm))
    story.append(HRFlowable(width='100%', thickness=2.5, color=AZUL,
                             spaceAfter=10, spaceBefore=0))
    story.append(Paragraph(
        'Análisis No Supervisado de Patrones<br/>de Movilidad Urbana en Taxi:<br/>Caso UrbanMove — Nueva York',
        estilo_titulo_portada))
    story.append(HRFlowable(width='100%', thickness=2.5, color=AZUL,
                             spaceAfter=20, spaceBefore=6))
    story.append(sp(16))
    story.append(Paragraph('<i>Aprendizaje de Máquinas No Supervisado</i>', estilo_subtitulo))
    story.append(Paragraph('Universidad de La Sabana · Aprendizaje No Supervisado', estilo_subtitulo))
    story.append(sp(40))
    story.append(Paragraph('<b>Autor</b>', S('eit', parent=estilo_miembros, fontSize=12, fontName='Arial-Bold')))
    story.append(sp(8))
    story.append(Paragraph('Andrés Padilla', estilo_miembros))
    story.append(sp(60))
    story.append(Paragraph('<font color="#888888">Septiembre de 2026</font>', estilo_subtitulo))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # RESUMEN
    # ═══════════════════════════════════════════════════════
    story.append(Paragraph('Resumen', estilo_abstract_title))
    story.append(hr())
    story.append(sp(4))
    story.append(Paragraph(
        'Este documento presenta los resultados de un análisis de aprendizaje no supervisado '
        'aplicado al conjunto de datos NYC Taxi Trip Duration, que registra 1,458,644 viajes '
        'realizados en la ciudad de Nueva York entre enero y junio de 2016. El objetivo central '
        'es identificar patrones latentes de demanda y comportamiento de viaje que permitan a '
        'UrbanMove, empresa de transporte bajo demanda, tomar decisiones operativas cuantificadas. '
        'Se aplicaron tres familias de métodos: análisis de información y entropía, segmentación '
        'por partición (K-means y DBSCAN), y modelado de mezclas gaussianas con el algoritmo EM. '
        'Los hallazgos revelan que la hora del día concentra casi toda su entropía posible (97.4 %), '
        'que cuatro segmentos espaciotemporales explican la estructura principal del servicio, y que '
        'la distribución de viajes responde a cuatro perfiles latentes con características operativas '
        'diferenciadas. Con base en estos resultados se formulan tres recomendaciones cuantificadas '
        'orientadas al posicionamiento de conductores, la tarificación diferencial y la modelización '
        'de demanda por régimen.',
        estilo_abstract_body))
    story.append(sp(4))
    story.append(hr())
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # SECCIÓN 1 — CONTEXTO
    # ═══════════════════════════════════════════════════════
    story.append(titulo_seccion('1', 'Contexto y motivación'))
    story.append(p(
        'El transporte en taxi representa uno de los sistemas logísticos más complejos de una ciudad '
        'de alta densidad. Nueva York opera decenas de miles de viajes diarios con variabilidad '
        'temporal y espacial pronunciada: la demanda de las 7 h no se parece en nada a la de las '
        '14 h, y un viaje al aeropuerto JFK tiene un perfil completamente distinto al de un '
        'desplazamiento corto en Midtown. Esta heterogeneidad hace que los modelos operativos '
        'basados en promedios globales sean sistemáticamente ineficientes.'))
    story.append(p(
        'UrbanMove enfrenta precisamente este reto: diseñar una estrategia de posicionamiento de '
        'conductores, tarificación y asignación que responda a la estructura real de la demanda y '
        'no a supuestos uniformes. Para ello, el análisis aquí presentado parte de datos históricos '
        'reales y aplica técnicas de aprendizaje no supervisado que no requieren etiquetas externas, '
        'dejando que la propia distribución de los datos revele los patrones latentes.'))
    story.append(p(
        'El conjunto de datos NYC Taxi Trip Duration, publicado por la plataforma Kaggle en el '
        'contexto de una competición de predicción de duración de viajes, cubre el período '
        'enero–junio de 2016 y contiene 1,458,644 registros con once atributos originales: '
        'identificador de viaje, proveedor, fechas y horas de recogida y entrega, número de '
        'pasajeros, coordenadas de origen y destino, indicador de transmisión diferida y duración '
        'en segundos.'))

    # ═══════════════════════════════════════════════════════
    # SECCIÓN 2 — DATOS
    # ═══════════════════════════════════════════════════════
    story.append(titulo_seccion('2', 'Datos y preprocesamiento'))

    story.append(titulo_subseccion('2.1', 'Criterios de limpieza'))
    story.append(p(
        'El conjunto de datos crudo presentó cero valores nulos y cero identificadores duplicados, '
        'lo que indica un proceso de captura razonablemente robusto. Sin embargo, se detectaron '
        'registros con valores implausibles que debían eliminarse para garantizar que los análisis '
        'posteriores reflejaran viajes reales. Los criterios aplicados, definidos a priori con base '
        'en restricciones físicas y operativas, se resumen en la Tabla 1.'))
    story.append(sp(6))

    data_limpieza = [
        ['Criterio', 'Umbral', 'Registros eliminados'],
        ['passenger_count fuera de 1–6', '—', '65  (0.00 %)'],
        ['trip_duration < 60 s o > 10 800 s', '1 min – 3 h', '10,707  (0.73 %)'],
        ['Coordenadas recogida fuera bbox NYC', '—', '731  (0.05 %)'],
        ['Coordenadas destino fuera bbox NYC', '—', '5,899  (0.40 %)'],
        ['Distancia Haversine < 0.10 km', '—', '13,318  (0.91 %)'],
        ['Velocidad media > 100 km/h', '—', '175  (0.01 %)'],
        ['Total eliminado (filtros combinados)', '—', '23,592  (1.62 %)'],
    ]
    cw1 = [7.5*cm, 3*cm, 5*cm]
    story += tabla(data_limpieza, cw1, 'Tabla 1. Criterios de depuración aplicados al conjunto crudo.')
    story.append(sp(6))

    story.append(p(
        'Tras la depuración quedaron 1,435,052 viajes válidos. El umbral mínimo de duración '
        '(60 segundos) descarta arranques accidentales y errores de GPS; el máximo (3 horas) '
        'conserva viajes largos por congestión severa, que sí ocurren en NYC, pero elimina '
        'taxímetros olvidados. La distancia mínima de 100 metros excluye registros donde el '
        'origen y el destino son prácticamente idénticos y que no representan desplazamientos reales.'))

    story.append(titulo_subseccion('2.2', 'Variables derivadas'))
    story.append(p(
        'La ingeniería de variables es determinante para los análisis posteriores. Las once columnas '
        'originales se ampliaron a veintidós mediante la generación de los atributos descritos en '
        'la Tabla 2. El cálculo de distancias se realizó exclusivamente mediante la fórmula de '
        'Haversine, que tiene en cuenta la curvatura terrestre y evita el error sistemático de la '
        'distancia euclidiana sobre coordenadas geográficas (error del orden del 0.5–1 % en las '
        'escalas de NYC).'))
    story.append(sp(6))

    data_feat = [
        [p_cell('Variable', bold=True, center=True), p_cell('Descripción', bold=True, center=True)],
        [p_cell('dist_km'),      p_cell('Distancia geodésica Haversine entre recogida y destino (km).')],
        [p_cell('speed_kmh'),    p_cell('Velocidad media: dist_km / (trip_duration / 3600).')],
        [p_cell('duration_min'), p_cell('Duración en minutos.')],
        [p_cell('hour'),         p_cell('Hora del día de recogida (0–23).')],
        [p_cell('day_of_week'),  p_cell('Día de la semana (0 = lunes, 6 = domingo).')],
        [p_cell('is_weekend'),   p_cell('Indicador binario: 1 si sábado o domingo.')],
        [p_cell('franja'),       p_cell('Franja horaria operativa: madrugada (0–5), mañana pico (6–9), '
                                        'mañana baja (10–12), tarde pico (13–17), tarde baja (18–20), '
                                        'noche (21–23).')],
        [p_cell('zone_id'),      p_cell('Celda en grilla 8×8 sobre bbox de NYC (53 zonas activas de 64 posibles).')],
    ]
    cw2 = [3.5*cm, 12*cm]
    story += tabla(data_feat, cw2, 'Tabla 2. Variables derivadas incorporadas al análisis.')
    story.append(sp(6))

    story.append(titulo_subseccion('2.3', 'Muestreo reproducible'))
    story.append(p(
        'Trabajar sobre 1.4 millones de registros eleva sustancialmente el costo computacional '
        'de algoritmos iterativos como DBSCAN (complejidad O(n log n)–O(n<sup>2</sup>)) y el EM del GMM. '
        'Por ello se extrajo una muestra de 50,000 viajes mediante muestreo aleatorio estratificado '
        'por mes, asignación proporcional, semilla fija SEED = 42. La estratificación garantiza '
        'que la proporción de cada mes en la muestra replique la del dataset limpio; el coeficiente '
        'de variación entre meses es del 4.3 %, confirmando representatividad temporal.'))
    story.append(sp(6))

    data_meses = [
        ['Mes', 'Dataset limpio (%)', 'Muestra (%)'],
        ['Enero',    '15.8', '15.8'],
        ['Febrero',  '16.3', '16.3'],
        ['Marzo',    '17.6', '17.6'],
        ['Abril',    '17.2', '17.2'],
        ['Mayo',     '17.0', '17.0'],
        ['Junio',    '16.1', '16.1'],
    ]
    cw3 = [5*cm, 5*cm, 5*cm]
    story += tabla(data_meses, cw3, 'Tabla 3. Distribución mensual en el dataset limpio y en la muestra.')
    story.append(sp(6))

    story.append(p(
        'Con 33 zonas activas y 50,000 viajes, cada zona recibe en promedio ≈ 1,515 viajes, '
        'suficiente para estimar distribuciones de probabilidad y matrices de covarianza de forma '
        'estable. La muestra final contiene 35,756 viajes laborables (71.5 %) y 14,244 de fin de '
        'semana (28.5 %). Las estadísticas descriptivas centrales son: duración media 14.0 min '
        '(mediana 11.1 min), distancia media 3.4 km (mediana 2.1 km) y velocidad media 14.4 km/h.'))

    # ═══════════════════════════════════════════════════════
    # SECCIÓN 3 — INFORMACIÓN
    # ═══════════════════════════════════════════════════════
    story.append(titulo_seccion('3', 'Análisis de incertidumbre e información'))

    story.append(titulo_subseccion('3.1', 'Entropía de Shannon por zona y por hora'))
    story.append(p(
        'La entropía de Shannon H(X) = −Σ p(x) log<sub>2</sub> p(x) cuantifica en bits la incertidumbre '
        'de una variable discreta. Aplicada a las zonas de recogida, H(zona) = 2.2693 bits frente '
        'al máximo teórico log<sub>2</sub>(33) = 5.04 bits para 33 zonas equiprobables. Esto significa que '
        'la demanda aprovecha apenas el 45 % de la capacidad de dispersión posible: dos o tres '
        'zonas concentran una fracción desproporcionada de los viajes, lo que valida el diseño de '
        'estrategias de posicionamiento focalizadas.'))
    story.append(p(
        'La distribución horaria exhibe un comportamiento opuesto: H(hora) = 4.4639 bits frente '
        'al máximo de log<sub>2</sub>(24) = 4.585 bits, es decir, el 97.4 % de la entropía máxima. Las '
        '24 horas del día reciben demanda relativamente uniforme, y ninguna hora domina de forma '
        'absoluta. La implicación operativa es que el servicio debe estar activo en todo el espectro '
        'horario, pero las estrategias de diferenciación deben basarse en dónde, no en cuándo en '
        'términos absolutos.'))

    story.append(titulo_subseccion('3.2', 'Entropía condicional'))
    story.append(p(
        'La entropía condicional H(Z|F) = Σ p(f) H(Z|F=f) mide cuánta incertidumbre queda sobre '
        'la zona una vez conocida la franja horaria. Los resultados muestran que la franja con '
        'menor incertidumbre zonal es la madrugada: H(zona|madrugada) = 2.1325 bits. La demanda '
        'nocturna se concentra en menos lugares, lo que permite decisiones de posicionamiento más '
        'precisas. Por el contrario, la mañana pico registra la mayor dispersión: '
        'H(zona|mañana pico) = 2.3438 bits. En ese tramo, los orígenes de viaje están más repartidos '
        'por la ciudad, dificultando las predicciones de zona a partir de la hora sola.'))
    story.append(p(
        'A nivel de hora exacta, la hora 5 presenta la máxima dispersión zonal (H = 2.5738 bits), '
        'mientras que las 19 h registran la mayor concentración (H = 2.1622 bits), confirmando que '
        'el pico vespertino tiene una geografía de demanda más predecible que las horas intempestivas.'))

    story.append(titulo_subseccion('3.3', 'Información mutua'))
    story.append(p(
        'La información mutua I(X;Y) = H(X) − H(X|Y) cuantifica cuánto reduce la incertidumbre '
        'sobre X el hecho de conocer Y. Entre hora y zona se obtiene I(hora; zona) = 0.044030 bits, '
        'equivalente al 1.94 % de H(zona). A nivel de franja horaria agregada, la cifra cae a '
        'I(franja; zona) = 0.031191 bits (1.37 %). Ambos valores son pequeños pero estrictamente '
        'positivos, lo que confirma que hora y zona no son estadísticamente independientes: conocer '
        'cuándo ocurre un viaje sí reduce, aunque ligeramente, la incertidumbre sobre dónde ocurre. '
        'En la práctica, modelos de asignación que combinen señales temporales y espaciales '
        'superarán a modelos que traten ambas dimensiones como independientes.'))

    story.append(titulo_subseccion('3.4', 'Divergencia KL y entropía cruzada'))
    story.append(p(
        'Para comparar los regímenes laborable y fin de semana, se estimaron las distribuciones '
        'de probabilidad por hora en cada subconjunto y se calculó la divergencia de '
        'Kullback-Leibler KL(P ‖ Q) = Σ P(x) log<sub>2</sub> [P(x)/Q(x)].'))
    story.append(sp(4))
    story += hallazgo_box(
        'KL(lab ‖ fds) = 0.163617 bits y KL(fds ‖ lab) = 0.180599 bits. La asimetría confirma '
        'que los dos regímenes no son intercambiables: usar un modelo entrenado en días laborables '
        'para predecir fines de semana impone un sobrecoste de codificación del 3.71 % respecto '
        'al mejor modelo posible.')
    story.append(p(
        'La entropía cruzada H(P, Q) = H(P) + KL(P ‖ Q) = 4.576012 bits verificó el resultado '
        'algebraicamente con un error residual inferior a 10<sup>-15</sup>. Este hallazgo fundamenta '
        'directamente la recomendación de construir modelos de demanda separados por régimen '
        '(sección 6).'))

    story.append(titulo_subseccion('3.5', 'Estabilidad numérica: log-sum-exp'))
    story.append(p(
        'El cálculo de probabilidades sobre distribuciones con muchos componentes (33 zonas) '
        'expone al software a desbordamiento de punto flotante en sentido negativo (underflow). '
        'El operador log-sum-exp resuelve este problema mediante la identidad:'))
    story.append(p(
        '<b>lse(x) = c + log Σ<sub>i</sub> exp(x<sub>i</sub> − c),  c = max x<sub>i</sub></b>'))
    story.append(p(
        'Aplicado al cálculo de los denominadores de responsabilidades en el paso E del GMM, '
        'el error máximo respecto a la aritmética exacta fue &lt; 2 × 10<sup>-15</sup> para las 33 zonas '
        'activas, garantizando convergencia numérica estable del algoritmo EM.'))

    # ═══════════════════════════════════════════════════════
    # SECCIÓN 4 — CLUSTERING
    # ═══════════════════════════════════════════════════════
    story.append(titulo_seccion('4', 'Segmentación por partición'))

    story.append(titulo_subseccion('4.1', 'K-means: selección del número de clústeres'))
    story.append(p(
        'K-means se aplicó al espacio de características (hour, duration_min, dist_km, speed_kmh), '
        'normalizado con media cero y varianza unitaria. La selección de K combinó dos criterios '
        'complementarios: la curva de inercia (codo) y el coeficiente de silueta promedio.'))
    story.append(p(
        'La inercia disminuye un 19.1 % al pasar de K = 3 a K = 4, y solo un 17 % adicional al '
        'pasar a K = 5, con reducción decreciente a partir de ahí. El coeficiente de silueta alcanza '
        'su máximo en K = 4 con un valor de 0.2916, indicando separación moderada pero interpretable '
        'de los segmentos. Se adoptó K = 4 como la solución con mejor balance entre parsimonia y '
        'capacidad discriminatoria. El ajuste convergió en 8 iteraciones con una inercia final '
        'de 91,866.'))
    story.append(sp(6))

    data_kmeans = [
        ['Clúster', 'n', '%', 'Hora media', 'Duración (min)', 'Distancia (km)', 'Perfil'],
        ['C0', '18,154', '36.3', '6.9',  '10.6', '2.64',  'Commuter mañana'],
        ['C1',  '1,102',  '2.2', '14.1', '41.5', '17.95', 'Aeropuerto (28.2 km/h)'],
        ['C2',  '6,381', '12.8', '14.4', '31.4',  '7.46', 'Diurno largo'],
        ['C3', '24,363', '48.7', '18.3', '10.6',  '2.29', 'Tarde/noche central'],
    ]
    cw4 = [1.8*cm, 2*cm, 1.5*cm, 2.2*cm, 2.5*cm, 2.5*cm, 3*cm]
    story += tabla(data_kmeans, cw4, 'Tabla 4. Perfiles de los cuatro clústeres K-means (n = 50,000).')
    story.append(sp(6))

    story.append(p(
        'El clúster C1 es el más pequeño (2.2 %) pero el de mayor valor económico unitario: '
        'viajes de ≈ 18 km de distancia a una velocidad media de 28.2 km/h, coherente con rutas '
        'a JFK o LaGuardia fuera de congestión severa. C3 es el más grande (48.7 %) y representa '
        'el servicio urbano de proximidad en hora vespertina, con distancias medianas de 2.29 km.'))

    story.append(titulo_subseccion('4.2', 'DBSCAN: detección de ruido y zonas atípicas'))
    story.append(p(
        'DBSCAN (Density-Based Spatial Clustering of Applications with Noise) permite identificar '
        'clústeres de forma arbitraria y declarar explícitamente puntos de ruido, lo que no es '
        'posible con K-means. El hiperparámetro ε se determinó mediante la gráfica de la distancia '
        'al k-ésimo vecino más cercano (k = 5, percentil 95 de la distribución), que señala un '
        'codo pronunciado en ε = 0.10.'))
    story.append(p(
        'Con esta configuración, DBSCAN identificó 23 clústeres y clasificó 247 viajes (1.23 %) '
        'como ruido. El coeficiente de silueta sin incluir el ruido fue 0.0971, inferior al de '
        'K-means, lo que refleja la forma irregular de los clústeres de densidad frente a los '
        'convexos de K-means. Los 247 viajes de ruido presentan una velocidad media de 18.3 km/h '
        'frente a 14.3 km/h del resto: son viajes inusualmente rápidos en zonas de baja densidad, '
        'posiblemente trayectos exprés o errores residuales de GPS no capturados por los filtros '
        'de limpieza.'))
    story.append(sp(4))
    story += hallazgo_box(
        'El ruido detectado por DBSCAN no es aleatoriamente distribuido: se concentra en viajes '
        'de alta velocidad y zonas periféricas. Tratarlos con tarifa diferencial es operativamente '
        'justificable y mejora la eficiencia de asignación.')

    # ═══════════════════════════════════════════════════════
    # SECCIÓN 5 — GMM / EM
    # ═══════════════════════════════════════════════════════
    story.append(titulo_seccion('5', 'Mezclas gaussianas y algoritmo EM'))

    story.append(titulo_subseccion('5.1', 'Selección del número de componentes'))
    story.append(p(
        'El Modelo de Mezcla Gaussiana (GMM) asume que los datos provienen de K distribuciones '
        'gaussianas con mezcla latente p(x) = Σ π<sub>k</sub> N(x; μ<sub>k</sub>, Σ<sub>k</sub>). El número de componentes se '
        'seleccionó minimizando el Criterio de Información Bayesiano (BIC), que penaliza la '
        'verosimilitud por complejidad del modelo.'))
    story.append(sp(6))

    data_bic = [
        ['K', 'BIC'],
        ['2', '195,449'],
        ['3', '145,187'],
        ['4', '116,936.9   ← mínimo'],
        ['5', '118,440'],
    ]
    cw5 = [4*cm, 8*cm]
    story += tabla(data_bic, cw5, 'Tabla 5. BIC por número de componentes gaussianas.')
    story.append(sp(6))

    story.append(p(
        'El BIC cae de forma pronunciada de K = 2 a K = 4 y aumenta ligeramente para K = 5, '
        'señalando inequívocamente cuatro componentes como la solución óptima. El modelo final '
        'con K = 4 y matrices de covarianza completas (covariance_type=\'full\') convergió en '
        '26 iteraciones a una log-verosimilitud de −58,257.49.'))

    story.append(titulo_subseccion('5.2', 'Perfiles latentes de viaje'))
    story.append(p(
        'Las cuatro componentes del GMM corresponden a perfiles de viaje con interpretación '
        'directa en términos operativos, tal como se detalla en la Tabla 6.'))
    story.append(sp(6))

    data_gmm = [
        ['Perfil', 'π (%)', 'Duración (min)', 'Distancia (km)', 'Velocidad (km/h)'],
        ['Micro-urbano rápido',   '27.1',  '5.66',  '1.57',  '16.34'],
        ['Tráfico lento-corto',   '29.9',  '9.70',  '1.55',   '9.62'],
        ['Commuter medio',        '25.3', '18.43',  '3.71',  '12.32'],
        ['Largo alta velocidad',  '17.7', '27.80',  '9.13',  '22.75'],
    ]
    cw6 = [5*cm, 2.5*cm, 3*cm, 3*cm, 3*cm]
    story += tabla(data_gmm, cw6, 'Tabla 6. Perfiles de viaje según el GMM (K = 4, n = 50,000).')
    story.append(sp(6))

    story.append(p(
        'El perfil "Tráfico lento-corto" (29.9 %) agrupa viajes de distancia muy similar al '
        'micro-urbano (1.55 km frente a 1.57 km) pero con duración casi el doble (9.70 min), '
        'lo que implica velocidades promedio de 9.62 km/h y señala congestión severa. Desde el '
        'punto de vista operativo, un conductor en este perfil da prácticamente la misma vuelta '
        'geográfica que en el perfil rápido, pero tarda el doble: la diferencia entre ambos es '
        'la congestión, no la distancia. El perfil "Largo alta velocidad" (17.7 %) es el que '
        'presenta mayor distancia media (9.13 km) y velocidad (22.75 km/h), consistente con '
        'rutas a aeropuertos o conexiones inter-boroughs sin congestión.'))
    story.append(p(
        'El grado de asignación es alto: el 92.1 % de los viajes fue asignado a un perfil con '
        'responsabilidad > 0.9, y solo el 23.4 % registró alguna ambigüedad (r<sub>ik</sub> &lt; 0.9 para '
        'el componente dominante).'))

    story.append(titulo_subseccion('5.3', 'Algoritmo EM: pasos E y M'))
    story.append(p(
        'El algoritmo EM optimiza iterativamente la log-verosimilitud incompleta mediante dos '
        'pasos alternos. En el paso E (expectation), se calculan las responsabilidades:'))
    story.append(p(
        '<b>r<sub>ik</sub> = π<sub>k</sub> N(x<sub>i</sub>; μ<sub>k</sub>, Σ<sub>k</sub>) / Σ<sub>j</sub> π<sub>j</sub> N(x<sub>i</sub>; μ<sub>j</sub>, Σ<sub>j</sub>)</b>'))
    story.append(p(
        'cuyo denominador se calcula mediante log-sum-exp para evitar underflow. En el paso M '
        '(maximization), los parámetros se actualizan como:'))
    story.append(p(
        '<b>N<sub>k</sub> = Σ<sub>i</sub> r<sub>ik</sub>,   π<sub>k</sub> = N<sub>k</sub>/n,   μ<sub>k</sub> = (1/N<sub>k</sub>) Σ<sub>i</sub> r<sub>ik</sub> x<sub>i</sub>,   Σ<sub>k</sub> = (1/N<sub>k</sub>) Σ<sub>i</sub> r<sub>ik</sub> (x<sub>i</sub>−μ<sub>k</sub>)(x<sub>i</sub>−μ<sub>k</sub>)<sup>T</sup></b>'))
    story.append(p(
        'La monotonía de la convergencia garantiza ℓ<sup>(t+1)</sup> ≥ ℓ<sup>(t)</sup> en cada iteración. Una '
        'implementación manual del EM ejecutada sobre un subconjunto de diagnóstico confirmó esta '
        'propiedad: la log-verosimilitud pasó de −15,760 a −12,403 a lo largo de 10 iteraciones, '
        'una mejora de +3,357.39 puntos.'))

    story.append(titulo_subseccion('5.4', 'Sensibilidad a la inicialización'))
    story.append(p(
        'La inicialización determina en qué mínimo local converge el EM. La comparación entre '
        'dos estrategias mostró diferencias significativas:'))
    story.append(p('• <b>K-means++:</b> log-verosimilitud final = −58,279.57,  26 iteraciones.'))
    story.append(p('• <b>Aleatoria:</b> log-verosimilitud final = −59,549.22,  19 iteraciones.'))
    story.append(p(
        'La inicialización K-means++ supera a la aleatoria en +1,269.65 puntos de '
        'log-verosimilitud, confirmando que converge a un óptimo local de mejor calidad aunque '
        'requiera más iteraciones. La inicialización aleatoria alcanzó un mínimo local inferior '
        'y exhibe mayor variabilidad entre ejecuciones. En producción, K-means++ es la estrategia '
        'recomendada.'))

    # ═══════════════════════════════════════════════════════
    # SECCIÓN 6 — RECOMENDACIONES
    # ═══════════════════════════════════════════════════════
    story.append(titulo_seccion('6', 'Recomendaciones operativas'))
    story.append(p(
        'Los hallazgos de los tres bloques analíticos anteriores se integran en tres '
        'recomendaciones cuantificadas para UrbanMove.'))

    story.append(titulo_subseccion('6.1', 'Posicionamiento predictivo de conductores'))
    story.append(p(
        'El análisis de entropía zonal y los clústeres de K-means identificaron que las zonas '
        '33, 42 y 41 concentran el 88.2 % de la demanda en la franja tarde-noche (13–23 h). '
        'Con una demanda media de 5.7 rotaciones por hora por conductor en ese tramo, tres '
        'conductores posicionados simultáneamente en esas zonas cubrirían la demanda de forma '
        'sostenida sin necesidad de reposicionamiento frecuente.'))
    story.append(p(
        'La entropía condicional mínima en madrugada (H = 2.1325 bits) respalda el mismo '
        'principio para las horas nocturnas: en esa franja la demanda es geográficamente '
        'predecible, por lo que un único conductor bien posicionado puede atender la mayoría '
        'de los llamados con tiempos de espera aceptables.'))

    story.append(titulo_subseccion('6.2', 'Tarificación diferencial por perfil'))
    story.append(p(
        'El clúster C1 de K-means (aeropuerto, 2.2 % de viajes) presenta viajes de alto valor: '
        '17.95 km de distancia media y 28.2 km/h de velocidad, con disponibilidad del conductor '
        'comprometida durante ≈ 42 min. Para hacer estos viajes económicamente atractivos para el '
        'conductor y reflejar su verdadero costo de oportunidad, se recomienda aplicar un '
        'multiplicador de tarifa 2.5× respecto a la base. Los 247 viajes de ruido detectados por '
        'DBSCAN, que presentan velocidades medias de 18.3 km/h frente a 14.3 km/h del grueso del '
        'servicio, justifican un multiplicador de 1.25× por corresponder a recorridos atípicos '
        'en zonas periféricas o de baja densidad.'))

    story.append(titulo_subseccion('6.3', 'Modelos de demanda separados por régimen'))
    story.append(p(
        'La divergencia KL entre días laborables y fin de semana '
        '(KL(lab ‖ fds) = 0.163617 bits, KL(fds ‖ lab) = 0.180599 bits) cuantifica la '
        'incompatibilidad de ambas distribuciones. Un sistema de asignación que use el mismo '
        'modelo para ambos regímenes generará decisiones subóptimas: estimado en 1,327 despachos '
        'subóptimos por mes sobre la muestra analizada, extrapolable al sistema completo.'))
    story.append(p(
        'La solución es entrenar dos modelos separados: uno para días laborables con foco en '
        'los picos 7–9 h y 17–21 h (franjas de mayor demanda y menor dispersión zonal), y otro '
        'para fines de semana con cobertura extendida hasta las 3 h (la madrugada concentra una '
        'proporción mayor de viajes en fin de semana que en días laborables).'))
    story.append(sp(8))

    data_resumen = [
        ['Bloque', 'Métrica', 'Valor'],
        ['Información', 'H(zona)', '2.2693 bits'],
        ['Información', 'H(hora)', '4.4639 bits  (97.4 % del máx.)'],
        ['Información', 'I(hora ; zona)', '0.0440 bits'],
        ['Información', 'KL(lab ‖ fds)', '0.1636 bits'],
        ['K-means', 'Silueta (K=4)', '0.2916'],
        ['K-means', 'Inercia', '91,866'],
        ['K-means', 'Clúster aeropuerto (C1)', '2.2 % · 17.95 km'],
        ['DBSCAN', 'ε óptimo', '0.10'],
        ['DBSCAN', 'Clústeres detectados', '23'],
        ['DBSCAN', 'Ruido', '247 viajes  (1.23 %)'],
        ['GMM / EM', 'BIC mínimo (K=4)', '116,936.9'],
        ['GMM / EM', 'Log-verosimilitud final', '−58,257.49'],
        ['GMM / EM', 'Iteraciones convergencia', '26'],
        ['GMM / EM', 'Responsabilidad media', '92.1 %'],
    ]
    cw7 = [3.5*cm, 6*cm, 6*cm]
    story += tabla(data_resumen, cw7, 'Tabla 7. Resumen de métricas clave por bloque analítico.')

    # ═══════════════════════════════════════════════════════
    # SECCIÓN 7 — LIMITACIONES
    # ═══════════════════════════════════════════════════════
    story.append(titulo_seccion('7', 'Limitaciones y trabajo futuro'))
    story.append(p(
        'El análisis presenta tres limitaciones principales. En primer lugar, el dataset cubre '
        'únicamente el primer semestre de 2016; patrones estacionales del segundo semestre '
        '(otoño-invierno neoyorquino, con mayor precipitación y demanda de taxi en horas pico) '
        'no están representados, lo que puede sobreestimar la velocidad media y subestimar la '
        'duración en condiciones adversas.'))
    story.append(p(
        'En segundo lugar, el modelo no incorpora variables externas con alto poder predictivo: '
        'clima, eventos masivos (conciertos, partidos de la NFL, el Maratón de Nueva York) e '
        'incidencias de tráfico en tiempo real. Tercero, el GMM asume colas gaussianas que '
        'subestiman la frecuencia de viajes extremadamente largos; distribuciones de colas '
        'pesadas como la Student-t podrían capturar mejor ese extremo de la distribución.'))
    story.append(p(
        'Como trabajos futuros se identifican tres líneas prioritarias: (1) integración de '
        'señales de eventos en tiempo real para recalibrar dinámicamente los modelos de '
        'posicionamiento; (2) exploración de mezclas con distribuciones t de Student para mayor '
        'robustez ante viajes atípicos; y (3) conexión del módulo de perfiles de demanda con el '
        'algoritmo de asignación de conductores ya desarrollado, que actualmente opera de '
        'forma aislada.'))

    # ═══════════════════════════════════════════════════════
    # SECCIÓN 8 — CONCLUSIONES
    # ═══════════════════════════════════════════════════════
    story.append(titulo_seccion('8', 'Conclusiones'))
    story.append(p(
        'El análisis no supervisado del sistema de taxis de Nueva York revela una estructura '
        'latente de la demanda que no es observable a simple vista en el dataset crudo. La '
        'distribución por zonas exhibe baja entropía (45 % del máximo teórico), indicando que '
        'la demanda está geográficamente concentrada y es direccionable. La distribución horaria '
        'es casi uniforme (97.4 % del máximo), lo que exige un servicio activo en todo el '
        'espectro temporal pero con estrategias diferenciadas por franja.'))
    story.append(p(
        'La divergencia KL entre laborables y fin de semana es suficientemente grande para '
        'justificar modelos separados, y los cuatro perfiles de viaje identificados por el GMM '
        'tienen correlatos operativos claros que conectan directamente con decisiones de '
        'tarificación y posicionamiento.'))
    story.append(p(
        'En conjunto, los tres métodos no supervisados aplicados son complementarios: K-means '
        'proporciona segmentos duros con semántica operativa clara; DBSCAN detecta anomalías que '
        'K-means asimilaría como ruido silencioso; y el GMM captura la naturaleza continua y '
        'superpuesta de los patrones de viaje. La articulación de estos tres bloques con las '
        'métricas de información proporciona una base cuantificada para la toma de decisiones '
        'operativas de UrbanMove.'))

    # ── Construir ──────────────────────────────────────────
    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_page)
    print(f'PDF generado: {OUT_PATH}')

if __name__ == '__main__':
    build()
