# 🛒 Sistema de Gestión "El Objeto Feliz" - Evaluación POO

## 📝 Descripción del Proyecto
Este sistema es una solución integral para la gestión de ventas y usuarios de un kiosko. Fue desarrollado como una evaluación práctica para la asignatura de **Programación Orientada a Objetos (POO)**, integrando una arquitectura de software robusta, bases de datos relacionales y consumo de servicios externos.

El proyecto destaca por su separación de responsabilidades, permitiendo la gestión de inventario, carritos de compra, autenticación segura y conversión de divisas en tiempo real.

## 👥 Autores (Trabajo Colaborativo)
Este proyecto fue desarrollado en conjunto por:
- **Patricia Salas** – [GitHub Profile](https://github.com/PatriciaSalas)
- **Gonzalo Steppes** – [GitHub Profile](https://github.com/gsttps)

## 🛠️ Tecnologías Utilizadas
- **Lenguaje:** Python 3.x  
- **Interfaz Gráfica:** Tkinter (GUI)  
- **Base de Datos:** Oracle Database (utilizando la librería `oracledb`)  
- **Seguridad:** `bcrypt` para el hashing de contraseñas  
- **APIs:** Consumo de *Mindicador.cl* para la obtención del valor del dólar actual  

## 🏗️ Arquitectura y Principios de POO Aplicados
El código fue diseñado siguiendo los pilares fundamentales de la POO:

- **Abstracción y Herencia:**  
  Uso de una clase base `Persona` de la cual heredan `Cliente` y `Administrador`, compartiendo atributos básicos pero con métodos especializados.

- **Encapsulamiento:**  
  Protección de la lógica de negocio y validación de datos sensibles antes de la persistencia.

- **Polimorfismo:**  
  Implementación de métodos que se comportan de manera distinta según el tipo de usuario (Administrador vs Cliente).

- **Modularidad:**  
  Separación clara en capas:
  - `clases.py`: Lógica de negocio y modelos  
  - `conexion.py`: Gestión del pool de conexiones a Oracle  
  - `interfaz.py`: Capa de presentación y eventos de usuario  
  - `api.py`: Cliente para servicios externos  

## 🚀 Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/PatriciaSalas/tu-repositorio.git
   ```

2. **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configurar variables de entorno:**
    * Crea un archivo .env basado en .env.example
    * Ingresa tus credenciales de Oracle

4. **Ejecutar la aplicación:**
    ```bash
    python main.py
    ```

## 🔒 Seguridad
- Las contraseñas no se almacenan en texto plano; se utiliza **salting y hashing** mediante la librería `bcrypt`.
- Uso de **consultas parametrizadas** en SQL para prevenir ataques de **Inyección SQL**.

---

📚 Este proyecto es de carácter **académico**, orientado a demostrar competencias en **desarrollo backend**, **POO** y **arquitectura de software**.

## 📌 Aprendizajes
- Aplicación práctica de POO
- Manejo de base de datos Oracle
- Seguridad básica en aplicaciones backend
- Consumo de APIs externas