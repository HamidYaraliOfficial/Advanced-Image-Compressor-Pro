import sys
import os
import numpy as np
import cv2
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSlider, QComboBox, QGroupBox, QSpinBox,
    QFileDialog, QTabWidget, QFormLayout, QCheckBox, QScrollArea,
    QFrame, QGridLayout, QMessageBox, QProgressBar
)
from PyQt6.QtGui import QPixmap, QImage, QPalette, QColor, QFont, QIcon
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# -------------------------------
# Translations (English & Persian)
# -------------------------------
translations = {
    "en": {
        "title": "Image Transform Studio",
        "load": "Load Image",
        "save": "Save Result",
        "reset": "Reset",
        "language": "Language",
        "theme": "Theme",
        "apply": "Apply",
        "translation": "Translation",
        "rotation": "Rotation",
        "scaling": "Scaling",
        "similarity": "Similarity",
        "affine": "Affine",
        "perspective": "Perspective",
        "tx": "X Shift",
        "ty": "Y Shift",
        "angle": "Angle (°)",
        "scale_x": "Scale X (%)",
        "scale_y": "Scale Y (%)",
        "center_x": "Center X",
        "center_y": "Center Y",
        "auto_center": "Auto Center",
        "keep_aspect": "Keep Aspect",
        "interp": "Interpolation",
        "nearest": "Nearest",
        "linear": "Linear",
        "cubic": "Cubic",
        "lanczos": "Lanczos",
        "border": "Border Mode",
        "constant": "Constant",
        "replicate": "Replicate",
        "reflect": "Reflect",
        "wrap": "Wrap",
        "border_val": "Border Value",
        "light": "Light Theme",
        "dark": "Dark Theme",
        "no_image": "No image loaded!",
        "save_ok": "Saved successfully!",
        "save_fail": "Save failed."
    },
    "fa": {
        "title": "استودیو تبدیل تصویر",
        "load": "بارگذاری تصویر",
        "save": "ذخیره نتیجه",
        "reset": "بازنشانی",
        "language": "زبان",
        "theme": "تم",
        "apply": "اعمال",
        "translation": "انتقال",
        "rotation": "چرخش",
        "scaling": "مقیاس‌دهی",
        "similarity": "تبدیل مشابه",
        "affine": "تبدیل آفین",
        "perspective": "تبدیل پرسپکتیو",
        "tx": "انتقال X",
        "ty": "انتقال Y",
        "angle": "زاویه (°)",
        "scale_x": "مقیاس X (%)",
        "scale_y": "مقیاس Y (%)",
        "center_x": "مرکز X",
        "center_y": "مرکز Y",
        "auto_center": "مرکز خودکار",
        "keep_aspect": "حفظ نسبت",
        "interp": "درون‌یابی",
        "nearest": "نزدیک‌ترین",
        "linear": "خطی",
        "cubic": "مکعبی",
        "lanczos": "لانکزوس",
        "border": "حالت حاشیه",
        "constant": "ثابت",
        "replicate": "تکرار",
        "reflect": "بازتاب",
        "wrap": "پیچش",
        "border_val": "مقدار حاشیه",
        "light": "تم روشن",
        "dark": "تم تاریک",
        "no_image": "تصویری بارگذاری نشده!",
        "save_ok": "با موفقیت ذخیره شد!",
        "save_fail": "ذخیره ناموفق بود."
    }
}

# Language direction
lang_dir = {"en": Qt.LayoutDirection.LeftToRight, "fa": Qt.LayoutDirection.RightToLeft}

# Interpolation & Border
interp_map = {
    "nearest": cv2.INTER_NEAREST,
    "linear": cv2.INTER_LINEAR,
    "cubic": cv2.INTER_CUBIC,
    "lanczos": cv2.INTER_LANCZOS4
}

border_map = {
    "constant": cv2.BORDER_CONSTANT,
    "replicate": cv2.BORDER_REPLICATE,
    "reflect": cv2.BORDER_REFLECT,
    "wrap": cv2.BORDER_WRAP
}

# -------------------------------
# Worker Thread
# -------------------------------
class TransformWorker(QThread):
    finished = pyqtSignal(np.ndarray)
    error = pyqtSignal(str)

    def __init__(self, img, typ, params):
        super().__init__()
        self.img = img
        self.typ = typ
        self.params = params

    def run(self):
        try:
            if self.img is None or self.img.size == 0:
                raise ValueError("Invalid image")
            h, w = self.img.shape[:2]
            result = self.img.copy()
            interp = self.params["interp"]
            border = self.params["border"]
            val = self.params["border_val"]

            if self.typ == "translation":
                M = np.float32([[1, 0, self.params["tx"]], [0, 1, self.params["ty"]]])
                result = cv2.warpAffine(self.img, M, (w, h), flags=interp, borderMode=border, borderValue=val)

            elif self.typ == "rotation":
                cx = self.params.get("cx", w // 2)
                cy = self.params.get("cy", h // 2)
                M = cv2.getRotationMatrix2D((cx, cy), self.params["angle"], 1.0)
                result = cv2.warpAffine(self.img, M, (w, h), flags=interp, borderMode=border, borderValue=val)

            elif self.typ == "scaling":
                sx = self.params["sx"] / 100.0
                sy = self.params["sy"] / 100.0
                new_w, new_h = int(w * sx), int(h * sy)
                result = cv2.resize(self.img, (new_w, new_h), interpolation=interp)

            elif self.typ == "similarity":
                cx, cy = w // 2, h // 2
                scale = self.params["scale"] / 100.0
                M = cv2.getRotationMatrix2D((cx, cy), self.params["angle"], scale)
                M[0, 2] += self.params["tx"]
                M[1, 2] += self.params["ty"]
                result = cv2.warpAffine(self.img, M, (w, h), flags=interp, borderMode=border, borderValue=val)

            elif self.typ == "affine":
                pts1 = np.float32([[50,50], [w-50,50], [50,h-50]])
                pts2 = np.float32([
                    [50 + self.params["tx1"], 50 + self.params["ty1"]],
                    [w-50 + self.params["tx2"], 50 + self.params["ty2"]],
                    [50 + self.params["tx3"], h-50 + self.params["ty3"]]
                ])
                M = cv2.getAffineTransform(pts1, pts2)
                result = cv2.warpAffine(self.img, M, (w, h), flags=interp, borderMode=border, borderValue=val)

            elif self.typ == "perspective":
                pts1 = np.float32([[0,0], [w,0], [0,h], [w,h]])
                pts2 = np.float32([
                    [self.params["p1x"], self.params["p1y"]],
                    [self.params["p2x"], self.params["p2y"]],
                    [self.params["p3x"], self.params["p3y"]],
                    [self.params["p4x"], self.params["p4y"]]
                ])
                M = cv2.getPerspectiveTransform(pts1, pts2)
                result = cv2.warpPerspective(self.img, M, (w, h), flags=interp, borderMode=border, borderValue=val)

            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

# -------------------------------
# Image Label
# -------------------------------
class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(400, 400)
        self.setStyleSheet("""
            border: 3px solid #3498db;
            border-radius: 16px;
            background: #f8f9fa;
            font: 12pt 'Segoe UI';
            color: #2c3e50;
        """)

    def set_image(self, img):
        if img is None: return
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
        pix = QPixmap.fromImage(qimg)
        scaled = pix.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(scaled)

# -------------------------------
# Main Window
# -------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lang = "en"
        self.theme = "light"
        self.original = None
        self.result = None
        self.worker = None
        self.init_ui()
        self.apply_theme()
        self.apply_lang()

    def init_ui(self):
        self.setWindowTitle("Image Transform Studio")
        self.setMinimumSize(1500, 900)
        self.setWindowIcon(QIcon.fromTheme("image"))

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(25)

        # Left Panel
        left = QScrollArea()
        left.setWidgetResizable(True)
        left.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(18)

        # Top Controls
        top = QGroupBox()
        top_l = QHBoxLayout(top)
        self.lang_cb = QComboBox()
        self.lang_cb.addItems(["English", "فارسی"])
        self.lang_cb.currentIndexChanged.connect(self.change_lang)
        self.theme_cb = QComboBox()
        self.theme_cb.addItems(["Light Theme", "Dark Theme"])
        self.theme_cb.currentIndexChanged.connect(self.change_theme)
        top_l.addWidget(QLabel("Language:"))
        top_l.addWidget(self.lang_cb)
        top_l.addWidget(QLabel("Theme:"))
        top_l.addWidget(self.theme_cb)
        layout.addWidget(top)

        # File Buttons
        file_box = QGroupBox()
        file_l = QHBoxLayout(file_box)
        self.load_btn = QPushButton()
        self.load_btn.clicked.connect(self.load)
        self.save_btn = QPushButton()
        self.save_btn.clicked.connect(self.save)
        self.reset_btn = QPushButton()
        self.reset_btn.clicked.connect(self.reset)
        file_l.addWidget(self.load_btn)
        file_l.addWidget(self.save_btn)
        file_l.addWidget(self.reset_btn)
        layout.addWidget(file_box)

        # Tabs
        self.tabs = QTabWidget()
        self.create_tabs()
        layout.addWidget(self.tabs)

        # Global
        global_box = QGroupBox()
        g_l = QFormLayout(global_box)
        self.interp_cb = QComboBox()
        self.interp_cb.addItems(["Nearest", "Linear", "Cubic", "Lanczos"])
        self.border_cb = QComboBox()
        self.border_cb.addItems(["Constant", "Replicate", "Reflect", "Wrap"])
        self.border_val = QSpinBox()
        self.border_val.setRange(0, 255)
        g_l.addRow(QLabel("Interpolation:"), self.interp_cb)
        g_l.addRow(QLabel("Border:"), self.border_cb)
        g_l.addRow(QLabel("Value:"), self.border_val)
        layout.addWidget(global_box)

        # Apply
        self.apply_btn = QPushButton()
        self.apply_btn.clicked.connect(self.apply)
        self.apply_btn.setMinimumHeight(60)
        self.apply_btn.setStyleSheet("font: bold 16pt; background: #2980b9; color: white; border-radius: 14px;")
        layout.addWidget(self.apply_btn)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        left.setWidget(content)
        main_layout.addWidget(left, 1)

        # Right Panel
        right = QFrame()
        r_l = QGridLayout(right)
        self.orig_lbl = ImageLabel()
        self.res_lbl = ImageLabel()
        r_l.addWidget(QLabel("<h2>Original</h2>"), 0, 0, Qt.AlignmentFlag.AlignCenter)
        r_l.addWidget(self.orig_lbl, 1, 0)
        r_l.addWidget(QLabel("<h2>Result</h2>"), 0, 1, Qt.AlignmentFlag.AlignCenter)
        r_l.addWidget(self.res_lbl, 1, 1)
        main_layout.addWidget(right, 3)

    def create_tabs(self):
        # Translation
        t1 = QWidget(); l1 = QFormLayout(t1)
        self.tx_s = QSlider(Qt.Orientation.Horizontal); self.tx_s.setRange(-1000, 1000)
        self.tx_n = QSpinBox(); self.tx_n.setRange(-1000, 1000)
        self.tx_s.valueChanged.connect(self.tx_n.setValue); self.tx_n.valueChanged.connect(self.tx_s.setValue)
        self.ty_s = QSlider(Qt.Orientation.Horizontal); self.ty_s.setRange(-1000, 1000)
        self.ty_n = QSpinBox(); self.ty_n.setRange(-1000, 1000)
        self.ty_s.valueChanged.connect(self.ty_n.setValue); self.ty_n.valueChanged.connect(self.ty_s.setValue)
        l1.addRow(QLabel("X:"), self.tx_s); l1.addRow("", self.tx_n)
        l1.addRow(QLabel("Y:"), self.ty_s); l1.addRow("", self.ty_n)
        self.tabs.addTab(t1, "Translation")

        # Rotation
        t2 = QWidget(); l2 = QFormLayout(t2)
        self.ang_s = QSlider(Qt.Orientation.Horizontal); self.ang_s.setRange(-180, 180)
        self.ang_n = QSpinBox(); self.ang_n.setRange(-180, 180)
        self.ang_s.valueChanged.connect(self.ang_n.setValue); self.ang_n.valueChanged.connect(self.ang_s.setValue)
        self.cx_n = QSpinBox(); self.cy_n = QSpinBox()
        self.auto_c = QCheckBox(); self.auto_c.setChecked(True)
        self.auto_c.toggled.connect(lambda c: [w.setEnabled(not c) for w in [self.cx_n, self.cy_n]])
        l2.addRow(QLabel("Angle:"), self.ang_s); l2.addRow("", self.ang_n)
        l2.addRow(QLabel("Center X:"), self.cx_n); l2.addRow(QLabel("Center Y:"), self.cy_n)
        l2.addRow(QLabel("Auto:"), self.auto_c)
        self.tabs.addTab(t2, "Rotation")

        # Scaling
        t3 = QWidget(); l3 = QFormLayout(t3)
        self.sx_s = QSlider(Qt.Orientation.Horizontal); self.sx_s.setRange(10, 500); self.sx_s.setValue(100)
        self.sx_n = QSpinBox(); self.sx_n.setRange(10, 500); self.sx_n.setValue(100)
        self.sx_s.valueChanged.connect(self.sx_n.setValue); self.sx_n.valueChanged.connect(self.sx_s.setValue)
        self.sy_s = QSlider(Qt.Orientation.Horizontal); self.sy_s.setRange(10, 500); self.sy_s.setValue(100)
        self.sy_n = QSpinBox(); self.sy_n.setRange(10, 500); self.sy_n.setValue(100)
        self.sy_s.valueChanged.connect(self.sy_n.setValue); self.sy_n.valueChanged.connect(self.sy_s.setValue)
        self.keep_a = QCheckBox(); self.keep_a.setChecked(True)
        self.keep_a.toggled.connect(lambda c: self.sy_s.setValue(self.sx_s.value()) if c else None)
        l3.addRow(QLabel("X (%):"), self.sx_s); l3.addRow("", self.sx_n)
        l3.addRow(QLabel("Y (%):"), self.sy_s); l3.addRow("", self.sy_n)
        l3.addRow(QLabel("Keep Aspect:"), self.keep_a)
        self.tabs.addTab(t3, "Scaling")

        # Similarity
        t4 = QWidget(); l4 = QFormLayout(t4)
        self.sim_a_s = QSlider(Qt.Orientation.Horizontal); self.sim_a_s.setRange(-180, 180)
        self.sim_a_n = QSpinBox(); self.sim_a_n.setRange(-180, 180)
        self.sim_a_s.valueChanged.connect(self.sim_a_n.setValue); self.sim_a_n.valueChanged.connect(self.sim_a_s.setValue)
        self.sim_sc_s = QSlider(Qt.Orientation.Horizontal); self.sim_sc_s.setRange(10, 300); self.sim_sc_s.setValue(100)
        self.sim_sc_n = QSpinBox(); self.sim_sc_n.setRange(10, 300); self.sim_sc_n.setValue(100)
        self.sim_sc_s.valueChanged.connect(self.sim_sc_n.setValue); self.sim_sc_n.valueChanged.connect(self.sim_sc_s.setValue)
        self.sim_tx = QSpinBox(); self.sim_tx.setRange(-500, 500)
        self.sim_ty = QSpinBox(); self.sim_ty.setRange(-500, 500)
        l4.addRow(QLabel("Angle:"), self.sim_a_s); l4.addRow("", self.sim_a_n)
        l4.addRow(QLabel("Scale:"), self.sim_sc_s); l4.addRow("", self.sim_sc_n)
        l4.addRow(QLabel("X:"), self.sim_tx); l4.addRow(QLabel("Y:"), self.sim_ty)
        self.tabs.addTab(t4, "Similarity")

        # Affine
        t5 = QWidget(); l5 = QFormLayout(t5)
        self.a_tx1 = QSpinBox(); self.a_tx1.setRange(-300, 300)
        self.a_ty1 = QSpinBox(); self.a_ty1.setRange(-300, 300)
        self.a_tx2 = QSpinBox(); self.a_tx2.setRange(-300, 300)
        self.a_ty2 = QSpinBox(); self.a_ty2.setRange(-300, 300)
        self.a_tx3 = QSpinBox(); self.a_tx3.setRange(-300, 300)
        self.a_ty3 = QSpinBox(); self.a_ty3.setRange(-300, 300)
        l5.addRow(QLabel("Top-L ΔX:"), self.a_tx1); l5.addRow(QLabel("ΔY:"), self.a_ty1)
        l5.addRow(QLabel("Top-R ΔX:"), self.a_tx2); l5.addRow(QLabel("ΔY:"), self.a_ty2)
        l5.addRow(QLabel("Bot-L ΔX:"), self.a_tx3); l5.addRow(QLabel("ΔY:"), self.a_ty3)
        self.tabs.addTab(t5, "Affine")

        # Perspective
        t6 = QWidget(); g6 = QGridLayout(t6)
        self.p1x = QSpinBox(); self.p1x.setRange(0, 2000)
        self.p1y = QSpinBox(); self.p1y.setRange(0, 2000)
        self.p2x = QSpinBox(); self.p2x.setRange(0, 2000); self.p2x.setValue(500)
        self.p2y = QSpinBox(); self.p2y.setRange(0, 2000)
        self.p3x = QSpinBox(); self.p3x.setRange(0, 2000)
        self.p3y = QSpinBox(); self.p3y.setRange(0, 2000); self.p3y.setValue(500)
        self.p4x = QSpinBox(); self.p4x.setRange(0, 2000); self.p4x.setValue(500)
        self.p4y = QSpinBox(); self.p4y.setRange(0, 2000); self.p4y.setValue(500)
        g6.addWidget(QLabel("P1 X:"), 0, 0); g6.addWidget(self.p1x, 0, 1)
        g6.addWidget(QLabel("P1 Y:"), 0, 2); g6.addWidget(self.p1y, 0, 3)
        g6.addWidget(QLabel("P2 X:"), 1, 0); g6.addWidget(self.p2x, 1, 1)
        g6.addWidget(QLabel("P2 Y:"), 1, 2); g6.addWidget(self.p2y, 1, 3)
        g6.addWidget(QLabel("P3 X:"), 2, 0); g6.addWidget(self.p3x, 2, 1)
        g6.addWidget(QLabel("P3 Y:"), 2, 2); g6.addWidget(self.p3y, 2, 3)
        g6.addWidget(QLabel("P4 X:"), 3, 0); g6.addWidget(self.p4x, 3, 1)
        g6.addWidget(QLabel("P4 Y:"), 3, 2); g6.addWidget(self.p4y, 3, 3)
        self.tabs.addTab(t6, "Perspective")

    def load(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if path:
            img = cv2.imread(path)
            if img is not None and img.size > 0:
                self.original = img
                self.result = img.copy()
                self.orig_lbl.set_image(img)
                self.res_lbl.set_image(img)
                h, w = img.shape[:2]
                self.cx_n.setRange(0, w); self.cy_n.setRange(0, h)
                if self.auto_c.isChecked():
                    self.cx_n.setValue(w//2); self.cy_n.setValue(h//2)
                self.p2x.setValue(w); self.p3y.setValue(h); self.p4x.setValue(w); self.p4y.setValue(h)

    def save(self):
        if self.result is None or self.result.size == 0:
            QMessageBox.warning(self, "Warning", translations[self.lang]["no_image"])
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save", "", "PNG (*.png);;JPEG (*.jpg)")
        if path:
            success = cv2.imwrite(path, self.result)
            QMessageBox.information(self, "Info", translations[self.lang]["save_ok"] if success else translations[self.lang]["save_fail"])

    def reset(self):
        if self.original is not None and self.original.size > 0:
            self.result = self.original.copy()
            self.res_lbl.set_image(self.result)

    def apply(self):
        if self.original is None or self.original.size == 0:
            QMessageBox.warning(self, "Warning", translations[self.lang]["no_image"])
            return

        idx = self.tabs.currentIndex()
        types = ["translation", "rotation", "scaling", "similarity", "affine", "perspective"]
        typ = types[idx]
        params = {
            "interp": interp_map[self.interp_cb.currentText().lower()],
            "border": border_map[self.border_cb.currentText().lower()],
            "border_val": self.border_val.value()
        }

        if typ == "translation":
            params["tx"] = self.tx_n.value()
            params["ty"] = self.ty_n.value()
        elif typ == "rotation":
            params["angle"] = self.ang_n.value()
            params["cx"] = self.cx_n.value() if not self.auto_c.isChecked() else self.original.shape[1] // 2
            params["cy"] = self.cy_n.value() if not self.auto_c.isChecked() else self.original.shape[0] // 2
        elif typ == "scaling":
            params["sx"] = self.sx_n.value()
            params["sy"] = self.sy_n.value() if not self.keep_a.isChecked() else self.sx_n.value()
        elif typ == "similarity":
            params["angle"] = self.sim_a_n.value()
            params["scale"] = self.sim_sc_n.value()
            params["tx"] = self.sim_tx.value()
            params["ty"] = self.sim_ty.value()
        elif typ == "affine":
            params.update({
                "tx1": self.a_tx1.value(), "ty1": self.a_ty1.value(),
                "tx2": self.a_tx2.value(), "ty2": self.a_ty2.value(),
                "tx3": self.a_tx3.value(), "ty3": self.a_ty3.value()
            })
        elif typ == "perspective":
            params.update({
                "p1x": self.p1x.value(), "p1y": self.p1y.value(),
                "p2x": self.p2x.value(), "p2y": self.p2y.value(),
                "p3x": self.p3x.value(), "p3y": self.p3y.value(),
                "p4x": self.p4x.value(), "p4y": self.p4y.value()
            })

        self.progress.setVisible(True); self.progress.setRange(0, 0); self.apply_btn.setEnabled(False)
        self.worker = TransformWorker(self.original, typ, params)
        self.worker.finished.connect(self.on_done)
        self.worker.error.connect(lambda e: QMessageBox.critical(self, "Error", e))
        self.worker.start()

    def on_done(self, img):
        self.result = img
        self.res_lbl.set_image(img)
        self.progress.setVisible(False)
        self.apply_btn.setEnabled(True)

    def change_lang(self, i):
        self.lang = "en" if i == 0 else "fa"
        self.apply_lang()

    def change_theme(self, i):
        self.theme = "light" if i == 0 else "dark"
        self.apply_theme()

    def apply_lang(self):
        t = translations[self.lang]
        self.setWindowTitle(t["title"])
        self.load_btn.setText(t["load"])
        self.save_btn.setText(t["save"])
        self.reset_btn.setText(t["reset"])
        self.apply_btn.setText(t["apply"])
        self.tabs.setTabText(0, t["translation"])
        self.tabs.setTabText(1, t["rotation"])
        self.tabs.setTabText(2, t["scaling"])
        self.tabs.setTabText(3, t["similarity"])
        self.tabs.setTabText(4, t["affine"])
        self.tabs.setTabText(5, t["perspective"])
        self.lang_cb.setCurrentIndex(0 if self.lang == "en" else 1)
        self.setLayoutDirection(lang_dir[self.lang])

    def apply_theme(self):
        app = QApplication.instance()
        if self.theme == "light":
            p = QPalette()
            p.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
            p.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
            p.setColor(QPalette.ColorRole.Base, QColor(250, 250, 250))
            p.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
            p.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
            p.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
            p.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
            app.setPalette(p)
        else:
            p = QPalette()
            p.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
            p.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            p.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
            p.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            p.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
            p.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
            p.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
            app.setPalette(p)

        self.setStyleSheet("""
            QGroupBox { font-weight: bold; border: 2px solid #bdc3c7; border-radius: 12px; margin-top: 12px; padding-top: 10px; }
            QGroupBox::title { subcontrol-origin: margin; left: 15px; padding: 0 8px; color: #2c3e50; }
            QLabel { color: #2c3e50; }
            QPushButton { padding: 10px; border-radius: 10px; font-weight: bold; }
        """)

# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())