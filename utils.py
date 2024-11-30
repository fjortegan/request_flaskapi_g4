import json

def procesar_body_usuario_contraseña(body) :

    if isinstance(body, dict):
        login = body
    else:
        login = json.loads(body)  # Decodifica si es cadena JSON

    # Extrae usuario y contraseña
    user = login.get("usuario")
    password = login.get("contraseña")

    if not user or not password:
        raise ValueError("Faltan campos de usuario o contraseña.")

    return user, password