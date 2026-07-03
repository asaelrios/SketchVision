# InitGui.py simplificado para diagnóstico
import FreeCAD as App
import FreeCADGui as Gui

class SketchVisionWorkbench(Gui.Workbench):
    MenuText = "SketchVision"
    ToolTip = "Procesamiento de imagen con OpenCV"
    
    def Initialize(self):
        """Se ejecuta al activar el workbench"""
        # Importamos los comandos aquí adentro para que si fallan, 
        # el workbench al menos aparezca en la lista.
        try:
            import SketchVision.freecad.commands.import_image
            self.appendToolbar("SketchVision Tools", ["ImportImageCommand"])
            App.Console.PrintLog("Comandos de SketchVision cargados.\n")
        except Exception as e:
            App.Console.PrintError(f"Error cargando comandos: {str(e)}\n")

    def GetClassName(self):
        return "Gui::PythonWorkbench"

# IMPORTANTE: Registramos la CLASE, no una instancia en algunas versiones
Gui.addWorkbench(SketchVisionWorkbench)

App.Console.PrintLog("SketchVision registrado en el sistema.\n")
