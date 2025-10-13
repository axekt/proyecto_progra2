from Ingrediente import Ingrediente

class Stock:
    def __init__(self):
        self.lista_ingredientes = []

    def agregar_ingrediente(self, ingrediente):
        # Verificar si el ingrediente ya existe
        for ing in self.lista_ingredientes:
            if ing.nombre == ingrediente.nombre and ing.unidad == ingrediente.unidad:
                # Si existe, sumar las cantidades
                ing.cantidad += float(ingrediente.cantidad)
                return
        
        # Si no existe, agregarlo a la lista
        self.lista_ingredientes.append(ingrediente)

    def eliminar_ingrediente(self, nombre_ingrediente):
        # Buscar y eliminar el ingrediente por nombre
        self.lista_ingredientes = [ing for ing in self.lista_ingredientes 
                                  if ing.nombre != nombre_ingrediente]    

    def verificar_stock(self):
        # Retorna True si hay ingredientes en stock, False si está vacío
        return len(self.lista_ingredientes) > 0

    def actualizar_stock(self, nombre_ingrediente, nueva_cantidad):
        # Actualizar la cantidad de un ingrediente existente
        for ingrediente in self.lista_ingredientes:
            if ingrediente.nombre == nombre_ingrediente:
                ingrediente.cantidad = float(nueva_cantidad)
                return True
        return False  # Ingrediente no encontrado

    def obtener_elementos_menu(self):
        # Retorna la lista de ingredientes disponibles
        return self.lista_ingredientes.copy()
    
    def buscar_ingrediente(self, nombre_ingrediente):
        # Busca un ingrediente por nombre y retorna su objeto o None
        for ingrediente in self.lista_ingredientes:
            if ingrediente.nombre == nombre_ingrediente:
                return ingrediente
        return None
    
    def hay_suficiente_stock(self, nombre_ingrediente, cantidad_necesaria):
        # Verifica si hay suficiente cantidad de un ingrediente específico
        ingrediente = self.buscar_ingrediente(nombre_ingrediente)
        if ingrediente:
            return float(ingrediente.cantidad) >= float(cantidad_necesaria)
        return False
    
    def consumir_ingrediente(self, nombre_ingrediente, cantidad_a_consumir):
        # Reduce la cantidad de un ingrediente (útil para pedidos)
        for ingrediente in self.lista_ingredientes:
            if ingrediente.nombre == nombre_ingrediente:
                nueva_cantidad = float(ingrediente.cantidad) - float(cantidad_a_consumir)
                if nueva_cantidad >= 0:
                    ingrediente.cantidad = nueva_cantidad
                    return True
                else:
                    return False  # No hay suficiente stock
        return False  # Ingrediente no encontrado

