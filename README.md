# Procesar Alertas de Valdomir

Procesa automáticamente alertas de Google sobre Sebastián Valdomir y las guarda en Airtable.

## Cómo funciona

1. Google Alerts llega a tu Gmail
2. Make.com captura el email
3. Envía a este webhook en Vercel
4. Se extrae: título, URL, medio
5. Se guarda en Airtable

## Despliegue en Vercel

1. Andá a https://vercel.com/import
2. Selecciona este repositorio
3. Vercel automáticamente detectará la configuración
4. Hacé click en "Deploy"

El URL final será: https://procesar-alertas-valdomir.vercel.app/api/process
