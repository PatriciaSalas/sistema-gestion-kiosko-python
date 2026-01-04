# api.py

import requests

# URLs de APIs públicas de ejemplo
# API de Clima (ejemplo - se necesitaría una API Key real)
# CLIMA_URL = "http://api.openweathermap.org/data/2.5/weather?q=Santiago,cl&appid=TU_API_KEY&units=metric"

# API de conversión de moneda (ejemplo de API gratuita de Dolar/Chile)
DOLAR_URL = "https://mindicador.cl/api/dolar"

def obtener_datos_api(tipo_dato):
    try:
        if tipo_dato == "dolar":
            response = requests.get(DOLAR_URL)
            response.raise_for_status()
            data = response.json()

            valor = data["serie"][0]["valor"]
            fecha = data["serie"][0]["fecha"][:10]

            return {
                "moneda": data["nombre"],   
                "valor": f"${valor:.2f} CLP",
                "fecha": fecha
            }

        elif tipo_dato == "clima":
            return {
                "ciudad": "Santiago",
                "temperatura": "22°C",
                "descripcion": "Soleado",
                "humedad": "40%"
            }

        else:
            return {"error": "Tipo de dato de API no reconocido."}

    except requests.exceptions.RequestException as e:
        return {"error": f"Error de conexión con la API: {e}"}
    except (KeyError, IndexError):
        return {"error": "Error en la estructura de los datos de la API."}
