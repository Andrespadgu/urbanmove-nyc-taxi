# Key Findings Walkthrough — UrbanMove: NYC Taxi Trip Duration
## ML No Supervisado · Universidad de La Sabana
**Duración del análisis completo:** ~11 minutos de presentación ejecutiva

Este documento recorre los cuatro bloques del análisis con el nivel de detalle suficiente para reproducir o defender cualquier número del proyecto.

---

## Estructura del análisis

| Bloque | Tema | Notebook |
|---|---|---|
| 1 | Contexto y preparación de datos | `00_data_prep.ipynb` |
| 2 | Incertidumbre e información | `01_informacion.ipynb` |
| 3 | Segmentación por partición | `02_clustering.ipynb` |
| 4 | Mezclas gaussianas y EM | `03_gmm_em.ipynb` |
| 5 | Recomendaciones operativas | `04_negocio_integracion.ipynb` |

---

## Bloque 1 — Contexto y datos

> "Nueva York, 2016. Un millón cuatrocientos cincuenta y ocho mil seiscientos cuarenta y cuatro viajes de taxi. UrbanMove no quiere saber cuántos hubo: quiere saber dónde va a ocurrir el siguiente. Esa pregunta tiene respuesta cuantitativa."

El dataset es NYC Taxi Trip Duration de Kaggle: coordenadas exactas de origen y destino, timestamps de pickup y dropoff, enero a junio de 2016.

De 1.4 millones de viajes se tomó una **muestra aleatoria de 50.000** (3.43%) con seed fija en 42. Antes de muestrear se aplicaron cinco filtros de limpieza. La distribución mensual del resultado tiene un coeficiente de variación del **4.3%** — cobertura uniforme de los seis meses.

---

## Bloque 2 — Incertidumbre e información

**Entropía de Shannon.** La entropía de zona de los 50.000 viajes es **2.27 bits** (45% del máximo posible de 5.04 bits con 33 zonas activas). Hay concentración moderada pero queda incertidumbre real.

Por franja horaria:
- **Madrugada: 2.13 bits** — los pocos viajes nocturnos van a sitios fijos.
- **Mañana pico: 2.34 bits** — los commuters salen desde múltiples barrios residenciales al mismo tiempo.

**Divergencia KL.** KL(laboral ‖ fin de semana) = **0.164 bits** → overhead del **3.71%** en cada decisión de despacho si se usa un modelo único. Las 7-8am tienen 3× más viajes laborales; la 1-2am tiene 4× más viajes de fin de semana.

**Información mutua hora-zona.** I(hora; zona) = **0.044 bits = 1.94%** de la incertidumbre total. La hora sola no basta para posicionar un conductor.

**log-sum-exp.** Estabilidad numérica crítica para el E-step del GMM: evita underflow en float64 cuando los log-likelihood llegan a −1000.

---

## Bloque 3 — Segmentación por partición

**K-Means.** K=4 elegido con codo de inercia (caída de 19.1% de K=3 a K=4, luego se aplana) + silueta 0.2916. K=2 tiene mejor silueta matemática (0.684) pero no produce perfiles operativos diferenciados.

| Cluster | % viajes | Hora media | Duración | Distancia |
|---|---|---|---|---|
| C0 Commuter mañana/madrugada | 36.3% | 6.9 h | 10.6 min | 2.64 km |
| C1 Aeropuerto / Periferia | 2.2% | 14.1 h | 41.5 min | 17.95 km |
| C2 Diurno largo | 12.8% | 14.4 h | 31.4 min | 7.46 km |
| C3 Tarde/Noche central | 48.7% | 18.3 h | 10.6 min | 2.29 km |

**DBSCAN.** ε = 0.10 calibrado con gráfica k-distancia (percentil 95). Resultado: 23 clusters, silueta 0.097, **247 puntos de ruido (1.23%)** con perfil de madrugada aislada y velocidad 18.3 km/h (vs. 14.3 km/h media). Tratamiento: tarifa +25% bajo demanda explícita.

---

## Bloque 4 — Mezclas gaussianas y EM

**Selección de K con BIC.** BIC cae de 195.450 en K=2 a 116.937 en K=4 (−78.500 pts). De K=4 a K=5 cae solo 18.000 — 77% menos de ganancia. K=4 es el codo del BIC.

**4 perfiles latentes** (con covarianza completa, K-means++):

| Perfil | π | Duración | Distancia | Velocidad |
|---|---|---|---|---|
| Micro-urbano rápido | 0.271 | 5.66 min | 1.57 km | 16.34 km/h |
| Tráfico lento-corto | 0.299 | 9.70 min | 1.55 km | 9.62 km/h |
| Commuter medio | 0.253 | 18.43 min | 3.71 km | 12.32 km/h |
| Largo alta velocidad | 0.177 | 27.80 min | 9.13 km | 22.75 km/h |

**EM manual.** Implementado en 10 iteraciones sobre 10.000 puntos: LL sube de −15.761 a −12.403 (+3.357), monótonamente — garantía matemática del algoritmo.

**Inicialización.** K-means++ (LL −58.280, BIC 116.937) vs. aleatoria (LL −59.549, BIC 119.520): diferencia de 2.583 puntos BIC. La aleatoria infla el componente lento-corto a 32% en lugar del real 27%.

**Viajes ambiguos.** 23.4% de viajes con responsabilidad máxima < 0.9 — genuinamente en frontera entre dos perfiles.

---

## Bloque 5 — Recomendaciones operativas

### Rec. 1 — Posicionamiento de conductores
17-22h concentra el 48.7% de la demanda. Las zonas 33, 42 y 41 capturan el **88.2%** de esa ventana. Con rotación de 5.7 viajes/conductor/hora se requieren ~3 conductores simultáneos en esas tres zonas para cubrir el 85% del turno.

*Limitación:* MI = 1.94% — la hora sola no predice la zona. Enriquecer con datos de eventos y clima.

### Rec. 2 — Tarificación diferenciada
C1 aeropuerto: distancia 7.8× mayor y duración 3.9× mayor que C3. Sin diferencial, el incentivo económico lleva conductores al centro. Propuesta: **multiplicador 2.5×** para C1, **1.25×** para los 247 viajes de ruido DBSCAN.

### Rec. 3 — Dos modelos de despacho
KL = 0.164 bits → 3.71% de overhead → **~1.327 despachos subóptimos** sobre las 35.756 predicciones laborales del sample. Modelo laboral: refuerzo 7-9h y 17-21h. Modelo fin de semana: cobertura activa hasta las 3am.

---

## Limitaciones honestas

- Datos de 2016 (prepandemia). Reentrenar con datos recientes de año completo.
- Sin variables externas: clima, eventos deportivos, conciertos.
- GMM asume distribuciones gaussianas — colas del cluster aeropuerto no capturadas correctamente. Alternativa: mezclas de Student-t.
- Grilla 8×8 gruesa (~3.2 × 6.1 km/celda). Siguiente paso: zonas TLC oficiales.
