

import customtkinter
from PIL import Image
"""
Importación robusta de PyMuPDF sin dependencias de import estático.
Se usa importlib para:
- Preferir `pymupdf` (nombre moderno)
- Intentar `fitz` (alias histórico) y validar que realmente sea PyMuPDF
- Evitar warnings de Pylance por import no resuelto
"""
import importlib.util
import importlib

_FITZ_OK = False
fitz = None  # será el módulo de PyMuPDF si está disponible

_spec = importlib.util.find_spec("pymupdf")
if _spec is None:
    _spec = importlib.util.find_spec("fitz")

if _spec is not None:
    try:
        _mod = importlib.import_module(_spec.name)
        # Si viene bajo nombre 'fitz', validar que sea PyMuPDF real
        if _spec.name == "fitz" and not hasattr(_mod, "open"):
            raise ImportError("El paquete 'fitz' instalado no es PyMuPDF.")
        fitz = _mod
        _FITZ_OK = True
    except Exception:
        fitz = None
        _FITZ_OK = False
from threading import Thread
import math
import io
import os

class CTkPDFViewer(customtkinter.CTkScrollableFrame):
    def __init__(self,
                 master: any,
                 file: str,
                 page_width: int = 600,
                 page_height: int = 700,
                 page_separation_height: int = 2,
                 **kwargs):
        
        super().__init__(master, **kwargs)

        self.page_width = page_width
        self.page_height = page_height
        self.separation = page_separation_height
        self.pdf_images = []
        self.labels = []
        self.file = file

        self.percentage_view = 0
        self.percentage_load = customtkinter.StringVar()
        
        self.loading_message = customtkinter.CTkLabel(self, textvariable=self.percentage_load, justify="center")
        self.loading_message.pack(pady=10)

        self.loading_bar = customtkinter.CTkProgressBar(self, width=100)
        self.loading_bar.set(0)
        self.loading_bar.pack(side="top", fill="x", padx=10)

        self.after(250, self.start_process)

    def start_process(self):
        Thread(target=self.add_pages).start()
        
    def add_pages(self):
        """ add images and labels """
        self.percentage_bar = 0
        if not _FITZ_OK or fitz is None:
            # Mostrar mensaje claro en el visor en vez de romper la app
            self.loading_bar.pack_forget()
            self.percentage_load.set(
                "PyMuPDF no está disponible.\n"
                "Instala el paquete correcto: pip install PyMuPDF\n"
                "Si tienes instalado 'fitz' (paquete incorrecto), desinstálalo: pip uninstall fitz"
            )
            return

        open_pdf = fitz.open(self.file)
        
        for page in open_pdf:
            page_data = page.get_pixmap()
            pix = fitz.Pixmap(page_data, 0) if page_data.alpha else page_data
            img = Image.open(io.BytesIO(pix.tobytes('ppm')))
            label_img = customtkinter.CTkImage(img, size=(self.page_width, self.page_height))
            self.pdf_images.append(label_img)
                
            self.percentage_bar = self.percentage_bar + 1
            percentage_view = (float(self.percentage_bar) / float(len(open_pdf)) * float(100))
            self.loading_bar.set(percentage_view)
            self.percentage_load.set(f"Loading {os.path.basename(self.file)} \n{int(math.floor(percentage_view))}%")
            
        self.loading_bar.pack_forget()
        self.loading_message.pack_forget()
        open_pdf.close()
        
        for i in self.pdf_images:
            label = customtkinter.CTkLabel(self, image=i, text="")
            label.pack(pady=(0, self.separation))
            self.labels.append(label)
        
    def configure(self, **kwargs):
        """ configurable options """
        
        if "file" in kwargs:
            self.file = kwargs.pop("file")
            self.pdf_images = []
            for i in self.labels:
                i.destroy()
            self.labels = []
            self.after(250, self.start_process)
            
        if "page_width" in kwargs:
            self.page_width = kwargs.pop("page_width")
            for i in self.pdf_images:
                i.configure(size=(self.page_width, self.page_height))
                
        if "page_height" in kwargs:
            self.page_height = kwargs.pop("page_height")
            for i in self.pdf_images:
                i.configure(size=(self.page_width, self.page_height))
            
        if "page_separation_height" in kwargs:
            self.separation = kwargs.pop("page_separation_height")
            for i in self.labels:
                i.pack_forget()
                i.pack(pady=(0,self.separation))
        
        super().configure(**kwargs)
