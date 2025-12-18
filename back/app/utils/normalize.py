from __future__ import annotations

def normalize_email(email: str) -> str:
    return email.strip().lower()

def normalize_codigo(codigo: str) -> str:
    return codigo.strip().upper()
