from ElementoMenu import CrearMenu 
class Pedido:
    def __init__(self):
        self.menus = []   #basicamente esto es una lista de menus que contiene los menus que se han agregado al pedido

    def agregar_menu(self, menu: CrearMenu):
        # Buscar si el menú ya existe en el pedido
        for m in self.menus:
            if m.nombre == menu.nombre:
                m.cantidad += 1  # Incrementar cantidad si ya existe
                return
        
        # Si no existe, crear una copia y agregarla
        menu_copia = CrearMenu(
            nombre=menu.nombre,
            ingredientes=menu.ingredientes.copy(),
            precio=menu.precio,
            icono_path=menu.icono_path,
            cantidad=1
        )
        self.menus.append(menu_copia)

    def eliminar_menu(self, nombre_menu: str):
        # Eliminar el menú del pedido por nombre, funciona de la siguiente manera:
        # crea una nueva lista de menus que incluye todos los menus cuyo nombre no coincide con el
        # Eliminar el menú del pedido por nombre
        #___________________________________#
        self.menus = [menu for menu in self.menus if menu.nombre != nombre_menu]

    def mostrar_pedido(self): # Muestra el detalle del pedido
        #___________________________________#


        if not self.menus:
            return "El pedido está vacío."
        
        detalle = "=== PEDIDO ===\n"
        for menu in self.menus:
            subtotal = menu.precio * menu.cantidad
            detalle += f"{menu.nombre} x{menu.cantidad} - ${menu.precio:.2f} c/u = ${subtotal:.2f}\n"
        
        total = self.calcular_total()
        detalle += f"\nTOTAL: ${total:.2f}"
        return detalle
#___________________________________# aca se modifico calcular total ya que estaba vacio, 
                                    # se agrego el codigo que calcula el total del pedido, el cual finciona de la siguiente manera:
                                    # para cada menu en el pedido multiplica su precio por la cantidad y lo suma al total
    def calcular_total(self) -> float:
        total = 0.0
        for menu in self.menus:
            total += menu.precio * menu.cantidad
        return total
