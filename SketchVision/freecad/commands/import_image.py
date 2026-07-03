import FreeCAD as App
import FreeCADGui as Gui

class ImportImageCommand:
    """Comando que lanza el panel de SketchVision"""

    def GetResources(self):
        # Std_Import es un icono que existe en casi todas las versiones
        return {
            'Pixmap': 'Std_Import', 
            'MenuText': 'Abrir Panel SketchVision',
            'ToolTip': 'Abre el panel de procesamiento de imagen'
        }

    def Activated(self):
        from ..ui.image_panel import show_panel
        show_panel()
            
    def IsActive(self):
        return App.ActiveDocument is not None

Gui.addCommand('ImportImageCommand', ImportImageCommand())
