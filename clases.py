from abc import ABC, abstractmethod


class Persona(ABC):
    # clase base abstracta para personas
    def __init__(self, rut, nombre, apellido, correo, telefono):
        self.rut = rut
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.telefono = telefono

    @abstractmethod
    def obtener_info(self):
        # metodo abstracto para polimorfismo
        pass


class Cliente(Persona):
    # hereda de persona, agrega nivel y contrasena
    def __init__(
        self, rut, nombre, apellido, correo, telefono, contrasena_hash, nivel="General"
    ):
        super().__init__(rut, nombre, apellido, correo, telefono)
        self.contrasena_hash = contrasena_hash
        self.nivel = nivel  # General o Estudiante

    def obtener_info(self):
        # retorna informacion del cliente
        return f"{self.nombre} {self.apellido} - {self.nivel}"

    def aplicar_descuento(self, subtotal):
        # aplica 10% descuento si es estudiante
        if self.nivel == "Estudiante":
            return subtotal * 0.10
        return 0


class Producto:
    # representa un producto del kiosko
    def __init__(self, id_producto, nombre, precio_neto, stock):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio_neto = precio_neto
        self.stock = stock

    def calcular_precio_con_iva(self):
        # calcula precio con iva 19%
        return self.precio_neto * 1.19

    def obtener_info(self):
        # retorna informacion del producto
        return f"{self.nombre} - Neto: ${self.precio_neto} - Stock: {self.stock}"


class ItemCarrito:
    # detalle de cada producto en el carrito
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad

    def calcular_subtotal(self):
        # calcula subtotal del detalle
        precio_con_iva = self.producto.calcular_precio_con_iva()
        return precio_con_iva * self.cantidad


class Carrito:
    # composicion: carrito contiene detalles
    def __init__(self, id_carrito, cliente):
        self.id_carrito = id_carrito
        self.cliente = cliente  # asociacion con cliente
        self.detalles = []  # lista de DetalleCarrito

    def agregar_detalle(self, detalle):
        # agrega un detalle al carrito
        self.detalles.append(detalle)

    def calcular_subtotal(self):
        # suma todos los subtotales de los detalles
        return sum(detalle.calcular_subtotal() for detalle in self.detalles)

    def calcular_descuento(self):
        # calcula descuento segun nivel del cliente
        subtotal = self.calcular_subtotal()
        return self.cliente.aplicar_descuento(subtotal)

    def calcular_total(self):
        # calcula total final aplicando descuento
        subtotal = self.calcular_subtotal()
        descuento = self.calcular_descuento()
        return subtotal - descuento
