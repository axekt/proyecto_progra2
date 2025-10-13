from ElementoMenu import CrearMenu
import customtkinter as ctk
from tkinter import ttk, Toplevel, Label, messagebox
from Ingrediente import Ingrediente
from Stock import Stock
import re
from PIL import Image
from CTkMessagebox import CTkMessagebox
from Pedido import Pedido
from BoletaFacade import BoletaFacade
import pandas as pd
from tkinter import filedialog
from Menu_catalog import get_default_menus
from menu_pdf import create_menu_pdf
from ctk_pdf_viewer import CTkPDFViewer
import os
from tkinter.font import nametofont
class AplicacionConPestanas(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Gestión de ingredientes y pedidos")
        self.geometry("870x700")
        nametofont("TkHeadingFont").configure(size=14)
        nametofont("TkDefaultFont").configure(size=11)

        self.stock = Stock()
        self.menus_creados = set()

        self.pedido = Pedido()

        self.menus = get_default_menus()  
  
        self.tabview = ctk.CTkTabview(self,command=self.on_tab_change)
        self.tabview.pack(expand=True, fill="both", padx=10, pady=10)

        self.crear_pestanas()

    def actualizar_treeview(self):

        for item in self.tree.get_children():
            self.tree.delete(item)


        for ingrediente in self.stock.lista_ingredientes:
            self.tree.insert("", "end", values=(ingrediente.nombre,ingrediente.unidad, ingrediente.cantidad))    

    def on_tab_change(self):
        selected_tab = self.tabview.get()
        if selected_tab == "carga de ingredientes":
            print('carga de ingredientes')
        if selected_tab == "Stock":
            self.actualizar_treeview()
        if selected_tab == "Pedido":
            self.actualizar_treeview()
            self.generar_menus()  # Generar tarjetas de menús
            self.actualizar_treeview_pedido()  # Actualizar lista del pedido
            print('pedido')
        if selected_tab == "Carta restorante":
            self.actualizar_treeview()
            print('Carta restorante')
        if selected_tab == "Boleta":
            self.actualizar_treeview()
            print('Boleta')  

    def crear_pestanas(self):
        self.tab3 = self.tabview.add("carga de ingredientes")  
        self.tab1 = self.tabview.add("Stock")
        self.tab4 = self.tabview.add("Carta restorante")  
        self.tab2 = self.tabview.add("Pedido")
        self.tab5 = self.tabview.add("Boleta")
        
        self.configurar_pestana1()
        self.configurar_pestana2()
        self.configurar_pestana3()
        self._configurar_pestana_crear_menu()
        self._configurar_pestana_ver_boleta()

    def configurar_pestana3(self):
        label = ctk.CTkLabel(self.tab3, text="Carga de archivo CSV")
        label.pack(pady=20)
        boton_cargar_csv = ctk.CTkButton(self.tab3, text="Cargar CSV", fg_color="#1976D2", text_color="white",command=self.cargar_csv)

        boton_cargar_csv.pack(pady=10)

        self.frame_tabla_csv = ctk.CTkFrame(self.tab3)
        self.frame_tabla_csv.pack(fill="both", expand=True, padx=10, pady=10)
        self.df_csv = None   
        self.tabla_csv = None

        self.boton_agregar_stock = ctk.CTkButton(self.frame_tabla_csv, text="Agregar al Stock")
        self.boton_agregar_stock.pack(side="bottom", pady=10)
 
    def agregar_csv_al_stock(self):
        if self.df_csv is None:
            CTkMessagebox(title="Error", message="Primero debes cargar un archivo CSV.", icon="warning")
            return

        if 'nombre' not in self.df_csv.columns or 'cantidad' not in self.df_csv.columns:
            CTkMessagebox(title="Error", message="El CSV debe tener columnas 'nombre' y 'cantidad'.", icon="warning")
            return
        for _, row in self.df_csv.iterrows():
            nombre = str(row['nombre'])
            cantidad = str(row['cantidad'])
            unidad = str(row['unidad'])
            ingrediente = Ingrediente(nombre=nombre,unidad=unidad,cantidad=cantidad)
            self.stock.agregar_ingrediente(ingrediente)
        CTkMessagebox(title="Stock Actualizado", message="Ingredientes agregados al stock correctamente.", icon="info")
        self.actualizar_treeview()   

    def cargar_csv(self):
        file_path = filedialog.askopenfilename(
            title="seleccionar archivo csv",
            filetypes=[("archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if not file_path:
            return
        try:
            df = pd.read_csv(file_path)
            self.df_csv = df
            self.mostrar_dataframe_en_tabla(df)
            self.boton_agregar_stock.configure(command=self.agregar_csv_al_stock)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo cargar el archivo CSV.\n{e}", icon="warning")
        
    def mostrar_dataframe_en_tabla(self, df):
        if self.tabla_csv:
            self.tabla_csv.destroy()

        self.tabla_csv = ttk.Treeview(self.frame_tabla_csv, columns=list(df.columns), show="headings")
        for col in df.columns:
            self.tabla_csv.heading(col, text=col)
            self.tabla_csv.column(col, width=100, anchor="center")


        for _, row in df.iterrows():
            self.tabla_csv.insert("", "end", values=list(row))

        self.tabla_csv.pack(expand=True, fill="both", padx=10, pady=10)

    def actualizar_treeview_pedido(self):
        for item in self.treeview_menu.get_children():
            self.treeview_menu.delete(item)

        for menu in self.pedido.menus:
            self.treeview_menu.insert("", "end", values=(menu.nombre, menu.cantidad, f"${menu.precio:.2f}"))
            
    def _configurar_pestana_crear_menu(self):
        contenedor = ctk.CTkFrame(self.tab4)
        contenedor.pack(expand=True, fill="both", padx=10, pady=10)

        boton_menu = ctk.CTkButton(
            contenedor,
            text="Generar Carta (PDF)",
            command=self.generar_y_mostrar_carta_pdf
        )
        boton_menu.pack(pady=10)

        self.pdf_frame_carta = ctk.CTkFrame(contenedor)
        self.pdf_frame_carta.pack(expand=True, fill="both", padx=10, pady=10)

        self.pdf_viewer_carta = None
    def generar_y_mostrar_carta_pdf(self):
        try:
            pdf_path = "carta.pdf"
            create_menu_pdf(self.menus, pdf_path,
                titulo_negocio="Restaurante",
                subtitulo="Carta Primavera 2025",
                moneda="$")
            
            if self.pdf_viewer_carta is not None:
                try:
                    self.pdf_viewer_carta.pack_forget()
                    self.pdf_viewer_carta.destroy()
                except Exception:
                    pass
                self.pdf_viewer_carta = None

            abs_pdf = os.path.abspath(pdf_path)
            self.pdf_viewer_carta = CTkPDFViewer(self.pdf_frame_carta, file=abs_pdf)
            self.pdf_viewer_carta.pack(expand=True, fill="both")

        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo generar/mostrar la carta.\n{e}", icon="warning")

    def _configurar_pestana_ver_boleta(self):
        contenedor = ctk.CTkFrame(self.tab5)
        contenedor.pack(expand=True, fill="both", padx=10, pady=10)
    
        boton_boleta = ctk.CTkButton(
            contenedor,
            text="Mostrar Boleta (PDF)",
            command=self.mostrar_boleta
        )
        boton_boleta.pack(pady=10)
    
        self.pdf_frame_boleta = ctk.CTkFrame(contenedor)
        self.pdf_frame_boleta.pack(expand=True, fill="both", padx=10, pady=10)
    
        self.pdf_viewer_boleta = None
        

    def mostrar_boleta(self):
        if not self.pedido.menus:
            CTkMessagebox(title="Error", message="No hay items en el pedido para mostrar la boleta.", icon="warning")
            return
        
        try:
            # Generar la boleta
            boleta_facade = BoletaFacade(self.pedido)
            pdf_path = boleta_facade.crear_pdf()
            
            # Limpiar visor anterior si existe
            if self.pdf_viewer_boleta is not None:
                try:
                    self.pdf_viewer_boleta.pack_forget()
                    self.pdf_viewer_boleta.destroy()
                except Exception:
                    pass
                self.pdf_viewer_boleta = None
            
            # Mostrar el PDF en el visor
            abs_pdf = os.path.abspath(pdf_path)
            self.pdf_viewer_boleta = CTkPDFViewer(self.pdf_frame_boleta, file=abs_pdf)
            self.pdf_viewer_boleta.pack(expand=True, fill="both")
            
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error al mostrar la boleta: {e}", icon="warning")

    def configurar_pestana1(self):
        # Dividir la Pestaña 1 en dos frames
        frame_formulario = ctk.CTkFrame(self.tab1)
        frame_formulario.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_treeview = ctk.CTkFrame(self.tab1)
        frame_treeview.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Formulario en el primer frame
        label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre del Ingrediente:")
        label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_formulario)
        self.entry_nombre.pack(pady=5)

        label_cantidad = ctk.CTkLabel(frame_formulario, text="Unidad:")
        label_cantidad.pack(pady=5)
        self.combo_unidad = ctk.CTkComboBox(frame_formulario, values=["kg", "unid"])
        self.combo_unidad.pack(pady=5)

        label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad:")
        label_cantidad.pack(pady=5)
        self.entry_cantidad = ctk.CTkEntry(frame_formulario)
        self.entry_cantidad.pack(pady=5)

        self.boton_ingresar = ctk.CTkButton(frame_formulario, text="Ingresar Ingrediente")
        self.boton_ingresar.configure(command=self.ingresar_ingrediente)
        self.boton_ingresar.pack(pady=10)

        self.boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar Ingrediente", fg_color="black", text_color="white")
        self.boton_eliminar.configure(command=self.eliminar_ingrediente)
        self.boton_eliminar.pack(pady=10)

        self.tree = ttk.Treeview(self.tab1, columns=("Nombre", "Unidad","Cantidad"), show="headings",height=25)
        
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Unidad", text="Unidad")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.boton_generar_menu = ctk.CTkButton(frame_treeview, text="Generar Menú", command=self.generar_menus)
        self.boton_generar_menu.pack(pady=10)
    def tarjeta_click(self, event, menu):
        suficiente_stock = True
        if self.stock.lista_ingredientes==[]:
            suficiente_stock=False
        for ingrediente_necesario in menu.ingredientes:
            for ingrediente_stock in self.stock.lista_ingredientes:
                if ingrediente_necesario.nombre == ingrediente_stock.nombre:
                    if int(ingrediente_stock.cantidad) < int(ingrediente_necesario.cantidad):
                        suficiente_stock = False
                        break
            if not suficiente_stock:
                break
        
        if suficiente_stock:
            for ingrediente_necesario in menu.ingredientes:
                for ingrediente_stock in self.stock.lista_ingredientes:
                    if ingrediente_necesario.nombre == ingrediente_stock.nombre:
                        ingrediente_stock.cantidad = str(int(ingrediente_stock.cantidad) - int(ingrediente_necesario.cantidad))
            
            self.pedido.agregar_menu(menu)
            self.actualizar_treeview_pedido()
            total = self.pedido.calcular_total()
            self.label_total.configure(text=f"Total: ${total:.2f}")
        else:
            CTkMessagebox(title="Stock Insuficiente", message=f"No hay suficientes ingredientes para preparar el menú '{menu.nombre}'.", icon="warning")
    
    def cargar_icono_menu(self, ruta_icono):
        imagen = Image.open(ruta_icono)
        icono_menu = ctk.CTkImage(imagen, size=(64, 64))
        return icono_menu

    
    def generar_menus(self):
        # Limpiar tarjetas existentes
        for widget in tarjetas_frame.winfo_children():
            widget.destroy()
        self.menus_creados.clear()
        
        # Crear tarjetas para cada menú disponible
        for menu in self.menus:
            if menu.nombre not in self.menus_creados:
                self.crear_tarjeta(menu)
                self.menus_creados.add(menu.nombre)

    def eliminar_menu(self):
        seleccion = self.treeview_menu.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Selecciona un menú del pedido para eliminar.", icon="warning")
            return
        
        # Obtener el nombre del menú seleccionado
        item = self.treeview_menu.item(seleccion[0])
        nombre_menu = item['values'][0]  # Primera columna es el nombre
        
        # Eliminar del pedido
        self.pedido.eliminar_menu(nombre_menu)
        
        # Actualizar vista y total
        self.actualizar_treeview_pedido()
        total = self.pedido.calcular_total()
        self.label_total.configure(text=f"Total: ${total:.2f}")
        
        CTkMessagebox(title="Éxito", message=f"Menú '{nombre_menu}' eliminado del pedido.", icon="check")

    def generar_boleta(self):
        if not self.pedido.menus:
            CTkMessagebox(title="Error", message="No hay items en el pedido para generar la boleta.", icon="warning")
            return
        
        try:
            boleta_facade = BoletaFacade(self.pedido)
            mensaje = boleta_facade.generar_boleta()
            CTkMessagebox(title="Éxito", message=mensaje, icon="check")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error al generar la boleta: {e}", icon="warning")

    def configurar_pestana2(self):
        frame_superior = ctk.CTkFrame(self.tab2)
        frame_superior.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        frame_intermedio = ctk.CTkFrame(self.tab2)
        frame_intermedio.pack(side="top", fill="x", padx=10, pady=5)

        global tarjetas_frame
        tarjetas_frame = ctk.CTkFrame(frame_superior)
        tarjetas_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.boton_eliminar_menu = ctk.CTkButton(frame_intermedio, text="Eliminar Menú", command=self.eliminar_menu)
        self.boton_eliminar_menu.pack(side="right", padx=10)

        self.label_total = ctk.CTkLabel(frame_intermedio, text="Total: $0.00", anchor="e", font=("Helvetica", 12, "bold"))
        self.label_total.pack(side="right", padx=10)

        frame_inferior = ctk.CTkFrame(self.tab2)
        frame_inferior.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

        self.treeview_menu = ttk.Treeview(frame_inferior, columns=("Nombre", "Cantidad", "Precio Unitario"), show="headings")
        self.treeview_menu.heading("Nombre", text="Nombre del Menú")
        self.treeview_menu.heading("Cantidad", text="Cantidad")
        self.treeview_menu.heading("Precio Unitario", text="Precio Unitario")
        self.treeview_menu.pack(expand=True, fill="both", padx=10, pady=10)

        self.boton_generar_boleta=ctk.CTkButton(frame_inferior,text="Generar Boleta",command=self.generar_boleta)
        self.boton_generar_boleta.pack(side="bottom",pady=10)

    def crear_tarjeta(self, menu):
        num_tarjetas = len(self.menus_creados)
        fila = 0
        columna = num_tarjetas

        tarjeta = ctk.CTkFrame(
            tarjetas_frame,
            corner_radius=10,
            border_width=1,
            border_color="#4CAF50",
            width=64,
            height=140,
            fg_color="gray",
        )
        tarjeta.grid(row=fila, column=columna, padx=15, pady=15, sticky="nsew")

        tarjeta.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))
        tarjeta.bind("<Enter>", lambda event: tarjeta.configure(border_color="#FF0000"))
        tarjeta.bind("<Leave>", lambda event: tarjeta.configure(border_color="#4CAF50"))

        if getattr(menu, "icono_path", None):
            try:
                icono = self.cargar_icono_menu(menu.icono_path)
                imagen_label = ctk.CTkLabel(
                    tarjeta, image=icono, width=64, height=64, text="", bg_color="transparent"
                )
                imagen_label.image = icono
                imagen_label.pack(anchor="center", pady=5, padx=10)
                imagen_label.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))
            except Exception as e:
                print(f"No se pudo cargar la imagen '{menu.icono_path}': {e}")

        texto_label = ctk.CTkLabel(
            tarjeta,
            text=f"{menu.nombre}",
            text_color="black",
            font=("Helvetica", 12, "bold"),
            bg_color="transparent",
        )
        texto_label.pack(anchor="center", pady=1)
        texto_label.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))

    def validar_nombre(self, nombre):
        if re.match(r"^[a-zA-Z\s]+$", nombre):
            return True
        else:
            CTkMessagebox(title="Error de Validación", message="El nombre debe contener solo letras y espacios.", icon="warning")
            return False

    def validar_cantidad(self, cantidad):
        if cantidad.isdigit():
            return True
        else:
            CTkMessagebox(title="Error de Validación", message="La cantidad debe ser un número entero positivo.", icon="warning")
            return False

    def ingresar_ingrediente(self):
        nombre = self.entry_nombre.get().strip()
        unidad = self.combo_unidad.get()
        cantidad_str = self.entry_cantidad.get().strip()
        
        if not nombre:
            CTkMessagebox(title="Error", message="El nombre del ingrediente no puede estar vacío.", icon="warning")
            return
            
        if not self.validar_nombre(nombre):
            return
            
        if not cantidad_str:
            CTkMessagebox(title="Error", message="La cantidad no puede estar vacía.", icon="warning")
            return
            
        try:
            cantidad = float(cantidad_str)
            if cantidad <= 0:
                CTkMessagebox(title="Error", message="La cantidad debe ser mayor a 0.", icon="warning")
                return
        except ValueError:
            CTkMessagebox(title="Error", message="La cantidad debe ser un número válido.", icon="warning")
            return
        
        ingrediente = Ingrediente(nombre, unidad, cantidad)
        self.stock.agregar_ingrediente(ingrediente)
        
        # Limpiar campos
        self.entry_nombre.delete(0, 'end')
        self.entry_cantidad.delete(0, 'end')
        
        # Actualizar vista
        self.actualizar_treeview()
        
        CTkMessagebox(title="Éxito", message=f"Ingrediente '{nombre}' agregado al stock.", icon="check")

    def eliminar_ingrediente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Selecciona un ingrediente para eliminar.", icon="warning")
            return
        
        # Obtener el nombre del ingrediente seleccionado
        item = self.tree.item(seleccion[0])
        nombre_ingrediente = item['values'][0]  # Primera columna es el nombre
        
        # Confirmar eliminación
        respuesta = CTkMessagebox(
            title="Confirmar", 
            message=f"¿Estás seguro de que quieres eliminar '{nombre_ingrediente}'?", 
            icon="question",
            option_1="Sí",
            option_2="No"
        )
        
        if respuesta.get() == "Sí":
            self.stock.eliminar_ingrediente(nombre_ingrediente)
            self.actualizar_treeview()
            CTkMessagebox(title="Éxito", message=f"Ingrediente '{nombre_ingrediente}' eliminado.", icon="check")

if __name__ == "__main__":
    import customtkinter as ctk
    from tkinter import ttk

    ctk.set_appearance_mode("Dark")  
    ctk.set_default_color_theme("blue") 
    ctk.set_widget_scaling(1.0)
    ctk.set_window_scaling(1.0)

    app = AplicacionConPestanas()

    try:
        style = ttk.Style(app)   
        style.theme_use("clam")
    except Exception:
        pass


    app.mainloop()
