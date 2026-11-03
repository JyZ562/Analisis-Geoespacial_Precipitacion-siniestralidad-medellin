# Influencia de la precipitación y la pendiente en la siniestralidad vial del Distrito de Medellín (2022–2024)

**Autor:** Jorge Andres Vivas Moreno — Ingeniero Civil e Ingeniero Sanitario · Especialización en Recursos Hídricos  
**Curso:** Análisis Geoespacial · Prof. Edier Vicente Aristizábal Giraldo · Semestre 2026-02  
Departamento de Geociencias y Medio Ambiente · Facultad de Minas · Universidad Nacional de Colombia, Sede Medellín

## Pregunta de investigación

¿La precipitación y la pendiente del terreno aumentan la ocurrencia y la gravedad de los siniestros viales en Medellín, y en qué zonas de la ciudad es mayor ese efecto?

## Datos

| Tipo | Capa | Fuente |
|---|---|---|
| Punto (0D) | Siniestros viales 2022–2024 (IPAT) | Secretaría de Movilidad de Medellín |
| Punto (0D) | Estaciones pluviométricas (precipitación diaria) | SIATA / IDEAM |
| Área (2D) | Comunas y barrios | GeoMedellín |
| Superficie (3D) | Raster de pendientes del terreno (%) | — |

Cada siniestro toma el valor de pendiente de la celda donde ocurrió, junto con la lluvia del día.

## Contenido

- [`presentacion/`](presentacion/) — presentación de la propuesta (PowerPoint).
- [`datos/estaciones_pluviometricas/`](datos/estaciones_pluviometricas/) — series diarias de precipitación de 81 estaciones SIATA (ZIP con CSV) e inventario de estaciones SIATA, IDEAM y EPM (Word).
- [`datos/siniestros/`](datos/siniestros/) — bases de siniestralidad vial y de mortalidad 2022–2024 de la Secretaría de Movilidad de Medellín (CSV y Excel).
  - [`datos/siniestros/depurados/`](datos/siniestros/depurados/) — las mismas bases sin los registros que no tienen coordenadas (siniestralidad: 79.467 de 85.793; mortalidad: 795 de 836).
