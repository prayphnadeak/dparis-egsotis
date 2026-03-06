"""Standard API response formatter."""
from typing import Any, Optional


def success(data: Any, message: str = "Berhasil", status_code: int = 200) -> dict:
    return {"success": True, "message": message, "data": data, "status_code": status_code}


def error(message: str, status_code: int = 400, detail: Optional[Any] = None) -> dict:
    return {"success": False, "message": message, "detail": detail, "status_code": status_code}


def created(data: Any, message: str = "Data berhasil dibuat") -> dict:
    return success(data, message, 201)


def not_found(entity: str = "Data") -> dict:
    return error(f"{entity} tidak ditemukan", 404)
