# SketchVision Workbench for FreeCAD

SketchVision es un banco de trabajo para FreeCAD diseñado para el procesamiento avanzado de imágenes utilizando OpenCV. Permite importar imágenes, ajustar su visualización y prepararlas para tareas de visión artificial como detección de contornos y calcado.

## Características actuales
- **Procesamiento en tiempo real**: Ajuste de brillo, contraste, gamma y opacidad.
- **Vistas avanzadas**: Modos de escala de grises y binarización con umbral (threshold) ajustable.
- **Filtros de limpieza**: Desenfoque Gaussiano y Mediana para reducir ruido.
- **Transformación 3D**: Control de escala, rotación y posición (X, Y) del plano de imagen directamente desde un panel lateral.
- **Integración Nativa**: Basado en PySide6 y Coin3D para una experiencia fluida en FreeCAD 1.x.

## Requisitos
- FreeCAD 1.0 o superior.
- Python con las librerías: `opencv-python` y `numpy`.

## Instalación
1. Clona este repositorio en tu carpeta de módulos de usuario de FreeCAD:
   - Windows: `%APPDATA%\FreeCAD\v1-1\Mod\`
2. Reinicia FreeCAD y selecciona el Workbench **SketchVision**.

## Próximos Pasos
- Detección de contornos (Canny Edge Detection).
- Exportación de formas detectadas a Sketcher de FreeCAD.
