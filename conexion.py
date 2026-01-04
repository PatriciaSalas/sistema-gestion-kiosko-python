# conexion.py

import oracledb
import os
from dotenv import load_dotenv

load_dotenv() 

class ObjetoConexion:
    def __init__(self):
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.service = os.getenv("DB_SERVICE")
        if not all([self.user, self.password, self.host, self.port, self.service]):
             raise ValueError("Faltan credenciales en el archivo .env")

        self.dsn = f"{self.host}:{self.port}/{self.service}"


    def obtener_conexion(self):
        try:
            connection = oracledb.connect(
                user=self.user, 
                password=self.password, 
                dsn=self.dsn
            )
            return connection
        
        except oracledb.Error as e:
            error, = e.args
            print(f"Error al conectar a Oracle XE: Código {error.code}, Mensaje: {error.message}")
            return None