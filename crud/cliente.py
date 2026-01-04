from conexion import ObjetoConexion
from validaciones import (
    validar_rut,
    validar_correo,
    hashear_contrasena,
    verificar_contrasena,
    formatear_rut,
)
from clases import Cliente


def crear_cliente(rut, nombre, apellido, correo, telefono, contrasena, nivel):
    # inserta nuevo cliente en bd con validaciones
    if not validar_rut(rut):
        return False, "rut invalido"

    if not validar_correo(correo):
        return False, "correo invalido"

    try:
        ObjetoConex = ObjetoConexion()
        conexion = ObjetoConex.obtener_conexion()
        cursor = conexion.cursor()
        
        # Se formatea el RUT una vez más
        rut_final = formatear_rut(rut)

        # hashear contrasena antes de guardar
        hash_pass = hashear_contrasena(contrasena)

        sql = """
        INSERT INTO CLIENTE (RUT, NOMBRE, APELLIDO, CORREO, TELEFONO, CONTRASENA_HASH, NIVEL)
        VALUES (:1, :2, :3, :4, :5, :6, :7)
        """
        cursor.execute(sql, (rut_final, nombre, apellido, correo, telefono, hash_pass, nivel))
        conexion.commit()
        cursor.close()
        return True, "cliente creado exitosamente"
    except Exception as e:
        return False, f"error al crear cliente: {e}"


def obtener_clientes():
    # retorna todos los clientes
    try:
        ObjetoConex = ObjetoConexion()
        conexion = ObjetoConex.obtener_conexion()
        cursor = conexion.cursor()

        sql = "SELECT RUT, NOMBRE, APELLIDO, CORREO, TELEFONO, NIVEL FROM CLIENTE"
        cursor.execute(sql)
        resultado = cursor.fetchall()
        cursor.close()
        return resultado
    except Exception as e:
        print(f"error al obtener clientes: {e}")
        return []


def obtener_cliente_por_rut(rut):
    # busca cliente por rut
    try:
        ObjetoConex = ObjetoConexion()
        conexion = ObjetoConex.obtener_conexion()
        cursor = conexion.cursor()

        sql = "SELECT RUT, NOMBRE, APELLIDO, CORREO, TELEFONO, CONTRASENA_HASH, NIVEL FROM CLIENTE WHERE RUT = :1"
        cursor.execute(sql, (rut,))
        resultado = cursor.fetchone()
        cursor.close()

        if resultado:
            return Cliente(*resultado)
        return None
    except Exception as e:
        print(f"error al obtener cliente: {e}")
        return None


def actualizar_cliente(rut, nombre, apellido, correo, telefono, nivel):
    # actualiza datos del cliente
    if not validar_correo(correo):
        return False, "correo invalido"

    try:
        ObjetoConex = ObjetoConexion()
        conexion = ObjetoConex.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE CLIENTE 
        SET NOMBRE = :1, APELLIDO = :2, CORREO = :3, TELEFONO = :4, NIVEL = :5
        WHERE RUT = :6
        """
        cursor.execute(sql, (nombre, apellido, correo, telefono, nivel, rut))
        conexion.commit()
        cursor.close()
        return True, "cliente actualizado exitosamente"
    except Exception as e:
        return False, f"error al actualizar cliente: {e}"


def eliminar_cliente(rut):
    # elimina cliente de la bd
    try:
        ObjetoConex = ObjetoConexion()
        conexion = ObjetoConex.obtener_conexion()
        cursor = conexion.cursor()

        sql = "DELETE FROM CLIENTE WHERE RUT = :1"
        cursor.execute(sql, (rut,))
        conexion.commit()
        cursor.close()
        return True, "cliente eliminado exitosamente"
    except Exception as e:
        return False, f"error al eliminar cliente: {e}"

def autenticar_cliente(rut, contrasena):
    """
    Verifica si el rut existe y si la contraseña coincide con el hash almacenado.
    """
    try:
        cliente = obtener_cliente_por_rut(rut)

        if not cliente:
            return False, "cliente no existe"

        if verificar_contrasena(contrasena, cliente.contrasena_hash):
            return True, cliente
        else:
            return False, "contraseña incorrecta"

    except Exception as e:
        return False, f"error al autenticar cliente: {e}"