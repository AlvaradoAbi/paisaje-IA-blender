# paisaje-IA-blender
Generador de paisaje 3D en Blender con KMeans (aprendizaje no supervisado)
# Generador de Paisajes 3D con KMeans en Blender

Este proyecto utiliza técnicas de aprendizaje no supervisado para crear un paisaje tridimensional procedural en Blender. Mediante el algoritmo **KMeans**, se clasifican regiones del terreno según sus coordenadas y se les asigna diferentes características naturales como montañas, lagos, praderas y bosques.

## 🌄 Características

- Terreno procedural generado a partir de un plano subdividido.
- Uso de **KMeans** para clasificar regiones en 4 zonas naturales.
- Generación automática de altura, color y objetos naturales según zona.
- Insertado de árboles, rocas y agua según lógica del terreno.
- Integración completa con **Python y Blender**.

## 🧠 Inteligencia Artificial

Este proyecto aplica el algoritmo **KMeans** (Scikit-learn) como técnica de **aprendizaje no supervisado**, agrupando los vértices del plano en 4 clusters. Cada uno representa un tipo de bioma:

- Cluster 0 → Pradera
- Cluster 1 → Montaña
- Cluster 2 → Lago
- Cluster 3 → Bosque

## 📝 Requisitos

- Blender 3.6+ (con Python habilitado)
- `scikit-learn`, `numpy`
  (Se puede instalar en Blender con consola de scripts)

## 📂 Archivos incluidos

- `blender_paisaje_IA.py`: Código completo en Python para ejecutar en Blender.
- `informe_COM300.pdf`: Documento detallado del proyecto.
- Carpeta `media/`: Capturas de pantalla y resultados visuales.

## 📸 Imágenes del resultado

*(Agregar aquí las imágenes más bonitas del paisaje generado)*

## 📚 Créditos

Proyecto desarrollado por **Betsabel Abigail Alvarado Choque**  
Materia: COM300 - Inteligencia Artificial Aplicada  
Docente: [Nombre del docente]  
Año: 2025
