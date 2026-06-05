# TP_Integrador_BDDII


Descargar PIP INSTALL streamlit
Para correr pagina web: streamlit run app_web.py
Descargar pip install redis

Para concectar con Neo4j:
Se debe ir a Neo4j desktop, crear una isntancia con usuario por defecto y contrasena cursusNeo4j, y tamebin instalar neo4j en python (pip install neo4j)

Funciones de motores

Mongo DB:

¿Para qué lo usamos?
MongoDB actúa como nuestro repositorio principal y archivo histórico ("Data Lake"). Al ser una base de datos orientada a documentos, nos permite almacenar todo el gran volumen de datos del dataset original de manera flexible. Es el motor ideal para lectura masiva y analítica de datos estáticos o históricos.

Funcionalidades principales:
Búsquedas y Filtros (Consultas Simples): Filtramos rápidamente la colección para encontrar caballos específicos (ej. por nombre, por peso menor a 1000 libras, o por entrenador).
Agregación y Estadísticas (Consultas Complejas): Realizamos cálculos sobre la totalidad de los datos, como obtener el Top 10 de tiempos más rápidos históricos o calcular promedios de tiempo globales y por entrenador.
Perfiles Individuales: Generamos un historial completo de un caballo específico en base a su nombre, calculando su efectividad y total de carreras jugadas/ganadas.

Redis (Motor Clave-Valor) - Simulación y Tiempo Real

¿Para qué lo usamos?
Redis es nuestra base de datos "en memoria" (In-Memory). A diferencia de Mongo, no lo usamos para guardar datos para siempre, sino para gestionar el estado efímero y la alta velocidad. Es el motor perfecto para simular la acción del momento y manejar datos que cambian constantemente.

Funcionalidades principales:
Simulación en Vivo: Creamos "carreras activas" cargando los participantes temporalmente. Utilizamos los *Sorted Sets* de Redis para simular la carrera vuelta a vuelta, actualizando el puntaje y el ranking en tiempo real de forma hiper-eficiente.
Sistema de Apuestas: Generamos apuestas ficticias asociadas a la carrera viva. Una vez finalizada la simulación, el sistema procesa instantáneamente qué apuestas fueron ganadas o perdidas.
Manejo de Estados Temporales: Aprovechamos la función nativa de expiración de Redis (`EXPIRE`). Una vez que la carrera termina y se pagan las apuestas, todos los datos temporales (participantes, ranking, apuestas) se "autodestruyen" luego de una hora, manteniendo nuestra memoria RAM limpia y optimizada.