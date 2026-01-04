# validaciones.py

import re
import bcrypt


# 1. Hashing de Contraseña (bcrypt) 
def hashear_contrasena(contrasena):
    """Genera un salt y hashea la contraseña usando bcrypt."""
    hashed = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def verificar_contrasena(contrasena, hash_guardado):
    """Verifica si la contraseña coincide con el hash almacenado."""
    return bcrypt.checkpw(contrasena.encode('utf-8'), hash_guardado.encode('utf-8'))

# 2. Validación de Correo (Expresión Regular) 
def validar_correo(correo):
    """Valida el formato de un correo electrónico usando una expresión regular."""
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.fullmatch(regex, correo) is not None

# 3. Validación y Formato de RUT Chileno
def formatear_rut(rut):
    """
    Limpia y da formato a un RUT (ej: 12345678-9 -> 12.345.678-9).
    """
    rut_limpio = rut.upper().replace('.', '').replace('-', '').strip()
    
    if len(rut_limpio) < 2:
        return rut_limpio
    
    dv = rut_limpio[-1]
    cuerpo = rut_limpio[:-1]
    
    # Lógica de formato
    formato = ""
    while cuerpo:
        formato = cuerpo[-3:] + "." + formato
        cuerpo = cuerpo[:-3]
    
    return (formato[:-1] + "-" + dv).lstrip('.')

def validar_rut(rut):
    """
    Valida el RUT usando la fórmula de Módulo 11 (algoritmo propio) para asegurar el DV.
    """
    if not rut or not isinstance(rut, str):
        return False

    # 1. Limpieza estricta y conversión a MAYÚSCULA
    rut_limpio = rut.strip().replace('.', '').replace('-', '').upper()

    if len(rut_limpio) < 2 or not rut_limpio[:-1].isdigit():
        return False

    # Separar cuerpo y DV
    dv_ingresado = rut_limpio[-1]
    cuerpo_rut = rut_limpio[:-1]

    # 2. Algoritmo Módulo 11
    s = 0
    multiplicador = 2
    
    for digito in reversed(cuerpo_rut):
        s += int(digito) * multiplicador
        multiplicador += 1
        if multiplicador == 8:
            multiplicador = 2

    resto = s % 11
    dv_calculado = 11 - resto

    # 3. Conversión de resultado a carácter
    if dv_calculado == 11:
        dv_final = '0'
    elif dv_calculado == 10:
        dv_final = 'K'
    else:
        dv_final = str(dv_calculado)

    # 4. Comparación final
    return dv_ingresado == dv_final