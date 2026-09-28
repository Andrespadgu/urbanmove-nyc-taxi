# Guion Video — UrbanMove: NYC Taxi Trip Duration
## ML No Supervisado · Universidad de La Sabana · 2026-II
**Duración total:** ~11 minutos (dentro del rango permitido 10–12 min)

---

## ESTRUCTURA OFICIAL (según rúbrica)

| Seg. | Denominación | Responsable | Tiempo |
|---|---|---|---|
| 1 | Contexto y datos | **Persona 4 (Rol 4)** | 0:00–1:30 |
| 2 | Incertidumbre e información | **Persona 1 (Rol 1)** | 1:30–4:00 |
| 3 | Segmentación por partición | **Persona 2 (Rol 2)** | 4:00–6:30 |
| 4 | Mezclas y variables latentes | **Persona 3 (Rol 3)** | 6:30–9:00 |
| 5 | Recomendaciones y cierre | **Persona 4 (Rol 4)** | 9:00–11:00 |

---

## SEGMENTO 1 — CONTEXTO Y DATOS (Persona 4 · 0:00–1:30)

**[Slide 1 — portada con pregunta de negocio]**

> "Nueva York, 2016. Un millón cuatrocientos cincuenta y ocho mil seiscientos cuarenta y cuatro viajes de taxi. UrbanMove no quiere saber cuántos hubo: quiere saber dónde va a ocurrir el siguiente. Esa pregunta tiene respuesta cuantitativa — y eso es lo que vamos a demostrar hoy."

**[Slide 2 — dataset y justificación del muestreo]**

> "El dataset es NYC Taxi Trip Duration de Kaggle: coordenadas exactas de origen y destino, timestamps de pickup y dropoff, enero a junio de 2016. Lo elegimos porque tiene la granularidad que necesitan los cuatro análisis que siguen: hora del viaje, zona geográfica, distancia y velocidad."

> "De 1.4 millones de viajes tomamos una **muestra aleatoria de 50.000** — el 3.43% — con seed fija en 42 para garantizar reproducibilidad. Antes de muestrear aplicamos cinco filtros: eliminamos viajes con duración menor a 30 segundos o mayor a 24 horas, coordenadas fuera del bounding-box de NYC, velocidades implausibles por encima de 75 km/h, y duplicados de ID. La distribución mensual del resultado tiene un coeficiente de variación del **4.3%** — cobertura uniforme de los seis meses."

> "Sobre esa muestra calculamos seis variables derivadas: distancia Haversine entre origen y destino, duración en minutos, velocidad promedio, hora del día, indicador de fin de semana, franja horaria en seis categorías, y zona geográfica en grid. Con eso trabajaron los tres roles que vienen a continuación."

---

## SEGMENTO 2 — INCERTIDUMBRE E INFORMACIÓN (Persona 1 · 1:30–4:00)

**[Slide 3 — Entropía de Shannon por zona y horario]**

> "Mi rol fue medir la incertidumbre de la demanda usando teoría de la información. El primer concepto: **entropía de Shannon**. La fórmula es H(X) = −Σ p(x)·log₂ p(x), medida en bits."

> "La **entropía de zona** de los 50.000 viajes es **2.27 bits**. Para interpretarlo: si los viajes se repartieran perfectamente entre las 33 zonas activas, la entropía sería log₂(33) = 5.04 bits — el máximo posible. Que sea 2.27 significa que hay concentración moderada, pero queda incertidumbre real: no podemos predecir la zona de un viaje solo por existir."

> "Por **franja horaria**: la **madrugada tiene la menor entropía de zona, 2.13 bits** — los pocos viajes nocturnos van a sitios fijos como Manhattan central y aeropuertos. La **mañana pico tiene la mayor, 2.34 bits** — los commuters salen desde múltiples barrios residenciales al mismo tiempo, la demanda está más dispersa."

**[Slide 4 — KL entre contextos: laboral vs fin de semana]**

> "Segundo concepto: **divergencia KL**. Compara dos distribuciones horarias — días laborales contra fin de semana. La fórmula es KL(P‖Q) = Σ P(h)·log₂[P(h)/Q(h)]. El resultado: **KL(laboral ‖ fin de semana) = 0.164 bits**."

> "¿Qué significa operativamente? Si UrbanMove usa un modelo horario entrenado en fin de semana para gestionar un día laboral, paga un **overhead del 3.71%** en cada decisión de despacho. Las horas más divergentes: a las 7 y 8 de la mañana hay **tres veces más viajes laborales** que en fin de semana — los commuters. A la 1 y 2 de la madrugada hay **cuatro veces más viajes de fin de semana** — la vida nocturna. Son distribuciones incompatibles."

> "La KL es **asimétrica**: KL(fin de semana ‖ laboral) = 0.181 bits — ligeramente mayor, porque el modelo laboral sorprende más ante las madrugadas activas del fin de semana que al revés."

**[Slide 5 — Información Mutua hora-zona y log-sum-exp]**

> "Tercer concepto: **información mutua** entre la hora del día y la zona de recogida. I(hora; zona) = H(zona) − H(zona | hora). El resultado: **0.044 bits, el 1.94%** de la incertidumbre total de zona."

> "Eso quiere decir que saber a qué hora ocurre un viaje reduce en menos del 2% la sorpresa sobre en qué zona va a ocurrir. La hora sola no basta para posicionar un conductor. UrbanMove necesita cruzar la hora con el día de semana, los eventos de la ciudad y el clima."

> "Cuarto concepto — el más técnico pero relevante para el siguiente bloque: **log-sum-exp**. Cuando el GMM del Rol 3 calcula responsabilidades en el paso E, los log-likelihood de puntos alejados de todos los centroides llegan a valores como −1000. Suma naïve: exp(−1000) → 0 → log(0) → infinito negativo. Con el truco — restar el máximo antes de exponenciar — el resultado es **−999.59, con error menor a 2×10⁻¹⁵**. Sin esto el algoritmo EM colapsa con NaN."

---

## SEGMENTO 3 — SEGMENTACIÓN POR PARTICIÓN (Persona 2 · 4:00–6:30)

**[Slide 6 — Justificación de K=4 (codo + silhouette)]**

> "Mi rol comparó dos métodos de clustering: **K-Means y DBSCAN**. Primero K-Means. El número de clusters no se elige arbitrariamente — se justifica con dos criterios simultáneos: el codo de inercia y la silhouette."

> "Probé K de 2 a 12. El **codo de inercia** aparece en K=4: la inercia cae un 19.1% de K=3 a K=4, pero solo un 17% de K=4 a K=5 — la curva se aplana. La **silhouette en K=4 es 0.2916**, mejor que K=5 (0.268) y K=6 (0.283). El pico de silhouette matemático está en K=2 con 0.684, pero K=2 solo genera dos grupos: 'viajes de día' y 'viajes de noche'. No produce segmentos operativos diferenciados. Por eso elegí K=4."

**[Slide 7 — Los 4 clusters K-Means con números propios]**

> "K=4 produce cuatro perfiles medidos sobre los 50.000 viajes reales. **Cluster C0 — Commuter Mañana**: 36.3% del volumen, hora media 6.9h, 10.6 minutos, 2.64 km. **Cluster C3 — Tarde/Noche Central**: 48.7%, hora media 18.3h, 10.6 minutos, 2.29 km. Juntos son el **85% de la demanda** — viajes cortos en el centro de Manhattan. **Cluster C2 — Diurno Largo**: 12.8%, 31.4 minutos, 7.46 km — turismo y negocios. **Cluster C1 — Aeropuerto/Periferia**: solo el 2.2% pero con una distancia media de **17.95 km y 41.5 minutos** — cuatro veces la duración de un viaje típico."

**[Slide 8 — DBSCAN: hiperparámetros, validación y ruido]**

> "Segundo método: **DBSCAN**. Aquí no se especifica K — el algoritmo lo determina solo. El hiperparámetro crítico es **ε**, el radio de vecindad. Lo calibré con la **gráfica k-distancia** (k=5): ordeno los puntos por su quinta distancia al vecino más cercano y busco el codo. El codo aparece en **ε=0.10** — percentil 95 de la distribución. Con ε=0.05 obtengo 39 clusters y 3% de ruido: demasiado fino. Con ε=0.25 quedan 6 clusters: demasiado grueso. ε=0.10 da **23 clusters y 1.23% de ruido**."

> "La silhouette de DBSCAN sin puntos de ruido es **0.097** — más baja que K-Means porque hay un cluster dominante con 18.443 de los 19.753 viajes asignados. DBSCAN no es el ganador para segmentación operativa."

> "Los **247 puntos de ruido** son pickups en zonas geográficamente aisladas, sin vecinos suficientes en radio ε. Su perfil: sobrerepresentados en madrugada (35% vs 28.5% en viajes normales), velocidad promedio 18.3 km/h contra 14.3 km/h en zonas densas — menor tráfico, pero acceso costoso para el conductor. Tratamiento operativo: **tarifa premium del 25%** para viajes con origen en zona de ruido, activación solo bajo demanda explícita."

---

## SEGMENTO 4 — MEZCLAS Y VARIABLES LATENTES (Persona 3 · 6:30–9:00)

**[Slide 9 — Por qué GMM: selección K con BIC]**

> "El clustering del segmento anterior asigna cada viaje a exactamente un grupo — decisión rígida. El **GMM** va más lejos: asigna a cada viaje una **probabilidad de pertenencia** a cada perfil. El 23.4% de los viajes tienen una certeza máxima menor al 90% — están genuinamente en la frontera entre dos tipos de viaje. Para esos, la asignación suave es más honesta."

> "Elegí K con el criterio **BIC**, que penaliza la complejidad del modelo. El BIC cae de 195.450 en K=2 a 116.937 en K=4 — una reducción de 78.500 puntos. De K=4 a K=5 solo cae 18.000 — un 77% menos de ganancia por componente adicional. **K=4 es el codo del BIC**. El modelo convergió en **26 iteraciones** con log-verosimilitud total de **−58.257**."

**[Slide 10 — Los 4 perfiles latentes con parámetros propios]**

> "Con K=4 y covarianza completa, el GMM descubrió estos perfiles sin que nadie se los indicara: **Micro-urbano Rápido** — 27.1% de los viajes, media de 5.66 minutos, 1.57 km, 16.3 km/h — taxi express de Manhattan. **Tráfico Lento-Corto** — 29.9%, misma distancia pero 9.70 minutos y solo 9.6 km/h — exactamente el mismo trayecto que el anterior, pero atascado. **Commuter Medio** — 25.3%, 18.4 minutos, 3.71 km. **Largo Alta Velocidad** — 17.7%, 27.8 minutos, 9.13 km a 22.75 km/h — aeropuerto o barrios periféricos."

> "La covarianza del componente largo es la más grande — diagonal de 2.27, 2.30, 2.02 — lo que indica que los viajes largos son mucho más variables entre sí que los viajes cortos."

**[Slide 11 — E-step / M-step con parámetros propios y convergencia]**

> "Implementé el algoritmo EM **manualmente** sobre 10.000 puntos para mostrar los pasos. El **E-step** calcula las responsabilidades: r_ik = πₖ · N(xᵢ|μₖ,Σₖ) dividido entre la suma sobre todos los componentes. El log-sum-exp del Rol 1 estabiliza este denominador."

> "El **M-step** actualiza: el peso πₖ = N_k/N, la media μₖ como promedio ponderado por responsabilidades, y la covarianza Σₖ como varianza ponderada. Los ponderadores son exactamente las responsabilidades — un viaje ambiguo contribuye proporcionalmente a varios componentes."

> "La curva de convergencia: **la log-verosimilitud sube en cada iteración sin excepción**. De −15.761 en la iteración 0 a −12.403 en la iteración 10 — ganancia de +3.357 puntos. Los deltas se desaceleran: +1.065 en la iteración 1, +144 en la iteración 10. Esto no es suerte — es la **garantía matemática del EM**: L(θ⁽ᵗ⁺¹⁾) ≥ L(θ⁽ᵗ⁾) siempre."

**[Slide 12 — Comparación de inicializaciones: mínimos locales]**

> "El EM converge a un **óptimo local**. Con **inicialización aleatoria**: convergió en 19 iteraciones a LL = −59.549. Con **K-means++**: 26 iteraciones, LL = −58.280. K-means++ es **1.270 puntos mejor** de log-verosimilitud. El BIC de la solución aleatoria es 119.520 contra 116.937 de K-means++ — 2.583 puntos peor, lo cual indica que la aleatoria quedó atrapada en un mínimo local de menor calidad. La diferencia en los pesos: la aleatoria infla artificialmente el componente Lento-Corto a 32% cuando el real es 27%."

---

## SEGMENTO 5 — RECOMENDACIONES Y CIERRE (Persona 4 · 9:00–11:00)

**[Slide 13 — Recomendación 1: Posicionamiento de conductores]**

> "Los tres bloques anteriores se tradujeron en tres decisiones concretas. **Recomendación 1 — Posicionamiento**: el análisis de K-Means muestra que entre las 17 y las 22 horas, el 48.7% de toda la demanda cae en el cluster C3. De esa demanda tarde-noche, las tres zonas con mayor densidad — zona 33, 42 y 41 — concentran el **88.2%**. Para cubrir el 85% del turno, con rotación media de 5.7 viajes por conductor por hora en ventana de 5 horas, se necesitan **aproximadamente 3 conductores en simultáneo** en esas tres zonas."

> "La limitación: la información mutua I(hora;zona) = 1.94% nos dice que la hora sola no predice bien la zona. Esta recomendación necesita enriquecerse con datos de eventos de la ciudad y condiciones climáticas para mejorar la precisión."

**[Slide 14 — Recomendación 2: Tarificación diferenciada]**

> "**Recomendación 2 — Tarificación**: el cluster C1 aeropuerto/periferia tiene distancia 7.8 veces mayor y duración 3.9 veces mayor que el viaje central C3. Sin tarifa diferenciada, un conductor que acepta 41.5 minutos de viaje gana menos por hora que uno que hace cuatro viajes de 10.6 minutos — un incentivo perverso que deteriora la cobertura de zonas alejadas. Proponemos **multiplicador 2.5x** para C1 (techo comercial sobre el 6.27x matemático) y **1.25x para los 247 viajes de ruido DBSCAN**, que cubre el overhead del 25% de tiempo de reposicionamiento."

**[Slide 15 — Recomendación 3: Dos modelos de despacho + limitaciones]**

> "**Recomendación 3 — Dos modelos horarios**: la divergencia KL entre laboral y fin de semana es 0.164 bits, equivalente a un overhead del 3.71% en cada predicción. Sobre las 35.756 predicciones laborales del sample, eso son **aproximadamente 1.327 despachos sub-óptimos**. Las horas 1-3am tienen 4 veces más viajes en fin de semana; las 7-9am tienen 3 veces más laborales. Modelo laboral: refuerzo 7-9h y 17-21h, reducción nocturna. Modelo fin de semana: sin pico matutino, flota activa hasta las 3am."

> "El 23.4% de viajes ambiguos del GMM se beneficia directamente de estos dos modelos: un viaje de 10 minutos y 2 km en madrugada laboral es probablemente un Commuter de turno temprano; el mismo viaje en madrugada de fin de semana es probablemente un regreso de ocio nocturno."

**[Slide 16 — Limitaciones y siguientes pasos]**

> "Tres limitaciones honestas del análisis. Primera: **la muestra es de 2016** — los patrones de movilidad post-pandemia en NYC son distintos. Cualquier implementación requiere reentrenar con datos recientes. Segunda: **no incluimos variables externas** — clima, eventos deportivos, conciertos — que podrían mejorar el poder predictivo de hora y zona más allá del 1.94% actual de MI. Tercera: **el GMM asume distribuciones gaussianas** — los viajes de aeropuerto tienen colas pesadas que una gaussiana no captura perfectamente."

> "Siguientes pasos: incorporar datos de eventos en tiempo real para enriquecer el modelo de posicionamiento; extender el GMM con distribuciones de cola pesada (mezclas de Student-t); y conectar las recomendaciones con el algoritmo de asignación en tiempo real para validar el impacto operativo real."

> "El análisis de 50.000 viajes con cuatro herramientas entrega **números defendibles y decisiones accionables**. Todo lo que necesita UrbanMove está en los primeros seis meses de 2016 — y en los cuatro notebooks que acabamos de presentar."

---

## NOTAS DE PRODUCCIÓN

**Transiciones oficiales entre segmentos:**
- Seg 1 → Seg 2: "Eso es el contexto. Ahora el primer análisis: ¿qué tan impredecible es la demanda de por sí?"
- Seg 2 → Seg 3: "Medimos la incertidumbre. El siguiente paso: identificar los grupos dentro de esa demanda."
- Seg 3 → Seg 4: "K-Means asigna cada viaje a un solo grupo. El siguiente bloque pregunta: ¿y si un viaje pertenece parcialmente a dos?"
- Seg 4 → Seg 5: "Cuatro perfiles, convergencia garantizada. ¿Qué hacemos con eso operativamente?"

**Tiempos por slide (referencia):**
- Seg 1: Slides 1–2 (~45 seg cada uno)
- Seg 2: Slides 3–5 (~50 seg cada uno)
- Seg 3: Slides 6–8 (~50 seg cada uno)
- Seg 4: Slides 9–12 (~37 seg cada uno)
- Seg 5: Slides 13–16 (~30 seg cada uno)

**Preguntas de defensa oral — por segmento:**

*Seg 1 (Rol 4):*
1. "¿Por qué 50.000 y no todo el dataset?" → CV=4.3%, suficiencia estadística, tiempo <5 min.
2. "¿Qué es seed=42 y por qué importa?" → Reproducibilidad: el mismo código da siempre el mismo resultado.

*Seg 2 (Rol 1):*
3. "¿Qué significa 2.27 bits de entropía?" → 45% del máximo posible (5.04 bits). Concentración moderada, no dominancia total.
4. "¿Por qué la KL no es simétrica?" → Las distribuciones P y Q juegan roles distintos: P es la real, Q es el modelo aproximado.
5. "¿Qué significa MI=1.94%?" → La hora sola explica menos del 2% de la incertidumbre de zona — casi independientes.
6. "¿Por qué se necesita log-sum-exp?" → Underflow en float64: exp(-1000)=0, log(0)=-∞, EM colapsa. El truco evita esto.

*Seg 3 (Rol 2):*
7. "¿Por qué K=4 si K=2 tiene mejor silhouette?" → K=2 no es operativamente útil: solo separa día/noche, sin perfiles accionables.
8. "¿Cómo elegiste ε en DBSCAN?" → Gráfica k-distancia (k=5): el codo visual en ε=0.10 corresponde al percentil 95.
9. "¿Qué haces con el 1.23% de ruido?" → No se asigna a flota estándar. Tarifa +25% bajo demanda explícita.

*Seg 4 (Rol 3):*
10. "¿Qué es el E-step y el M-step?" → E: calculo cuánto 'pertenece' cada viaje a cada perfil. M: actualizo los parámetros usando esas pertenencias como pesos.
11. "¿Por qué la convergencia del EM es garantizada?" → Cada M-step maximiza el bound inferior de la log-verosimilitud, así que L nunca puede bajar.
12. "¿Qué es un mínimo local en el EM?" → El EM llega al mejor valle del paisaje de log-verosimilitud desde donde empieza. Si empieza mal, llega a un valle local inferior.

*Seg 5 (Rol 4):*
13. "¿Cuáles son las limitaciones del análisis?" → Datos de 2016, sin variables externas (clima/eventos), gaussianas pueden no capturar colas del cluster aeropuerto.
14. "¿Cómo priorizarías las tres recomendaciones?" → Primero el posicionamiento (mayor impacto en volumen: 88.2% de la demanda). Segundo los modelos separados (evita 1.327 errores/ciclo). Tercero la tarificación (afecta solo el 3.43% del volumen pero mejora margen por conductor).
