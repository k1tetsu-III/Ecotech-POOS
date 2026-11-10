import math
from urllib.parse import quote

import requests

from persistencia.conexion import conexion_segura, marcador_sql


class ServicioExternoAPI:
    @staticmethod
    def obtener_clima(ciudad: str) -> dict:
        """Obtiene el clima actual y guarda la consulta en el historial."""
        if not isinstance(ciudad, str) or not ciudad.strip():
            raise ValueError("La ciudad debe ser un texto no vacío.")
        ciudad = ciudad.strip()
        url = f"https://wttr.in/{quote(ciudad, safe='')}?format=j1"

        try:
            respuesta = requests.get(url, timeout=5)
            respuesta.raise_for_status()
            datos = respuesta.json()
        except ValueError as error:
            raise RuntimeError(
                "La API climática devolvió una respuesta JSON inválida."
            ) from error
        except requests.exceptions.RequestException as error:
            raise RuntimeError(
                "No se pudo obtener la información climática. Intente más tarde."
            ) from error

        try:
            actual = datos["current_condition"][0]
            temperatura = float(actual["temp_C"])
            condicion = actual["weatherDesc"][0]["value"]
            humedad = int(actual["humidity"])
            if (
                not math.isfinite(temperatura)
                or not isinstance(condicion, str)
                or not condicion.strip()
                or not 0 <= humedad <= 100
            ):
                raise ValueError
            resultado = {
                "ciudad": ciudad,
                "temperatura": temperatura,
                "condicion": condicion.strip(),
                "humedad": humedad,
            }
        except (KeyError, IndexError, TypeError, ValueError) as error:
            raise RuntimeError(
                "La API climática devolvió datos incompletos o inválidos."
            ) from error

        marca = marcador_sql()
        with conexion_segura() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO historial_clima "
                f"(ciudad, temperatura, condicion, humedad) "
                f"VALUES ({marca}, {marca}, {marca}, {marca})",
                (
                    resultado["ciudad"],
                    resultado["temperatura"],
                    resultado["condicion"],
                    resultado["humedad"],
                ),
            )
        return resultado

    @staticmethod
    def obtener_indicador_economico(codigo_moneda: str) -> float:
        """Consulta un indicador económico y guarda el valor en el historial."""
        if not isinstance(codigo_moneda, str) or not codigo_moneda.strip():
            raise ValueError("El código de moneda debe ser un texto no vacío.")
        codigo_moneda = codigo_moneda.strip()
        url = f"https://mindicador.cl/api/{quote(codigo_moneda.lower(), safe='')}"

        try:
            respuesta = requests.get(url, timeout=5)
            respuesta.raise_for_status()
            datos = respuesta.json()
        except ValueError as error:
            raise RuntimeError(
                "La API económica devolvió una respuesta JSON inválida."
            ) from error
        except requests.exceptions.RequestException as error:
            raise RuntimeError(
                "Error al consultar el indicador económico externo."
            ) from error

        try:
            valor = float(datos["serie"][0]["valor"])
            if not math.isfinite(valor):
                raise ValueError
        except (KeyError, IndexError, TypeError, ValueError) as error:
            raise RuntimeError(
                "La API económica devolvió datos incompletos o inválidos."
            ) from error

        marca = marcador_sql()
        with conexion_segura() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO historial_indicador (codigo_moneda, valor) "
                f"VALUES ({marca}, {marca})",
                (codigo_moneda.upper(), valor),
            )
        return valor
