from fpdf import FPDF
from datetime import datetime

class BoletaFacade:
    def __init__(self, pedido):
        self.pedido = pedido
        self.detalle = ""
        self.subtotal = 0
        self.iva = 0
        self.total = 0

    def generar_detalle_boleta(self):
        self.detalle = ""
        for item in self.pedido.menus:
            subtotal = item.precio * item.cantidad
            self.detalle += f"{item.nombre:<30} {item.cantidad:<10} ${item.precio:<10.2f} ${subtotal:<10.2f}\n"
        
        self.subtotal = self.pedido.calcular_total()
        self.iva = self.subtotal * 0.19
        self.total = self.subtotal + self.iva

    def crear_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Boleta Restaurante", ln=True, align='L')
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "Razón Social del Negocio", ln=True, align='L')
        pdf.cell(0, 10, "RUT: 12345678-9", ln=True, align='L')
        pdf.cell(0, 10, "Dirección: Calle Falsa 123", ln=True, align='L')
        pdf.cell(0, 10, "Teléfono: +56 9 1234 5678", ln=True, align='L')
        pdf.cell(0, 10, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", ln=True, align='R')
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(70, 10, "Nombre", border=1)
        pdf.cell(20, 10, "Cantidad", border=1)
        pdf.cell(35, 10, "Precio Unitario", border=1)
        pdf.cell(30, 10, "Subtotal", border=1)
        pdf.ln()
        
        pdf.set_font("Arial", size=12)
        for item in self.pedido.menus:
            subtotal = item.precio * item.cantidad
            pdf.cell(70, 10, item.nombre, border=1)
            pdf.cell(20, 10, str(item.cantidad), border=1)
            pdf.cell(35, 10, f"${item.precio:.2f}", border=1)
            pdf.cell(30, 10, f"${subtotal:.2f}", border=1)
            pdf.ln()

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(120, 10, "Subtotal:", 0, 0, 'R')
        pdf.cell(30, 10, f"${self.subtotal:.2f}", ln=True, align='R')
        
        pdf.cell(120, 10, "IVA (19%):", 0, 0, 'R')
        pdf.cell(30, 10, f"${self.iva:.2f}", ln=True, align='R')
        
        pdf.cell(120, 10, "Total:", 0, 0, 'R')
        pdf.cell(30, 10, f"${self.total:.2f}", ln=True, align='R')
        
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(0, 10, "Gracias por su compra. Para cualquier consulta, llámenos al +56 9 777 5678.", 0, 1, 'C')
        pdf.cell(0, 10, "Los productos adquiridos no tienen garantía.", 0, 1, 'C')
        

        pdf_filename = "boleta.pdf"
        pdf.output(pdf_filename)
        return pdf_filename

    def generar_boleta(self):
        """Coordina la generación de la boleta y la creación del PDF."""
        self.generar_detalle_boleta()
        pdf_path = self.crear_pdf()
        return(f"Boleta generada y guardada en: {pdf_path}")
