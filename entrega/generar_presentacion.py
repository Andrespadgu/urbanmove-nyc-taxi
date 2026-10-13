"""
Generador de presentación PPTX — UrbanMove NYC Taxi
Ejecutar: python entrega/generar_presentacion.py
Salida:   entrega/presentacion_urbanmove.pptx
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import os

# ──────────────────────────────────────────────
# PALETA DE COLORES
# ──────────────────────────────────────────────
C_DARK_BG    = RGBColor(0x0D, 0x1B, 0x2A)   # azul marino oscuro
C_ACCENT_1   = RGBColor(0x00, 0xB4, 0xD8)   # cian brillante
C_ACCENT_2   = RGBColor(0xFF, 0x9F, 0x1C)   # naranja ámbar
C_ACCENT_3   = RGBColor(0x4C, 0xAF, 0x50)   # verde
C_ACCENT_4   = RGBColor(0xF4, 0x43, 0x36)   # rojo
C_WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
C_LIGHT_GRAY = RGBColor(0xCC, 0xD6, 0xE0)
C_DARK_CARD  = RGBColor(0x16, 0x2A, 0x3A)   # card background

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

BLANK = prs.slide_layouts[6]  # completamente en blanco

def add_slide():
    return prs.slides.add_slide(BLANK)

def bg(slide, color=C_DARK_BG):
    """Rellena el fondo de una diapositiva."""
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        0, 0, prs.slide_width, prs.slide_height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_text(slide, text, left, top, width, height,
             font_size=18, bold=False, color=C_WHITE,
             align=PP_ALIGN.LEFT, wrap=True):
    txb = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    tf = txb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = "Calibri"
    return txb

def add_rect(slide, left, top, width, height, fill_color, line_color=None, line_width=0):
    shape = slide.shapes.add_shape(
        1, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(line_width)
    else:
        shape.line.fill.background()
    return shape

def add_pill(slide, text, left, top, width, height, bg_color, text_color=C_WHITE, font_size=13):
    """Rectángulo pequeño con texto centrado — estilo badge/pill."""
    add_rect(slide, left, top, width, height, bg_color)
    add_text(slide, text, left, top, width, height,
             font_size=font_size, bold=True, color=text_color, align=PP_ALIGN.CENTER)

def accent_bar(slide, color=C_ACCENT_1):
    """Barra de acento horizontal en la parte inferior."""
    add_rect(slide, 0, 7.1, 13.33, 0.07, color)

def slide_number(slide, n, total=17):
    add_text(slide, f"{n} / {total}", 12.2, 7.1, 1.0, 0.35,
             font_size=9, color=C_LIGHT_GRAY, align=PP_ALIGN.RIGHT)

def role_badge(slide, role_text, color):
    add_pill(slide, role_text, 0.4, 0.25, 1.8, 0.38, color, font_size=10)

# ══════════════════════════════════════════════
# SLIDE 1 — PORTADA / HOOK
# ══════════════════════════════════════════════
sl = add_slide()
bg(sl)
add_rect(sl, 0, 0, 13.33, 0.06, C_ACCENT_1)   # barra superior cian
add_rect(sl, 0, 7.44, 13.33, 0.06, C_ACCENT_2) # barra inferior naranja

add_text(sl, "¿A qué hora está tu conductor?",
         1.0, 1.6, 11.3, 1.4, font_size=44, bold=True,
         color=C_WHITE, align=PP_ALIGN.CENTER)

add_text(sl, "UrbanMove · NYC Taxi Trip Duration",
         1.0, 3.1, 11.3, 0.7, font_size=22,
         color=C_ACCENT_1, align=PP_ALIGN.CENTER)

add_text(sl, "ML No Supervisado · Universidad de La Sabana",
         1.0, 3.8, 11.3, 0.5, font_size=14,
         color=C_LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Métricas destacadas en la parte baja
stats = [
    ("1.4M", "viajes totales"),
    ("50K", "muestra limpia"),
    ("4", "roles · 4 métodos"),
    ("3", "recomendaciones"),
]
for i, (val, label) in enumerate(stats):
    x = 1.2 + i * 2.8
    add_rect(sl, x, 5.0, 2.3, 1.3, C_DARK_CARD)
    add_text(sl, val, x, 5.1, 2.3, 0.6, font_size=28, bold=True,
             color=C_ACCENT_2, align=PP_ALIGN.CENTER)
    add_text(sl, label, x, 5.65, 2.3, 0.5, font_size=11,
             color=C_LIGHT_GRAY, align=PP_ALIGN.CENTER)

slide_number(sl, 1)

# ══════════════════════════════════════════════
# SLIDE 2 — DATASET Y METODOLOGÍA
# ══════════════════════════════════════════════
sl = add_slide()
bg(sl)
accent_bar(sl, C_ACCENT_1)
role_badge(sl, "CONTEXTO", C_DARK_CARD)

add_text(sl, "El dataset y la metodología",
         0.4, 0.7, 12.5, 0.7, font_size=26, bold=True, color=C_WHITE)

# Pipeline visual
steps = [
    ("DATA PREP", "50K viajes\nCV=4.3%\nseed=42", C_ACCENT_1),
    ("ROL 1", "Teoría de\nInformación", RGBColor(0x5C, 0x6B, 0xC0)),
    ("ROL 2", "Clustering\nK-Means·DBSCAN", C_ACCENT_2),
    ("ROL 3", "GMM\nAlgoritmo EM", C_ACCENT_3),
    ("ROL 4", "Estrategia\nde Negocio", C_ACCENT_4),
]
for i, (title, desc, color) in enumerate(steps):
    x = 0.5 + i * 2.5
    add_rect(sl, x, 1.7, 2.1, 2.0, color)
    add_text(sl, title, x, 1.8, 2.1, 0.55, font_size=13, bold=True,
             color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(sl, desc, x, 2.4, 2.1, 1.1, font_size=10,
             color=C_WHITE, align=PP_ALIGN.CENTER)
    if i < 4:
        add_text(sl, "→", x + 2.1, 2.5, 0.4, 0.5, font_size=22,
                 color=C_LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Justificación muestreo
add_rect(sl, 0.4, 4.0, 12.5, 1.9, C_DARK_CARD)
add_text(sl, "Justificación del muestreo:",
         0.6, 4.05, 4.0, 0.4, font_size=12, bold=True, color=C_ACCENT_1)
add_text(sl,
    "NYC Taxi 2016 · 1.458.644 viajes · 50.000 extraídos (3.43%) · Muestreo aleatorio seed=42\n"
    "Filtros: duración >30s y <24h · coordenadas dentro de NYC · velocidad <75 km/h\n"
    "Distribución mensual CV=4.3% — cobertura uniforme enero–junio · Haversine, no euclidiana",
    0.6, 4.5, 12.1, 1.3, font_size=11, color=C_LIGHT_GRAY)

slide_number(sl, 2)

# ══════════════════════════════════════════════
# SLIDE 3 — ROL 1: ENTROPÍA DE SHANNON
# ══════════════════════════════════════════════
sl = add_slide()
bg(sl)
accent_bar(sl, RGBColor(0x5C, 0x6B, 0xC0))
role_badge(sl, "ROL 1 · INFORMACIÓN", RGBColor(0x5C, 0x6B, 0xC0))

add_text(sl, "Entropía de Shannon — ¿qué tan impredecible es la demanda?",
         0.4, 0.7, 12.5, 0.7, font_size=22, bold=True, color=C_WHITE)

# Fórmula
add_rect(sl, 0.4, 1.5, 5.8, 1.0, C_DARK_CARD)
add_text(sl, "H(X) = −Σ p(x) · log₂ p(x)  [bits]",
         0.6, 1.58, 5.4, 0.7, font_size=16, bold=True,
         color=C_ACCENT_1, align=PP_ALIGN.CENTER)

# Métricas entropía
metrics = [
    ("H(zone_id) global", "2.2693 bits", "33 zonas activas\n(máx = 5.04 bits)"),
    ("H(hour) global",    "4.4639 bits", "Dispersión horaria alta\n(máx = 4.58 bits)"),
    ("H(zone|madrugada)", "2.1325 bits ↓ MIN", "Franja más concentrada\n→ más predecible"),
    ("H(zone|mañana_pico)", "2.3438 bits ↑ MAX", "Commuters dispersos\n→ mayor cobertura"),
]
for i, (label, val, note) in enumerate(metrics):
    x = 0.4 + (i % 2) * 6.2
    y = 2.8 + (i // 2) * 1.9
    add_rect(sl, x, y, 5.9, 1.7, C_DARK_CARD)
    add_text(sl, label, x + 0.15, y + 0.1, 5.6, 0.45, font_size=11,
             color=C_LIGHT_GRAY)
    add_text(sl, val, x + 0.15, y + 0.5, 5.6, 0.6, font_size=18, bold=True,
             color=C_ACCENT_1)
    add_text(sl, note, x + 0.15, y + 1.1, 5.6, 0.5, font_size=10,
             color=C_LIGHT_GRAY)

slide_number(sl, 3)

# ══════════════════════════════════════════════
# SLIDE 4 — ROL 1: INFORMACIÓN MUTUA
# ══════════════════════════════════════════════
sl = add_slide()
bg(sl)
accent_bar(sl, RGBColor(0x5C, 0x6B, 0xC0))
role_badge(sl, "ROL 1 · INFORMACIÓN", RGBColor(0x5C, 0x6B, 0xC0))

add_text(sl, "Información Mutua — la hora NO predice la zona",
         0.4, 0.7, 12.5, 0.7, font_size=22, bold=True, color=C_WHITE)

# Gran número central
add_rect(sl, 3.5, 1.5, 6.3, 2.0, C_DARK_CARD)
add_text(sl, "I(hora ; zona) = 0.044 bits",
         3.5, 1.6, 6.3, 0.8, font_size=22, bold=True,
         color=C_ACCENT_2, align=PP_ALIGN.CENTER)
add_text(sl, "= 1.94% de la incertidumbre total de zona",
         3.5, 2.25, 6.3, 0.6, font_size=15,
         color=C_WHITE, align=PP_ALIGN.CENTER)
add_text(sl, "La hora del día reduce en menos del 2% la sorpresa de dónde ocurrirá el próximo viaje",
         3.5, 2.85, 6.3, 0.5, font_size=10,
         color=C_LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Interpretación
items = [
    ("✗ Hora sola", "Predice 1.94% de la zona\nNo es suficiente para despachar"),
    ("✗ Franja (6 grupos)", "Predice 1.37% de la zona\nAgrupar pierde información"),
    ("✓ Hora + variables", "Día semana + eventos + clima\nNecesario para predicción real"),
]
for i, (title, desc) in enumerate(items):
    x = 0.4 + i * 4.2
    add_rect(sl, x, 4.0, 3.9, 2.0, C_DARK_CARD)
    color = C_ACCENT_4 if "✗" in title else C_ACCENT_3
    add_text(sl, title, x + 0.15, 4.1, 3.6, 0.5, font_size=14, bold=True, color=color)
    add_text(sl, desc, x + 0.15, 4.65, 3.6, 1.1, font_size=11, color=C_LIGHT_GRAY)

slide_number(sl, 4)

# ══════════════════════════════════════════════
# SLIDE 5 — ROL 1: KL DIVERGENCE
# ══════════════════════════════════════════════
sl = add_slide()
bg(sl)
accent_bar(sl, RGBColor(0x5C, 0x6B, 0xC0))
role_badge(sl, "ROL 1 · INFORMACIÓN", RGBColor(0x5C, 0x6B, 0xC0))

add_text(sl, "Divergencia KL — Laboral vs. Fin de Semana",
         0.4, 0.7, 12.5, 0.7, font_size=22, bold=True, color=C_WHITE)

# Fórmula
add_rect(sl, 0.4, 1.5, 6.0, 0.9, C_DARK_CARD)
add_text(sl, "KL(P‖Q) = Σ P(h) · log₂[P(h)/Q(h)]",
         0.6, 1.58, 5.6, 0.65, font_size=14, bold=True,
         color=C_ACCENT_1, align=PP_ALIGN.CENTER)

# Resultado principal
add_rect(sl, 6.8, 1.5, 6.1, 0.9, C_DARK_CARD)
add_text(sl, "KL(laboral ‖ fds) = 0.1636 bits  →  overhead +3.71%",
         7.0, 1.58, 5.7, 0.65, font_size=13, bold=True,
         color=C_ACCENT_2, align=PP_ALIGN.CENTER)

# Tabla de horas divergentes
headers = ["Hora", "P(laboral)", "P(fin semana)", "Quién domina", "Ratio"]
rows = [
    ["h=07", "0.04553", "0.01404", "LABORAL ×3.2", "→ pico AM commuters"],
    ["h=08", "0.05621", "0.02261", "LABORAL ×2.5", "→ mayor hora laboral"],
    ["h=01", "0.01720", "0.05048", "FIN SEMANA ×2.9", "→ vida nocturna"],
    ["h=02", "0.01007", "0.04093", "FIN SEMANA ×4.1", "→ máxima divergencia noche"],
    ["h=00", "0.03026", "0.05532", "FIN SEMANA ×1.8", "→ medianoche fds"],
]

# Header tabla
col_w = [0.8, 1.2, 1.4, 1.9, 2.5]
col_x = [0.5, 1.4, 2.7, 4.2, 6.2]
y_header = 2.6
for j, (header, cw, cx) in enumerate(zip(headers, col_w, col_x)):
    add_rect(sl, cx, y_header, cw, 0.4, RGBColor(0x5C, 0x6B, 0xC0))
    add_text(sl, header, cx + 0.05, y_header, cw, 0.4, font_size=10,
             bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)

for ri, row in enumerate(rows):
    y = y_header + 0.45 + ri * 0.42
    row_color = C_DARK_CARD if ri % 2 == 0 else RGBColor(0x12, 0x22, 0x32)
    for j, (val, cw, cx) in enumerate(zip(row, col_w, col_x)):
        add_rect(sl, cx, y, cw, 0.38, row_color)
        text_col = C_ACCENT_4 if "LABORAL" in val else (C_ACCENT_2 if "FIN" in val else C_LIGHT_GRAY)
        add_text(sl, val, cx + 0.05, y, cw, 0.38, font_size=9,
                 color=text_col, align=PP_ALIGN.CENTER)

# Conclusión
add_rect(sl, 0.4, 5.2, 12.5, 1.5, C_DARK_CARD)
add_text(sl, "→ CONCLUSIÓN OPERATIVA",
         0.6, 5.28, 5.0, 0.4, font_size=12, bold=True, color=C_ACCENT_2)
add_text(sl,
    "Dos distribuciones incompatibles: mismo modelo genera overhead +3.71% por decisión.\n"
    "Laboral: pico 07-09h matutino pronunciado.  Fin de semana: actividad nocturna sostenida hasta 03h.\n"
    "UrbanMove necesita DOS POLÍTICAS DE DESPACHO distintas.",
    0.6, 5.68, 12.1, 1.0, font_size=10, color=C_LIGHT_GRAY)

slide_number(sl, 5)

# ══════════════════════════════════════════════
# SLIDE 6 — ROL 1: LOG-SUM-EXP + ENTROPÍA CRUZADA
# ══════════════════════════════════════════════
sl = add_slide()
bg(sl)
accent_bar(sl, RGBColor(0x5C, 0x6B, 0xC0))
role_badge(sl, "ROL 1 · INFORMACIÓN", RGBColor(0x5C, 0x6B, 0xC0))

add_text(sl, "log-sum-exp y Entropía Cruzada — puente hacia el GMM",
         0.4, 0.7, 12.5, 0.7, font_size=22, bold=True, color=C_WHITE)

# LSE
add_rect(sl, 0.4, 1.6, 6.1, 3.5, C_DARK_CARD)
add_text(sl, "log-sum-exp", 0.6, 1.7, 5.7, 0.5, font_size=16, bold=True,
         color=C_ACCENT_1)
add_text(sl, "lse(x) = c + log Σ exp(xᵢ − c),  c = max(x)",
         0.6, 2.2, 5.7, 0.5, font_size=12, bold=True, color=C_ACCENT_1)
lse_items = [
    ("Suma naïve  x=[-1000,-1001,-1002]", "→ exp(-1000) = 0 → log(0) = -∞  ✗"),
    ("log-sum-exp  x=[-1000,-1001,-1002]", "→ -999.5924  (error vs exacto: 0.00)  ✓"),
    ("Zonas procesadas:", "33  ·  error máx |lse-naive|: < 2×10⁻¹⁵"),
    ("En el E-step del GMM:", "densidades llegan a exp(-1000) → sin este truco → NaN"),
]
for i, (k, v) in enumerate(lse_items):
    y = 2.8 + i * 0.52
    add_text(sl, k, 0.6, y, 3.0, 0.45, font_size=10, color=C_LIGHT_GRAY)
    add_text(sl, v, 3.7, y, 2.6, 0.45, font_size=10, bold=True,
             color=C_ACCENT_3 if "✓" in v else (C_ACCENT_4 if "✗" in v else C_WHITE))

# Entropía cruzada
add_rect(sl, 6.8, 1.6, 6.1, 3.5, C_DARK_CARD)
add_text(sl, "Entropía Cruzada", 7.0, 1.7, 5.7, 0.5, font_size=16, bold=True,
         color=C_ACCENT_2)
add_text(sl, "H(P,Q) = −Σ P(h)·log₂Q(h)  =  H(P) + KL(P‖Q)",
         7.0, 2.2, 5.7, 0.5, font_size=11, bold=True, color=C_ACCENT_2)
ce_items = [
    ("H(laboral)  — costo propio óptimo:", "4.4124 bits"),
    ("KL(lab ‖ fds)  — costo por modelo erróneo:", "+0.1636 bits"),
    ("H(laboral, fds)  — costo total:", "4.5760 bits"),
    ("Overhead al usar modelo fds→laboral:", "+3.71 %"),
    ("Verificación H(P)+KL = H(P,Q):", "error < 1×10⁻¹⁵  ✓"),
]
for i, (k, v) in enumerate(ce_items):
    y = 2.8 + i * 0.52
    add_text(sl, k, 7.0, y, 4.0, 0.45, font_size=10, color=C_LIGHT_GRAY)
    add_text(sl, v, 11.0, y, 1.7, 0.45, font_size=11, bold=True,
             color=C_ACCENT_3 if "✓" in v else C_ACCENT_2)

# Síntesis
add_rect(sl, 0.4, 5.4, 12.5, 1.4, RGBColor(0x1A, 0x3A, 0x2A))
add_text(sl, "Síntesis Rol 1:",
         0.6, 5.48, 2.5, 0.4, font_size=12, bold=True, color=C_ACCENT_3)
add_text(sl,
    "H(zone)=2.27 bits · I(hora;zona)=0.044 bits (1.94%) · KL(lab‖fds)=0.164 bits (+3.71%)\n"
    "Madrugada = franja MÁS predecible (2.13 bits) · Mañana pico = MÁS dispersa (2.34 bits)",
    3.2, 5.48, 9.5, 1.3, font_size=10, color=C_LIGHT_GRAY)

slide_number(sl, 6)

# ══════════════════════════════════════════════
# SLIDE 7 — ROL 2: ELECCIÓN K=4
# ══════════════════════════════════════════════
sl = add_slide()
bg(sl)
accent_bar(sl, C_ACCENT_2)
role_badge(sl, "ROL 2 · CLUSTERING", C_ACCENT_2)

add_text(sl, "K-Means — Justificación de K=4",
         0.4, 0.7, 12.5, 0.7, font_size=22, bold=True, color=C_WHITE)

# Tabla inercia/silhouette
headers_k = ["K", "Inercia", "Reducción", "Silhouette", "¿Elegido?"]
rows_k = [
    ["2", "148,327", "—", "0.6844*", "No (demasiado grueso)"],
    ["3", "113,501", "23.5%", "0.2664", "No"],
    ["4",  "91,866", "19.1% ← codo", "0.2916 ✓", "SÍ"],
    ["5",  "76,213", "17.0%", "0.2683", "No"],
    ["6",  "67,166", "11.9%", "0.2826", "No"],
]
col_w2 = [0.5, 1.3, 1.8, 1.5, 3.0]
col_x2 = [0.4, 1.0, 2.4, 4.3, 5.9]
y_h2 = 1.6
for j, (hdr, cw, cx) in enumerate(zip(headers_k, col_w2, col_x2)):
    add_rect(sl, cx, y_h2, cw, 0.4, C_ACCENT_2)
    add_text(sl, hdr, cx + 0.04, y_h2, cw, 0.4, font_size=10,
             bold=True, color=C_DARK_BG, align=PP_ALIGN.CENTER)

for ri, row in enumerate(rows_k):
    y = y_h2 + 0.45 + ri * 0.45
    row_bg = RGBColor(0x12, 0x33, 0x1E) if ri == 2 else C_DARK_CARD
    for j, (val, cw, cx) in enumerate(zip(row, col_w2, col_x2)):
        add_rect(sl, cx, y, cw, 0.42, row_bg)
        col = C_ACCENT_3 if (ri == 2) else (C_ACCENT_4 if "No" in val else C_LIGHT_GRAY)
        add_text(sl, val, cx + 0.04, y, cw, 0.42, font_size=9,
                 bold=(ri == 2), color=col, align=PP_ALIGN.CENTER)

# Razón K=2 rechazado
add_rect(sl, 9.1, 1.6, 3.9, 1.7, C_DARK_CARD)
add_text(sl, "* K=2: silhouette = 0.684", 9.3, 1.7, 3.5, 0.4, font_size=11,
         bold=True, color=C_ACCENT_4)
add_text(sl,
    "Matemáticamente el mejor, pero\nsolo separa viajes de día vs noche.\nNo produce segmentos operativos.",
    9.3, 2.15, 3.5, 1.0, font_size=10, color=C_LIGHT_GRAY)

# Decisión
add_rect(sl, 9.1, 3.4, 3.9, 1.0, RGBColor(0x12, 0x33, 0x1E))
add_text(sl, "K=4 elegido: codo en 19.1% + 4 perfiles operativos distintos",
         9.3, 3.5, 3.5, 0.8, font_size=10, bold=True, color=C_ACCENT_3)

# Características del clustering
add_rect(sl, 0.4, 4.8, 8.5, 2.3, C_DARK_CARD)
add_text(sl, "Features K-Means (4 variables):",
         0.6, 4.9, 6.0, 0.4, font_size=12, bold=True, color=C_ACCENT_2)
add_text(sl,
    "pickup_longitude  ·  pickup_latitude  ·  hour  ·  duration_min\n"
    "→ capturan geografía de pickup + momento del día + duración del viaje\n"
    "→ StandardScaler antes de fitear (evita sesgo por magnitudes distintas)\n"
    "→ 50.000 puntos · seed=42 · n_init=10 · 8 iteraciones hasta convergencia",
    0.6, 5.35, 8.1, 1.65, font_size=10, color=C_LIGHT_GRAY)

slide_number(sl, 7)

# ══════════════════════════════════════════════
# SLIDE 8 — ROL 2: LOS 4 CLUSTERS
# ══════════════════════════════════════════════
sl = add_slide()
bg(sl)
accent_bar(sl, C_ACCENT_2)
role_badge(sl, "ROL 2 · CLUSTERING", C_ACCENT_2)

add_text(sl, "K-Means K=4 — Los 4 perfiles de demanda",
         0.4, 0.7, 12.5, 0.7, font_size=22, bold=True, color=C_WHITE)

clusters = [
    ("C0", "Commuter\nMañana", "36.3%", "18,154 viajes", "Hora media: 6.9h",
     "10.6 min · 2.64 km · 15.0 km/h", "Zona: 33 · lat=40.752", C_ACCENT_1),
    ("C1", "Aeropuerto /\nPeriferia", "2.2%", "1,102 viajes", "Hora media: 14.1h",
     "41.5 min · 17.95 km · 28.2 km/h", "Zona: 31 · lat=40.646", C_ACCENT_2),
    ("C2", "Viaje\nDiurno Largo", "12.8%", "6,381 viajes", "Hora media: 14.4h",
     "31.4 min · 7.46 km · 14.5 km/h", "Zona: 42 · lat=40.762", C_ACCENT_3),
    ("C3", "Tarde/Noche\nCentral", "48.7%", "24,363 viajes", "Hora media: 18.3h",
     "10.6 min · 2.29 km · 13.4 km/h", "Zona: 33 · lat=40.752", C_ACCENT_4),
]

for i, (code, name, pct, n, hora, metrics, geo, color) in enumerate(clusters):
    x = 0.3 + i * 3.25
    add_rect(sl, x, 1.5, 3.0, 5.5, C_DARK_CARD)
    add_rect(sl, x, 1.5, 3.0, 0.45, color)
    add_text(sl, code, x + 0.1, 1.52, 0.7, 0.4, font_size=14, bold=True,
             color=C_DARK_BG)
    add_text(sl, name, x + 0.85, 1.55, 2.0, 0.4, font_size=12, bold=True,
             color=C_DARK_BG)
    add_text(sl, pct, x + 0.1, 2.05, 2.8, 0.6, font_size=24, bold=True,
             color=color, align=PP_ALIGN.CENTER)
    add_text(sl, n, x + 0.1, 2.65, 2.8, 0.4, font_size=11,
             color=C_LIGHT_GRAY, align=PP_ALIGN.CENTER)
    add_text(sl, hora, x + 0.1, 3.1, 2.8, 0.4, font_size=11,
             color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(sl, metrics, x + 0.1, 3.6, 2.8, 0.6, font_size=9,
             color=C_LIGHT_GRAY, align=PP_ALIGN.CENTER)
    add_text(sl, geo, x + 0.1, 4.3, 2.8, 0.4, font_size=9,
             color=C_LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Insight clave
add_rect(sl, 0.3, 7.05, 12.7, 0.38, RGBColor(0x0D, 0x2A, 0x1E))
add_text(sl,
    "C0 + C3 = 85% del volumen (viajes cortos <11 min / <2.7 km en Manhattan central)  ·  "
    "C1 = tarifa 3–4× mayor  ·  Silhouette K=4 = 0.2916",
    0.5, 7.05, 12.3, 0.38, font_size=9, color=C_ACCENT_3, align=PP_ALIGN.CENTER)

slide_number(sl, 8)

# ══════════════════════════════════════════════
# SLIDE 9 — ROL 2: DBSCAN
# ══════════════════════════════════════════════
sl = add_slide()
bg(sl)
accent_bar(sl, C_ACCENT_2)
role_badge(sl, "ROL 2 · CLUSTERING", C_ACCENT_2)

add_text(sl, "DBSCAN — Hotspots y Zonas de Ruido",
         0.4, 0.7, 12.5, 0.7, font_size=22, bold=True, color=C_WHITE)

# Parámetros
add_rect(sl, 0.4, 1.5, 5.8, 1.1, C_DARK_CARD)
add_text(sl, "Parámetros elegidos: ε = 0.10 · min_samples = 5",
         0.6, 1.58, 5.4, 0.4, font_size=13, bold=True, color=C_ACCENT_2)
add_text(sl,
    "ε=0.10 = codo de gráfica k-distancia (k=5, p95 de distribución)\n"
    "20.000 puntos subsample · Features: pickup_lon, pickup_lat (StandardScaler)",
    0.6, 2.0, 5.4, 0.5, font_size=9, color=C_LIGHT_GRAY)

# Resultados DBSCAN
res_items = [
    ("Clusters encontrados", "23", "hotspots geográficos NYC", C_ACCENT_2),
    ("Silhouette (sin ruido)", "0.0971", "separación entre zonas densas", C_ACCENT_1),
    ("Puntos de RUIDO", "247  (1.23%)", "zonas periféricas atípicas", C_ACCENT_4),
]
for i, (label, val, note, color) in enumerate(res_items):
    x = 6.4 + i * 2.25
    add_rect(sl, x, 1.5, 2.1, 1.1, C_DARK_CARD)
    add_text(sl, val, x + 0.1, 1.55, 1.9, 0.55, font_size=18, bold=True,
             color=color, align=PP_ALIGN.CENTER)
    add_text(sl, label, x + 0.1, 2.1, 1.9, 0.3, font_size=8,
             color=C_LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Perfil de ruido vs normal
add_rect(sl, 0.4, 2.8, 12.5, 2.4, C_DARK_CARD)
add_text(sl, "Perfil de los 247 viajes de RUIDO vs viajes normales:",
         0.6, 2.88, 6.0, 0.4, font_size=12, bold=True, color=C_ACCENT_4)

headers_r = ["Métrica", "Ruido (n=247)", "Normales (n≈19,753)", "Diferencia"]
rows_r = [
    ["Hora media", "10.50h", "13.56h", "Más temprano"],
    ["Duración media", "15.60 min", "12.85 min", "+21% más largo"],
    ["Distancia media", "4.89 km", "3.19 km", "+53% más lejos"],
    ["Velocidad media", "18.3 km/h", "14.3 km/h", "+28% más rápido"],
    ["% fin de semana", "35.6%", "28.3%", "+7.3pp"],
    ["Franja dominante", "Madrugada (35%)", "Tarde pico", "Periférico nocturno"],
]
col_wr = [2.8, 2.3, 2.7, 2.7]
col_xr = [0.5, 3.4, 5.8, 8.6]
y_hr = 3.35
for j, (hdr, cw, cx) in enumerate(zip(headers_r, col_wr, col_xr)):
    add_rect(sl, cx, y_hr, cw, 0.35, RGBColor(0xAA, 0x33, 0x22))
    add_text(sl, hdr, cx, y_hr, cw, 0.35, font_size=9, bold=True,
             color=C_WHITE, align=PP_ALIGN.CENTER)

for ri, row in enumerate(rows_r):
    y = y_hr + 0.38 + ri * 0.35
    row_bg = C_DARK_CARD if ri % 2 == 0 else RGBColor(0x12, 0x22, 0x32)
    for j, (val, cw, cx) in enumerate(zip(row, col_wr, col_xr)):
        add_rect(sl, cx, y, cw, 0.32, row_bg)
        add_text(sl, val, cx, y, cw, 0.32, font_size=8, color=C_LIGHT_GRAY,
                 align=PP_ALIGN.CENTER)

# Recomendación
add_rect(sl, 0.4, 5.5, 12.5, 1.1, RGBColor(0x2A, 0x12, 0x12))
add_text(sl, "→ Política operativa DBSCAN:",
         0.6, 5.58, 3.5, 0.35, font_size=11, bold=True, color=C_ACCENT_4)
add_text(sl,
    "NO asignar conductores a zonas de ruido por defecto · Activar solo bajo demanda explícita\n"
    "Tarifa premium +25% para los 247 viajes periféricos (cubre overhead de reposicionamiento)",
    4.2, 5.58, 8.5, 0.98, font_size=10, color=C_LIGHT_GRAY)

slide_number(sl, 9)

# ══════════════════════════════════════════════
# SLIDE 10 — ROL 2: COMPARATIVA
# ══════════════════════════════════════════════
sl = add_slide()
bg(sl)
accent_bar(sl, C_ACCENT_2)
role_badge(sl, "ROL 2 · CLUSTERING", C_ACCENT_2)

add_text(sl, "K-Means vs DBSCAN — Comparativa y recomendación",
         0.4, 0.7, 12.5, 0.7, font_size=22, bold=True, color=C_WHITE)

# Tabla comparativa
add_rect(sl, 0.4, 1.5, 12.5, 3.8, C_DARK_CARD)
comp_data = [
    ["Criterio", "K-Means (K=4)", "DBSCAN (ε=0.10)", "Ganador"],
    ["Silhouette", "0.2916", "0.0971", "K-Means ✓"],
    ["Nº clusters", "4 (especificado)", "23 (automático)", "DBSCAN ✓"],
    ["% asignado", "100%", "98.77%", "K-Means ✓"],
    ["Detecta ruido", "No (forzado)", "Sí: 247 viajes", "DBSCAN ✓"],
    ["Muestra", "50,000", "20,000", "K-Means (mayor)"],
    ["Uso operativo", "Planif. de turnos", "Gestión de riesgo", "Complementarios"],
]
col_wc = [2.5, 2.8, 2.8, 4.2]
col_xc = [0.5, 3.1, 6.0, 8.9]
y_hc = 1.55
for j, (hdr, cw, cx) in enumerate(zip(comp_data[0], col_wc, col_xc)):
    add_rect(sl, cx, y_hc, cw, 0.4, C_ACCENT_2)
    add_text(sl, hdr, cx, y_hc, cw, 0.4, font_size=10, bold=True,
             color=C_DARK_BG, align=PP_ALIGN.CENTER)

for ri, row in enumerate(comp_data[1:]):
    y = y_hc + 0.42 + ri * 0.47
    row_bg = C_DARK_CARD if ri % 2 == 0 else RGBColor(0x12, 0x22, 0x32)
    for j, (val, cw, cx) in enumerate(zip(row, col_wc, col_xc)):
        add_rect(sl, cx, y, cw, 0.44, row_bg)
        text_c = C_ACCENT_3 if "✓" in val else C_LIGHT_GRAY
        add_text(sl, val, cx + 0.05, y, cw, 0.44, font_size=9,
                 color=text_c, align=PP_ALIGN.CENTER)

# Síntesis
add_rect(sl, 0.4, 5.5, 12.5, 1.5, RGBColor(0x12, 0x33, 0x1E))
add_text(sl, "Síntesis Rol 2:",
         0.6, 5.58, 2.5, 0.4, font_size=12, bold=True, color=C_ACCENT_3)
add_text(sl,
    "K=4 con Silhouette=0.2916 · C3 Tarde/Noche = 48.7% del volumen (foco posicionamiento 17h-22h)\n"
    "C1 Aeropuerto = 2.2% con 17.95 km/41.5 min (tarifa diferenciada) · DBSCAN: 247 zonas de ruido (1.23%)\n"
    "Las 3 zonas principales (33, 42, 41) cubren el 88.2% de la demanda 17-22h",
    3.2, 5.58, 9.5, 1.3, font_size=10, color=C_LIGHT_GRAY)

slide_number(sl, 10)

# ══════════════════════════════════════════════
# SLIDE 11 — ROL 3: SELECCIÓN K (BIC)
# ══════════════════════════════════════════════
sl = add_slide()
bg(sl)
accent_bar(sl, C_ACCENT_3)
role_badge(sl, "ROL 3 · GMM / EM", C_ACCENT_3)

add_text(sl, "GMM — Selección de K con criterio BIC",
         0.4, 0.7, 12.5, 0.7, font_size=22, bold=True, color=C_WHITE)

add_rect(sl, 0.4, 1.5, 6.0, 0.8, C_DARK_CARD)
add_text(sl, "p(x) = Σ πₖ · N(x | μₖ, Σₖ)  —  K=4, covariance_type='full'",
         0.6, 1.6, 5.6, 0.55, font_size=12, bold=True,
         color=C_ACCENT_3, align=PP_ALIGN.CENTER)

# Tabla BIC
bic_rows = [
    ["K=2", "195,449.6", "—", "No"],
    ["K=3", "145,187.6", "−50,262", "No"],
    ["K=4", "116,936.9", "−28,251  ← codo", "SÍ"],
    ["K=5",  "98,928.7", "−18,008", "No"],
    ["K=6",  "75,153.1", "−23,775", "No"],
]
col_wb = [1.0, 1.8, 2.5, 1.5]
col_xb = [0.4, 1.5, 3.4, 6.0]
y_hb = 2.5
headers_b = ["K", "BIC", "|ΔBIC|", "Elegido?"]
for j, (hdr, cw, cx) in enumerate(zip(headers_b, col_wb, col_xb)):
    add_rect(sl, cx, y_hb, cw, 0.38, C_ACCENT_3)
    add_text(sl, hdr, cx, y_hb, cw, 0.38, font_size=10, bold=True,
             color=C_DARK_BG, align=PP_ALIGN.CENTER)

for ri, row in enumerate(bic_rows):
    y = y_hb + 0.4 + ri * 0.47
    row_bg = RGBColor(0x12, 0x33, 0x1E) if ri == 2 else C_DARK_CARD
    for j, (val, cw, cx) in enumerate(zip(row, col_wb, col_xb)):
        add_rect(sl, cx, y, cw, 0.44, row_bg)
        col = C_ACCENT_3 if (ri == 2) else C_LIGHT_GRAY
        add_text(sl, val, cx, y, cw, 0.44, font_size=9, bold=(ri==2),
                 color=col, align=PP_ALIGN.CENTER)

# Justificación K=4
add_rect(sl, 7.8, 1.5, 5.1, 4.0, C_DARK_CARD)
add_text(sl, "¿Por qué K=4 y no K=2 o K=6?",
         8.0, 1.6, 4.7, 0.45, font_size=12, bold=True, color=C_ACCENT_3)
justif_items = [
    "BIC K=2→4: caída de 78,513 pts (41%)",
    "BIC K=4→5: solo −18,008 pts (−36% menos)",
    "A partir de K=4 el retorno marginal cae",
    "K=4 alinea con 4 perfiles reales NYC:",
    "  · Micro-urbano rápido",
    "  · Corto en tráfico",
    "  · Commuter",
    "  · Aeropuerto/largo",
    "GMM convergió en 26 iters (True)",
    "Log-likelihood final: −58,257",
]
for i, item in enumerate(justif_items):
    add_text(sl, item, 8.0, 2.15 + i * 0.31, 4.7, 0.28,
             font_size=9, color=C_LIGHT_GRAY)

slide_number(sl, 11)

# ══════════════════════════════════════════════
# SLIDE 12 — ROL 3: PERFILES LATENTES
# ══════════════════════════════════════════════
sl = add_slide()
bg(sl)
accent_bar(sl, C_ACCENT_3)
role_badge(sl, "ROL 3 · GMM / EM", C_ACCENT_3)

add_text(sl, "GMM K=4 — Los 4 perfiles latentes de viaje",
         0.4, 0.7, 12.5, 0.7, font_size=22, bold=True, color=C_WHITE)

perfiles = [
    ("C0", "Micro-urbano\nRápido", "27.1%", "5.66 min", "1.57 km", "16.34 km/h",
     "Downtown express\nAlta rotación", C_ACCENT_1),
    ("C2", "Tráfico\nLento-Corto", "29.9%", "9.70 min", "1.55 km", "9.62 km/h",
     "Misma dist que C0\ndoble tiempo (congest.)", C_ACCENT_2),
    ("C3", "Commuter\nMedio", "25.3%", "18.43 min", "3.71 km", "12.32 km/h",
     "Corredores\nresidenciales", RGBColor(0x9C, 0x27, 0xB0)),
    ("C1", "Largo Alta\nVelocidad", "17.7%", "27.80 min", "9.13 km", "22.75 km/h",
     "Aeropuerto /\nouter-boroughs", C_ACCENT_4),
]

for i, (code, name, pi, dur, dist, spd, note, color) in enumerate(perfiles):
    x = 0.3 + i * 3.25
    add_rect(sl, x, 1.5, 3.0, 5.5, C_DARK_CARD)
    add_rect(sl, x, 1.5, 3.0, 0.45, color)
    add_text(sl, code, x + 0.1, 1.52, 0.7, 0.4, font_size=14, bold=True, color=C_DARK_BG)
    add_text(sl, name, x + 0.85, 1.55, 2.0, 0.4, font_size=11, bold=True, color=C_DARK_BG)
    add_text(sl, f"π = {pi}", x + 0.1, 2.05, 2.8, 0.6, font_size=22, bold=True,
             color=color, align=PP_ALIGN.CENTER)
    for j, (lbl, val) in enumerate([("Duración", dur), ("Distancia", dist), ("Velocidad", spd)]):
        y = 2.75 + j * 0.65
        add_text(sl, lbl + ":", x + 0.15, y, 1.4, 0.5, font_size=10, color=C_LIGHT_GRAY)
        add_text(sl, val, x + 1.55, y, 1.3, 0.5, font_size=11, bold=True, color=C_WHITE)
    add_rect(sl, x + 0.1, 4.7, 2.8, 1.0, RGBColor(0x10, 0x20, 0x28))
    add_text(sl, note, x + 0.15, 4.75, 2.7, 0.9, font_size=9, color=C_ACCENT_3)

add_rect(sl, 0.3, 7.05, 12.7, 0.38, RGBColor(0x0D, 0x2A, 0x1E))
add_text(sl,
    "Micro-urbano + Lento-Corto = 57% del volumen (viajes <2 km)  ·  "
    "Largo Alta Velocidad = tarifa diferenciada  ·  "
    "Certeza media GMM: 92.1%  ·  Ambiguos: 23.4%",
    0.5, 7.05, 12.3, 0.38, font_size=9, color=C_ACCENT_3, align=PP_ALIGN.CENTER)

slide_number(sl, 12)

# ══════════════════════════════════════════════
# SLIDE 13 — ROL 3: EM MANUAL
# ══════════════════════════════════════════════
sl = add_slide()
bg(sl)
accent_bar(sl, C_ACCENT_3)
role_badge(sl, "ROL 3 · GMM / EM", C_ACCENT_3)

add_text(sl, "Algoritmo EM Manual — E-step, M-step, Convergencia",
         0.4, 0.7, 12.5, 0.7, font_size=22, bold=True, color=C_WHITE)

# E-step
add_rect(sl, 0.4, 1.5, 5.8, 2.4, C_DARK_CARD)
add_text(sl, "E-step — Calcular responsabilidades",
         0.6, 1.58, 5.4, 0.4, font_size=13, bold=True, color=C_ACCENT_1)
add_text(sl, "rᵢₖ = πₖ · N(xᵢ|μₖ,Σₖ) / Σⱼ πⱼ · N(xᵢ|μⱼ,Σⱼ)",
         0.6, 2.0, 5.4, 0.45, font_size=11, bold=True, color=C_ACCENT_1)
add_text(sl,
    "rᵢₖ = probabilidad de que el viaje i\npertenezca al perfil k\n"
    "→ log-sum-exp en el denominador\n  (evita underflow float64)",
    0.6, 2.5, 5.4, 1.3, font_size=10, color=C_LIGHT_GRAY)

# M-step
add_rect(sl, 6.6, 1.5, 6.3, 2.4, C_DARK_CARD)
add_text(sl, "M-step — Actualizar parámetros",
         6.8, 1.58, 5.9, 0.4, font_size=13, bold=True, color=C_ACCENT_2)
add_text(sl,
    "Nₖ = Σᵢ rᵢₖ        πₖ = Nₖ/N\n"
    "μₖ = Σᵢ rᵢₖ·xᵢ / Nₖ\n"
    "Σₖ = Σᵢ rᵢₖ·(xᵢ−μₖ)(xᵢ−μₖ)ᵀ / Nₖ",
    6.8, 2.0, 5.9, 0.85, font_size=11, bold=True, color=C_ACCENT_2)
add_text(sl,
    "Ponderadores = responsabilidades rᵢₖ\n→ viajes ambiguos contribuyen\n  proporcionalmente a varios perfiles",
    6.8, 2.88, 5.9, 0.9, font_size=10, color=C_LIGHT_GRAY)

# Tabla convergencia EM manual
add_rect(sl, 0.4, 4.1, 12.5, 0.42, C_DARK_CARD)
iter_headers = ["Iter", "Log-Likelihood", "ΔLLL", "Peso C0", "Peso C1", "Peso C2", "Peso C3"]
col_we = [0.5, 2.2, 1.8, 1.4, 1.4, 1.4, 1.4]
col_xe = [0.4, 1.0, 3.3, 5.2, 6.7, 8.2, 9.7]
y_he = 4.1
for j, (hdr, cw, cx) in enumerate(zip(iter_headers, col_we, col_xe)):
    add_rect(sl, cx, y_he, cw, 0.38, C_ACCENT_3)
    add_text(sl, hdr, cx, y_he, cw, 0.38, font_size=9, bold=True,
             color=C_DARK_BG, align=PP_ALIGN.CENTER)

em_rows = [
    ["0",  "−15,760.6", "—", "0.2143", "0.5822", "0.1567", "0.0468"],
    ["1",  "−14,695.8", "+1,064.8", "0.2128", "0.5686", "0.1671", "0.0515"],
    ["5",  "−13,239.5", "+253.4",  "0.2123", "0.4988", "0.2069", "0.0820"],
    ["10", "−12,403.2", "+143.7",  "0.2262", "0.4291", "0.2295", "0.1152"],
]
for ri, row in enumerate(em_rows):
    y = y_he + 0.4 + ri * 0.45
    row_bg = C_DARK_CARD if ri % 2 == 0 else RGBColor(0x12, 0x22, 0x32)
    for j, (val, cw, cx) in enumerate(zip(row, col_we, col_xe)):
        add_rect(sl, cx, y, cw, 0.42, row_bg)
        add_text(sl, val, cx, y, cw, 0.42, font_size=8.5, color=C_LIGHT_GRAY,
                 align=PP_ALIGN.CENTER)

add_rect(sl, 0.4, 6.4, 12.5, 0.75, RGBColor(0x12, 0x33, 0x1E))
add_text(sl,
    "Ganancia total en 10 iteraciones: +3,357 puntos LL  ·  "
    "Propiedad garantizada del EM: L(θ⁽ᵗ⁺¹⁾) ≥ L(θ⁽ᵗ⁾) siempre  ·  "
    "No es suerte: es convergencia monótona garantizada matemáticamente",
    0.6, 6.48, 12.1, 0.6, font_size=10, bold=True, color=C_ACCENT_3)

slide_number(sl, 13)

# ══════════════════════════════════════════════
# SLIDE 14 — ROL 3: INICIALIZACIÓN
# ══════════════════════════════════════════════
sl = add_slide()
bg(sl)
accent_bar(sl, C_ACCENT_3)
role_badge(sl, "ROL 3 · GMM / EM", C_ACCENT_3)

add_text(sl, "Inicialización — K-means++ vs. Aleatoria",
         0.4, 0.7, 12.5, 0.7, font_size=22, bold=True, color=C_WHITE)

# Comparativa
comp_init = [
    ("K-MEANS++", "−58,279.57", "26 iteraciones", "116,937", "No", C_ACCENT_3),
    ("ALEATORIA",  "−59,549.22", "19 iteraciones", "119,520", "SÍ  (LL inferior en +1,270 pts)", C_ACCENT_4),
]
for i, (method, ll, iters, bic, local, color) in enumerate(comp_init):
    x = 0.4 + i * 6.4
    add_rect(sl, x, 1.5, 6.1, 2.8, C_DARK_CARD)
    add_rect(sl, x, 1.5, 6.1, 0.42, color)
    add_text(sl, method, x + 0.2, 1.53, 5.7, 0.38, font_size=15, bold=True,
             color=C_DARK_BG, align=PP_ALIGN.CENTER)
    for j, (lbl, val) in enumerate([("Log-Likelihood final", ll),
                                     ("Iteraciones hasta conv.", iters),
                                     ("BIC final", bic),
                                     ("¿Mínimo local?", local)]):
        y = 2.05 + j * 0.55
        add_text(sl, lbl + ":", x + 0.2, y, 3.0, 0.45, font_size=10, color=C_LIGHT_GRAY)
        add_text(sl, val, x + 3.3, y, 2.6, 0.45, font_size=11, bold=True,
                 color=color if j in [0, 3] else C_WHITE)

# Explicación mínimos locales
add_rect(sl, 0.4, 4.5, 12.5, 2.6, C_DARK_CARD)
add_text(sl, "¿Qué son los mínimos locales en el EM?",
         0.6, 4.58, 6.0, 0.42, font_size=13, bold=True, color=C_ACCENT_3)
add_text(sl,
    "El EM maximiza la log-verosimilitud LOCALMENTE — el punto de partida determina a qué 'valle' llega.\n"
    "Inicialización aleatoria: convergió en 19 iters pero a LL=−59,549 (mínimo local de baja calidad)\n"
    "K-means++ tarda 7 iters más pero llega a LL=−58,280 — el 'valle más profundo' disponible\n"
    "Diferencia de BIC: 116,937 vs 119,520 = 2,583 puntos — solución aleatoria tergiversa pesos\n"
    "  (Lento-Corto sube artificialmente de 27% a 32% con inicialización aleatoria)",
    0.6, 5.05, 12.1, 1.95, font_size=10, color=C_LIGHT_GRAY)

slide_number(sl, 14)

# ══════════════════════════════════════════════
# SLIDE 15 — ROL 4: LAS 3 RECOMENDACIONES
# ══════════════════════════════════════════════
sl = add_slide()
bg(sl)
accent_bar(sl, C_ACCENT_4)
role_badge(sl, "ROL 4 · NEGOCIO", C_ACCENT_4)

add_text(sl, "3 Recomendaciones Operativas Cuantificadas",
         0.4, 0.7, 12.5, 0.7, font_size=22, bold=True, color=C_WHITE)

recs = [
    ("1", "Posicionamiento\nde Conductores",
     "Turno 17h–22h", "C3=48.7%  ·  Zonas 33, 42, 41",
     "Las 3 zonas cubren el 88.2% de\nla demanda tarde-noche (17-22h)\n~3 conductores en simultáneo necesarios",
     "I(hora;zona)=1.94% → cruzar\nhora + día semana + eventos",
     C_ACCENT_1),
    ("2", "Tarificación\nDiferenciada",
     "C1 aeropuerto", "2.2% de viajes  ·  17.95 km / 41.5 min",
     "Multiplicador 2.5x para C1\n(7.8x más distancia, 3.9x más tiempo)\n+1.25x para 247 viajes ruido DBSCAN",
     "Sin diferenciación: conductor C1\npaga 3.9x más tiempo por el mismo\ningreso → incentivo perverso",
     C_ACCENT_2),
    ("3", "Modelos Separados\nLaboral / Fin de Semana",
     "KL = 0.164 bits", "+3.71% overhead con modelo único",
     "h=07-09am: 3x más viajes laborales\nh=01-03am: 4x más viajes fds\n~1,327 despachos sub-óptimos/muestra",
     "23.4% viajes GMM ambiguos se\nresuelven con contexto lab/fds\nDos modelos: evita overhead 3.71%",
     C_ACCENT_3),
]

for i, (num, title, subtitle, kpi, action, note, color) in enumerate(recs):
    x = 0.3 + i * 4.35
    add_rect(sl, x, 1.5, 4.1, 5.6, C_DARK_CARD)
    add_rect(sl, x, 1.5, 0.55, 5.6, color)   # barra lateral color
    add_text(sl, num, x + 0.1, 1.7, 0.4, 0.6, font_size=20, bold=True,
             color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(sl, title, x + 0.65, 1.58, 3.35, 0.55, font_size=13, bold=True, color=color)
    add_text(sl, subtitle, x + 0.65, 2.15, 3.35, 0.38, font_size=10,
             bold=True, color=C_ACCENT_2)
    add_text(sl, kpi, x + 0.65, 2.55, 3.35, 0.45, font_size=9, color=C_LIGHT_GRAY)
    add_rect(sl, x + 0.65, 3.1, 3.35, 1.6, RGBColor(0x10, 0x20, 0x28))
    add_text(sl, "ACCIÓN:", x + 0.75, 3.15, 3.1, 0.35, font_size=9,
             bold=True, color=C_ACCENT_3)
    add_text(sl, action, x + 0.75, 3.5, 3.1, 1.15, font_size=9, color=C_WHITE)
    add_text(sl, note, x + 0.65, 4.8, 3.35, 1.1, font_size=8.5, color=C_LIGHT_GRAY)

slide_number(sl, 15)

# ══════════════════════════════════════════════
# SLIDE 16 — TABLA RESUMEN EJECUTIVA
# ══════════════════════════════════════════════
sl = add_slide()
bg(sl)
accent_bar(sl, C_ACCENT_4)
role_badge(sl, "ROL 4 · NEGOCIO", C_ACCENT_4)

add_text(sl, "Tabla Ejecutiva — Los 4 roles, los números clave",
         0.4, 0.7, 12.5, 0.7, font_size=22, bold=True, color=C_WHITE)

exec_data = [
    ["Rol", "Método", "Número clave", "Decisión operativa"],
    ["Data Prep", "Muestreo aleatorio\nseed=42", "50K viajes\nCV mensual=4.3%", "Dataset reproducible\ncobertura uniforme"],
    ["Rol 1\nInformación", "Entropía·KL·MI\nlog-sum-exp", "I(hora;zona)=0.044b\nKL=0.164b (+3.71%)", "Hora sola insuficiente\nDos modelos horarios"],
    ["Rol 2\nClustering", "K-Means K=4\nDBSCAN ε=0.10", "Silhouette=0.2916\n247 ruido (1.23%)", "C3=48.7% foco tarde\nC1 tarifa 2.5x"],
    ["Rol 3\nGMM/EM", "GMM K=4\nEM manual 10 iters", "BIC=116,937\nLL: +3,357 pts en 10it", "4 perfiles latentes\nK-means++ evita loc.mín"],
    ["Rol 4\nNegocio", "Integración\n3 recomendaciones", "88.2% demand.\n~1,327 despachos +", "Posic. + Tarifa + Modelos\n→ sistema de decisión"],
]

col_we2 = [1.5, 2.5, 2.6, 3.0]
col_xe2 = [0.3, 1.9, 4.5, 7.2]
y_he2 = 1.5
for j, (hdr, cw, cx) in enumerate(zip(exec_data[0], col_we2, col_xe2)):
    add_rect(sl, cx, y_he2, cw, 0.42, C_ACCENT_4)
    add_text(sl, hdr, cx, y_he2, cw, 0.42, font_size=10, bold=True,
             color=C_DARK_BG, align=PP_ALIGN.CENTER)

role_colors = [C_ACCENT_1, RGBColor(0x5C, 0x6B, 0xC0), C_ACCENT_2, C_ACCENT_3, C_ACCENT_4]
for ri, row in enumerate(exec_data[1:]):
    y = y_he2 + 0.44 + ri * 0.9
    add_rect(sl, col_xe2[0], y, col_we2[0], 0.86, role_colors[ri])
    add_text(sl, row[0], col_xe2[0], y, col_we2[0], 0.86, font_size=10,
             bold=True, color=C_DARK_BG, align=PP_ALIGN.CENTER)
    for j in range(1, 4):
        row_bg = C_DARK_CARD if ri % 2 == 0 else RGBColor(0x12, 0x22, 0x32)
        add_rect(sl, col_xe2[j], y, col_we2[j], 0.86, row_bg)
        add_text(sl, row[j], col_xe2[j] + 0.08, y, col_we2[j], 0.86,
                 font_size=9, color=C_LIGHT_GRAY)

slide_number(sl, 16)

# ══════════════════════════════════════════════
# SLIDE 17 — CIERRE
# ══════════════════════════════════════════════
sl = add_slide()
bg(sl)
add_rect(sl, 0, 0, 13.33, 0.08, C_ACCENT_2)
add_rect(sl, 0, 7.42, 13.33, 0.08, C_ACCENT_1)

add_text(sl, "No es una exploración académica.",
         1.0, 1.4, 11.3, 1.0, font_size=34, bold=True,
         color=C_WHITE, align=PP_ALIGN.CENTER)
add_text(sl, "Es un sistema de decisión.",
         1.0, 2.3, 11.3, 0.9, font_size=34, bold=True,
         color=C_ACCENT_2, align=PP_ALIGN.CENTER)

add_text(sl,
    "50.000 viajes  ·  4 métodos  ·  3 recomendaciones con número\n"
    "Implementables sin recopilar un solo dato adicional",
    1.0, 3.3, 11.3, 0.7, font_size=15,
    color=C_LIGHT_GRAY, align=PP_ALIGN.CENTER)

# 3 cifras clave
final_stats = [
    ("88.2%", "demanda cubierta\ncon 3 zonas (17-22h)"),
    ("2.5×", "tarifa C1 aeropuerto\n(7.8× más distancia)"),
    ("+3.71%", "overhead evitable\ncon 2 modelos horarios"),
]
for i, (val, label) in enumerate(final_stats):
    x = 1.5 + i * 3.7
    add_rect(sl, x, 4.2, 3.2, 1.8, C_DARK_CARD)
    add_text(sl, val, x, 4.3, 3.2, 0.9, font_size=28, bold=True,
             color=C_ACCENT_2, align=PP_ALIGN.CENTER)
    add_text(sl, label, x, 5.15, 3.2, 0.7, font_size=11,
             color=C_LIGHT_GRAY, align=PP_ALIGN.CENTER)

add_text(sl, "ML No Supervisado · Universidad de La Sabana",
         1.0, 6.4, 11.3, 0.4, font_size=11,
         color=C_LIGHT_GRAY, align=PP_ALIGN.CENTER)

slide_number(sl, 17)

# ──────────────────────────────────────────────
# GUARDAR
# ──────────────────────────────────────────────
output_path = os.path.join(os.path.dirname(__file__), "presentacion_urbanmove.pptx")
prs.save(output_path)
print(f"Presentación guardada en: {output_path}")
print(f"Total de diapositivas: {len(prs.slides)}")
