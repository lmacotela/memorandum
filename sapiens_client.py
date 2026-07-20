"""Cliente HTTP para la API de Sapiens Consulting."""
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("SAPIENS_BASE_URL", "https://empleados.sapiensconsultingperu.com")
USERNAME = os.getenv("SAPIENS_USERNAME")
PASSWORD = os.getenv("SAPIENS_PASSWORD")


async def obtener_token() -> str:
    """Paso 1: Login para obtener el Bearer token."""
    url = f"{BASE_URL}/apitest/api/Auth/Login"
    payload = {"username": USERNAME, "password": PASSWORD}

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()

    data = response.json()

    # El API retorna Code 404 cuando las credenciales no son válidas
    if data.get("Code") == 404:
        raise ValueError(f"Login fallido: {data.get('Message', 'Credenciales incorrectas')}")

    # Extraer el token del response
    objeto = data.get("Objeto") or {}
    token = (
        data.get("token")
        or data.get("Token")
        or data.get("Dato")
        or (objeto.get("AccessToken") if isinstance(objeto, dict) else None)
        or (objeto.get("token") if isinstance(objeto, dict) else None)
    )

    if not token:
        raise ValueError(f"Token no encontrado en la respuesta: {data}")

    return token


async def obtener_memorandums(token: str, from_date: str, to_date: str, user_ids: list[str]) -> list[dict]:
    """Paso 2: Obtener datos de memorandums desde el timesheet."""
    url = f"{BASE_URL}/apitest/api/TimesheetStatus/GetReporteMemorandumTimesheet"
    payload = {
        "fromDate": from_date,
        "toDate": to_date,
        "userIds": user_ids,
    }
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()

    data = response.json()

    if data.get("Code") not in (200, None):
        raise ValueError(f"Error al obtener memorandums: {data.get('Message')}")

    # El listado puede venir en Listado o directamente como lista
    registros = data.get("Listado") or data.get("Data") or data.get("data") or []

    if isinstance(data, list):
        registros = data

    return registros
