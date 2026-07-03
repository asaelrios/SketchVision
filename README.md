# SketchVision Workbench for FreeCAD

[English](#english) | [Español](#español)

---

<a name="english"></a>
## English

SketchVision is a FreeCAD workbench designed for advanced image processing using OpenCV. It allows users to import images, adjust their display properties, and prepare them for computer vision tasks such as contour detection and tracing.

### Current Features
- **Real-time Processing**: Adjust brightness, contrast, gamma, and opacity.
- **Advanced Views**: Grayscale and Binarized modes with adjustable threshold.
- **Cleaning Filters**: Gaussian and Median Blur to reduce image noise.
- **3D Transformation**: Control scale (20%-200%), rotation (0-359°), and position (X, Y) directly from a task panel.
- **Native Integration**: Built with PySide6 and Coin3D for a smooth FreeCAD 1.x experience.

### Requirements
- FreeCAD 1.0 or higher.
- Python libraries: `opencv-python`, `numpy`, and `pivy`.

### Installation
1. Clone this repository into your FreeCAD user modules folder:
   - Windows: `%APPDATA%\FreeCAD\v1-1\Mod\`
2. Restart FreeCAD and select the **SketchVision** workbench.

---

<a name="español"></a>
## Español

SketchVision es un banco de trabajo para FreeCAD diseñado para el procesamiento avanzado de imágenes utilizando OpenCV. Permite importar imágenes, ajustar su visualización y prepararlas para tareas de visión artificial como detección de contornos y calcado.

### Características actuales
- **Procesamiento en tiempo real**: Ajuste de brillo, contraste, gamma y opacidad.
- **Vistas avanzadas**: Modos de escala de grises y binarización con umbral (threshold) ajustable.
- **Filtros de limpieza**: Desenfoque Gaussiano y Mediana para reducir ruido.
- **Transformación 3D**: Control de escala (20%-200%), rotación (0-359°) y posición (X, Y) directamente desde un panel lateral.
- **Integración Nativa**: Basado en PySide6 y Coin3D para una experiencia fluida en FreeCAD 1.x.

### Requisitos
- FreeCAD 1.0 o superior.
- Librerías de Python: `opencv-python`, `numpy` y `pivy`.

### Instalación
1. Clona este repositorio en tu carpeta de módulos de usuario de FreeCAD:
   - Windows: `%APPDATA%\FreeCAD\v1-1\Mod\`
2. Reinicia FreeCAD y selecciona el Workbench **SketchVision**.

---

## Roadmap / Próximos Pasos
- [ ] Canny Edge Detection / Detección de bordes Canny.
- [ ] Export shapes to FreeCAD Sketcher / Exportar formas al Sketcher de FreeCAD.
- [ ] Contour area filtering / Filtrado de contornos por área.
