import FreeCAD as App
import FreeCADGui as Gui
import os
from pivy import coin

class SketchVisionObject:
    def __init__(self, obj):
        obj.addProperty("App::PropertyPath", "ImagePath", "Base", "Ruta original")
        obj.addProperty("App::PropertyPath", "ProcessedPath", "Base", "Ruta procesada").ProcessedPath = ""
        obj.addProperty("App::PropertyPlacement", "Placement", "Base", "Ubicación")
        obj.Placement = App.Placement()
        
        # Visión
        obj.addProperty("App::PropertyFloat", "Brightness", "Vision").Brightness = 0.0
        obj.addProperty("App::PropertyFloat", "Contrast", "Vision").Contrast = 0.0
        obj.addProperty("App::PropertyFloat", "Gamma", "Vision").Gamma = 1.0
        obj.addProperty("App::PropertyFloat", "Opacity", "Display").Opacity = 1.0
        obj.addProperty("App::PropertyInteger", "Threshold", "Vision").Threshold = 0
        
        # Geometría
        obj.addProperty("App::PropertyFloat", "BaseWidth", "Internal").BaseWidth = 100.0
        obj.addProperty("App::PropertyFloat", "BaseHeight", "Internal").BaseHeight = 100.0
        obj.addProperty("App::PropertyFloat", "Width", "Geometry").Width = 100.0
        obj.addProperty("App::PropertyFloat", "Height", "Geometry").Height = 100.0
        obj.addProperty("App::PropertyFloat", "Scale", "Transform").Scale = 100.0
        
        obj.Proxy = self

    def execute(self, obj):
        pass

class ViewProviderSketchVision:
    def __init__(self, vobj):
        vobj.Proxy = self

    def attach(self, vobj):
        self.ViewObject = vobj
        self.Object = vobj.Object
        self.root = coin.SoSeparator()
        
        self.transform = coin.SoTransform()
        self.texture = coin.SoTexture2()
        # MODO REPLACE: Muestra el color real de la imagen sin sombras de FreeCAD
        self.texture.model = coin.SoTexture2.REPLACE
        
        self.material = coin.SoMaterial()
        self.material.diffuseColor = (1, 1, 1) # Blanco puro por si acaso
        
        self.coords = coin.SoCoordinate3()
        self.face = coin.SoFaceSet()
        
        self.transp_type = coin.SoTransparencyType()
        self.transp_type.value = coin.SoTransparencyType.SORTED_OBJECT_BLEND
        
        self.root.addChild(self.transform)
        self.root.addChild(self.transp_type)
        self.root.addChild(self.texture)
        self.root.addChild(self.material)
        self.root.addChild(self.coords)
        self.root.addChild(self.face)
        vobj.addDisplayMode(self.root, "ProcessedImage")

    def updateData(self, obj, prop):
        if prop in ["ProcessedPath", "Opacity", "Width", "Height", "Placement"]:
            self._update_view()

    def _update_view(self):
        if not hasattr(self, "transform"): return
        try:
            w, h = float(self.Object.Width), float(self.Object.Height)
            self.coords.point.setValues(0, 4, [(0,0,0), (w,0,0), (w,h,0), (0,h,0)])
            self.transform.center.setValue(w/2.0, h/2.0, 0)
            
            p = self.Object.Placement
            self.transform.translation.setValue(p.Base.x, p.Base.y, p.Base.z)
            self.transform.rotation.setValue(coin.SbVec3f(p.Rotation.Axis.x, p.Rotation.Axis.y, p.Rotation.Axis.z), p.Rotation.Angle)
            
            path = self.Object.ProcessedPath
            if path and os.path.exists(path):
                self.texture.filename.setValue(str(os.path.abspath(path)))
            
            # Opacidad (1.0 - opacity = transparencia en Coin3D)
            val = float(1.0 - max(0.0, min(1.0, self.Object.Opacity)))
            self.material.transparency.set1Value(0, val)
        except: pass

    def getDisplayModes(self, obj): return ["ProcessedImage"]
    def getDefaultDisplayMode(self): return "ProcessedImage"
    def __getstate__(self): return None
    def __setstate__(self, state): return None

def create_sketch_vision_object(image_path, w=100.0, h=100.0):
    doc = App.ActiveDocument or App.newDocument()
    obj = doc.addObject("App::FeaturePython", "SketchVisionImage")
    SketchVisionObject(obj)
    ViewProviderSketchVision(obj.ViewObject)
    obj.BaseWidth, obj.BaseHeight = w, h
    obj.Width, obj.Height = w, h
    obj.ImagePath = image_path
    obj.Opacity = 1.0 # Asegurar opacidad total al inicio
    obj.ViewObject.DisplayMode = "ProcessedImage"
    doc.recompute()
    return obj
