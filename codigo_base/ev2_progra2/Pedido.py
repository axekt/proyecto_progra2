from ElementoMenu import CrearMenu 
class Pedido:
    def __init__(self):
        self.menus = []  

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
        # Eliminar el menú del pedido por nombre
        self.menus = [menu for menu in self.menus if menu.nombre != nombre_menu]

    def mostrar_pedido(self):
        if not self.menus:
            return "El pedido está vacío."
        
        detalle = "=== PEDIDO ===\n"
        for menu in self.menus:
            subtotal = menu.precio * menu.cantidad
            detalle += f"{menu.nombre} x{menu.cantidad} - ${menu.precio:.2f} c/u = ${subtotal:.2f}\n"
        
        total = self.calcular_total()
        detalle += f"\nTOTAL: ${total:.2f}"
        return detalle

    def calcular_total(self) -> float:
        total = 0.0
        for menu in self.menus:
            total += menu.precio * menu.cantidad
        return total
