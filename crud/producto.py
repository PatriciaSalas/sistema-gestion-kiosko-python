from conexion import ObjetoConexion
from clases import Producto


def crear_producto(nombre, precio_neto, stock):
    # inserta nuevo producto en bd
    try:
        ObjetoConex = ObjetoConexion()
        conexion = ObjetoConex.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO PRODUCTO (NOMBRE, PRECIO_NETO, STOCK)
        VALUES (:1, :2, :3)
        """
        cursor.execute(sql, (nombre, precio_neto, stock))
        conexion.commit()
        cursor.close()
        return True, "producto creado exitosamente"
    except Exception as e:
        return False, f"error al crear producto: {e}"


def obtener_productos():
    # retorna todos los productos
    try:
        ObjetoConex = ObjetoConexion()
        conexion = ObjetoConex.obtener_conexion()
        cursor = conexion.cursor()

        sql = "SELECT ID_PRODUCTO, NOMBRE, PRECIO_NETO, STOCK FROM PRODUCTO"
        cursor.execute(sql)
        resultado = cursor.fetchall()
        cursor.close()
        return resultado
    except Exception as e:
        print(f"error al obtener productos: {e}")
        return []


def obtener_producto_por_id(id_producto):
    # busca producto por id
    try:
        ObjetoConex = ObjetoConexion()
        conexion = ObjetoConex.obtener_conexion()
        cursor = conexion.cursor()

        sql = "SELECT ID_PRODUCTO, NOMBRE, PRECIO_NETO, STOCK FROM PRODUCTO WHERE ID_PRODUCTO = :1"
        cursor.execute(sql, (id_producto,))
        resultado = cursor.fetchone()
        cursor.close()

        if resultado:
            return Producto(*resultado)
        return None
    except Exception as e:
        print(f"error al obtener producto: {e}")
        return None


def actualizar_producto(id_producto, nombre, precio_neto, stock):
    # actualiza datos del producto
    try:
        ObjetoConex = ObjetoConexion()
        conexion = ObjetoConex.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE PRODUCTO 
        SET NOMBRE = :1, PRECIO_NETO = :2, STOCK = :3
        WHERE ID_PRODUCTO = :4
        """
        cursor.execute(sql, (nombre, precio_neto, stock, id_producto))
        conexion.commit()
        cursor.close()
        return True, "producto actualizado exitosamente"
    except Exception as e:
        return False, f"error al actualizar producto: {e}"


def eliminar_producto(id_producto):
    # elimina producto de la bd
    try:
        ObjetoConex = ObjetoConexion()
        conexion = ObjetoConex.obtener_conexion()
        cursor = conexion.cursor()

        sql = "DELETE FROM PRODUCTO WHERE ID_PRODUCTO = :1"
        cursor.execute(sql, (id_producto,))
        conexion.commit()
        cursor.close()
        return True, "producto eliminado exitosamente"
    except Exception as e:
        return False, f"error al eliminar producto: {e}"
