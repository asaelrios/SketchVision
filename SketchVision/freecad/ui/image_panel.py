import os
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets, QtUiTools
import cv2
import time

class SketchVisionPanel:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        ui_path = os.path.abspath(os.path.join(current_dir, "../../ui/image_panel.ui"))
        loader = QtUiTools.QUiLoader()
        self.form = loader.load(ui_path)
        
        from ...core.engine import ImageEngine
        self.engine = ImageEngine()
        self.active_obj = None
        self.last_update = 0
        self.is_processing = False
        self.last_temp_file = None
        
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        self.form.sliderOpacity.setRange(0, 100)
        self.form.sliderRotation.setRange(0, 359)
        self.form.sliderScale.setRange(20, 200)
        self.form.sliderPosX.setRange(-100, 100)
        self.form.sliderPosY.setRange(-100, 100)
        self.form.sliderBrightness.setRange(-100, 100)
        self.form.sliderContrast.setRange(-100, 100)
        self.form.sliderGamma.setRange(1, 300)
        self.form.sliderThreshold.setRange(0, 255)

    def _connect_signals(self):
        for s in [self.form.sliderBrightness, self.form.sliderContrast, 
                  self.form.sliderThreshold, self.form.sliderGamma,
                  self.form.sliderGaussian, self.form.sliderMedian]:
            s.valueChanged.connect(self.on_param_changed)
            
        self.form.sliderOpacity.valueChanged.connect(self.on_opacity_changed)
        self.form.sliderScale.valueChanged.connect(self.on_scale_changed)
        self.form.sliderRotation.valueChanged.connect(self.on_rotation_changed)
        self.form.sliderPosX.valueChanged.connect(self.on_position_changed)
        self.form.sliderPosY.valueChanged.connect(self.on_position_changed)
        
        self.form.chkGray.stateChanged.connect(lambda: self.on_view_mode_changed("gray"))
        self.form.chkBinary.stateChanged.connect(lambda: self.on_view_mode_changed("binary"))
        self.form.chkGaussian.stateChanged.connect(lambda: self.on_blur_changed("gaussian"))
        self.form.chkMedian.stateChanged.connect(lambda: self.on_blur_changed("median"))
        
        self.form.btnOpenImage.clicked.connect(self.on_open_image)
        self.form.btnReset.clicked.connect(self.on_reset)

    def on_view_mode_changed(self, mode):
        self.form.chkGray.blockSignals(True)
        self.form.chkBinary.blockSignals(True)
        if mode == "gray" and self.form.chkGray.isChecked():
            self.form.chkBinary.setChecked(False)
        elif mode == "binary" and self.form.chkBinary.isChecked():
            self.form.chkGray.setChecked(False)
        self.form.chkGray.blockSignals(False)
        self.form.chkBinary.blockSignals(False)
        self.on_param_changed()

    def on_blur_changed(self, current):
        self.form.chkGaussian.blockSignals(True)
        self.form.chkMedian.blockSignals(True)
        if current == "gaussian" and self.form.chkGaussian.isChecked():
            self.form.chkMedian.setChecked(False)
        elif current == "median" and self.form.chkMedian.isChecked():
            self.form.chkGaussian.setChecked(False)
        self.form.chkGaussian.blockSignals(False)
        self.form.chkMedian.blockSignals(False)
        self.on_param_changed()

    def on_opacity_changed(self):
        if not self.active_obj: return
        self.active_obj.Opacity = float(self.form.sliderOpacity.value()) / 100.0
        Gui.updateGui()

    def on_open_image(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Abrir Imagen", "", "Images (*.png *.jpg *.bmp)")
        if filename:
            shape = self.engine.load_image(filename)
            if shape:
                from ..proxies import create_sketch_vision_object
                self.active_obj = create_sketch_vision_object(filename, w=100 * (shape[1]/shape[0]), h=100)
                self.on_reset()
                # Pequeña pausa para asegurar que el objeto existe antes de procesar
                QtCore.QTimer.singleShot(100, self.update_process)

    def on_scale_changed(self):
        if not self.active_obj: return
        t = time.time()
        if t - self.last_update < 0.02: return
        self.last_update = t
        scale = float(self.form.sliderScale.value()) / 100.0
        self.active_obj.Width = self.active_obj.BaseWidth * scale
        self.active_obj.Height = self.active_obj.BaseHeight * scale
        Gui.updateGui()

    def on_rotation_changed(self):
        if not self.active_obj: return
        t = time.time()
        if t - self.last_update < 0.02: return
        self.last_update = t
        p = self.active_obj.Placement
        p.Rotation = App.Rotation(App.Vector(0,0,1), float(self.form.sliderRotation.value()))
        self.active_obj.Placement = p
        Gui.updateGui()

    def on_position_changed(self):
        if not self.active_obj: return
        t = time.time()
        if t - self.last_update < 0.02: return
        self.last_update = t
        p = self.active_obj.Placement
        p.Base = App.Vector(float(self.form.sliderPosX.value()), float(self.form.sliderPosY.value()), 0)
        self.active_obj.Placement = p
        Gui.updateGui()

    def on_param_changed(self):
        if not self.active_obj or self.is_processing: return
        t = time.time()
        if t - self.last_update < 0.05: return
        self.last_update = t
        self.update_process()

    def update_process(self):
        if not self.active_obj: return
        self.is_processing = True
        try:
            blur_type = None
            blur_val = 3
            if self.form.chkGaussian.isChecked():
                blur_type = "gaussian"
                blur_val = self.form.sliderGaussian.value()
            elif self.form.chkMedian.isChecked():
                blur_type = "median"
                blur_val = self.form.sliderMedian.value()

            img = self.engine.process(
                brightness=float(self.form.sliderBrightness.value()),
                contrast=float(self.form.sliderContrast.value()),
                gamma=self.form.sliderGamma.value() / 100.0,
                threshold=self.form.sliderThreshold.value() if self.form.chkBinary.isChecked() else 0,
                grayscale=self.form.chkGray.isChecked(),
                blur_type=blur_type,
                blur_strength=blur_val
            )
            
            temp_file = os.path.join(App.getTempPath(), f"sv_render_{int(time.time()*1000)}.png")
            cv2.imwrite(temp_file, img)
            
            old_file = self.last_temp_file
            self.active_obj.ProcessedPath = temp_file
            self.last_temp_file = temp_file
            
            Gui.updateGui()
            if old_file and os.path.exists(old_file):
                try: os.remove(old_file)
                except: pass
        finally:
            self.is_processing = False

    def on_reset(self):
        for widget in self.form.findChildren(QtWidgets.QSlider) + self.form.findChildren(QtWidgets.QCheckBox):
            widget.blockSignals(True)

        self.form.sliderBrightness.setValue(0)
        self.form.sliderContrast.setValue(0)
        self.form.sliderThreshold.setValue(127)
        self.form.sliderGamma.setValue(100)
        self.form.sliderOpacity.setValue(100)
        self.form.sliderScale.setValue(100)
        self.form.sliderRotation.setValue(0)
        self.form.sliderPosX.setValue(0)
        self.form.sliderPosY.setValue(0)
        self.form.sliderGaussian.setValue(3)
        self.form.sliderMedian.setValue(3)
        self.form.chkGray.setChecked(False)
        self.form.chkBinary.setChecked(False)
        self.form.chkGaussian.setChecked(False)
        self.form.chkMedian.setChecked(False)
        self.form.chkLockAspect.setChecked(True)
        
        for widget in self.form.findChildren(QtWidgets.QSlider) + self.form.findChildren(QtWidgets.QCheckBox):
            widget.blockSignals(False)

    def getStandardButtons(self):
        return int(QtWidgets.QDialogButtonBox.StandardButton.Close.value)

def show_panel():
    Gui.Control.showDialog(SketchVisionPanel())
