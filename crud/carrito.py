from conexion import ObjetoConexion
from crud.cliente import obtener_cliente_por_rut
from crud.producto import obtener_producto_por_id
from clases import Carrito, ItemCarrito


def crear_carrito(rut_cliente):
    # crea un nuevo carrito para un cliente
    try:
        ObjetoConex = ObjetoConexion()
        conexion = ObjetoConex.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO CARRITO (RUT_CLIENTE, FECHA_CREACION)
        VALUES (:1, SYSDATE)
        """
        cursor.execute(sql, (rut_cliente,))
        conexion.commit()

        # obtener id del carrito recien creado
        cursor.execute(
            "SELECT MAX(ID_CARRITO) FROM CARRITO WHERE RUT_CLIENTE = :1", (rut_cliente,)
        )
        id_carrito = cursor.fetchone()[0]
        cursor.close()

        return True, id_carrito
    except Exception as e:
        return False, f"error al crear carrito: {e}"


def agregar_detalle(id_carrito, id_producto, cantidad):
    # agrega un producto al carrito
    try:
        ObjetoConex = ObjetoConexion()
        conexion = ObjetoConex.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO ITEM_CARRITO (ID_CARRITO, ID_PRODUCTO, CANTIDAD)
        VALUES (:1, :2, :3)
        """
        cursor.execute(sql, (id_carrito, id_producto, cantidad))
        conexion.commit()
        cursor.close()
        return True, "producto agregado al carrito"
    except Exception as e:
        return False, f"error al agregar producto: {e}"


def obtener_detalles_carrito(id_carrito):
    # obtiene todos los productos del carrito con join
    try:
        ObjetoConex = ObjetoConexion()
        conexion = ObjetoConex.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        SELECT p.ID_PRODUCTO, p.NOMBRE, p.PRECIO_NETO, p.STOCK, d.CANTIDAD
        FROM ITEM_CARRITO d
        JOIN PRODUCTO p ON d.ID_PRODUCTO = p.ID_PRODUCTO
        WHERE d.ID_CARRITO = :1
        """
        cursor.execute(sql, (id_carrito,))
        resultado = cursor.fetchall()
        cursor.close()
        return resultado
    except Exception as e:
        print(f"error al obtener detalles: {e}")
        return []


def calcular_totales(id_carrito, rut_cliente):
    # calcula subtotal, descuento y total del carrito
    try:
        detalles = obtener_detalles_carrito(id_carrito)
        ObjetoCliente = obtener_cliente_por_rut(rut_cliente)

        if not ObjetoCliente:
            return None

        # crear objeto carrito con sus detalles
        ObjetoCarrito = Carrito(id_carrito, ObjetoCliente)

        for detalle in detalles:
            id_prod, _, _, _, cantidad = detalle

            ObjetoProducto = obtener_producto_por_id(id_prod)
            if not ObjetoProducto:
                continue
            ObjetoDetalle = ItemCarrito(ObjetoProducto, cantidad)
            ObjetoCarrito.agregar_detalle(ObjetoDetalle)


        subtotal = ObjetoCarrito.calcular_subtotal()
        descuento = ObjetoCarrito.calcular_descuento()
        total = ObjetoCarrito.calcular_total()

        return {
            "subtotal": subtotal,
            "descuento": descuento,
            "total": total,
            "detalles": detalles,
            "cliente": ObjetoCliente,
        }
    except Exception as e:
        print(f"error al calcular totales: {e}")
        return None


def eliminar_carrito(id_carrito):
    # elimina carrito y sus detalles
    try:
        ObjetoConex = ObjetoConexion()
        conexion = ObjetoConex.obtener_conexion()
        cursor = conexion.cursor()

        # primero eliminar detalles
        sql1 = "DELETE FROM ITEM_CARRITO WHERE ID_CARRITO = :1"
        cursor.execute(sql1, (id_carrito,))

        # luego eliminar carrito
        sql2 = "DELETE FROM CARRITO WHERE ID_CARRITO = :1"
        cursor.execute(sql2, (id_carrito,))

        conexion.commit()
        cursor.close()
        return True, "carrito eliminado exitosamente"
    except Exception as e:
        return False, f"error al eliminar carrito: {e}"


def generar_voucher(id_carrito, rut_cliente):
    # genera texto del voucher completo
    totales = calcular_totales(id_carrito, rut_cliente)

    if not totales:
        return "error al generar voucher"

    voucher = "=" * 50 + "\n"
    voucher += "          KIOSKO OBJETO FELIZ\n"
    voucher += "=" * 50 + "\n\n"

    voucher += f"cliente: {totales['cliente'].nombre} {totales['cliente'].apellido}\n"
    voucher += f"rut: {totales['cliente'].rut}\n"
    voucher += f"nivel: {totales['cliente'].nivel}\n"
    voucher += "-" * 50 + "\n\n"

    voucher += "productos:\n"
    for detalle in totales["detalles"]:
        id_prod, nombre, precio_neto, stock, cantidad = detalle
        precio_con_iva = precio_neto * 1.19
        subtotal_item = precio_con_iva * cantidad
        voucher += f"  {nombre}\n"
        voucher += f"    cantidad: {cantidad}\n"
        voucher += f"    precio unitario con iva: ${precio_con_iva:.2f}\n"
        voucher += f"    subtotal: ${subtotal_item:.2f}\n\n"

    voucher += "-" * 50 + "\n"
    voucher += f"subtotal: ${totales['subtotal']:.2f}\n"
    voucher += f"descuento: ${totales['descuento']:.2f}\n"
    voucher += f"total a pagar: ${totales['total']:.2f}\n"
    voucher += "=" * 50 + "\n"

    return voucher
