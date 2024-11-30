from jwcrypto import jwt, jwk
import json
from control_usuario import user_password_correcto
from flask_exceptions import *

def generate_token(usuario:str,contraseña:str) -> tuple[str,str] :

    key = jwk.JWK(generate='oct', size=256)

    Token = jwt.JWT(header={"alg": "HS256"},
                claims={"usuario": usuario,
                        "contrasenia" : contraseña})
    
    Token.make_signed_token(key)
    return key,Token.serialize()

def deserialize_token(key : str,token:str) -> str :

    ET = jwt.JWT(key=key, jwt=token, expected_type="JWS")

    return ET.claims

def token_correcto(dict_usuarios : dict[str,str],payload : str) :

    login = json.loads(payload)

    usuario = login["usuario"]
    contraseña = login["contrasenia"]

    return user_password_correcto(dict_usuarios,usuario,contraseña)

def comprobar_cookies(dict_usuarios : dict[str,str],cookies : dict[str,str]):

    try:

       jwk = cookies["jwk_token"]
       jwt = cookies["jwt_token"]

       return token_correcto(dict_usuarios,deserialize_token(jwk,jwt))
    
    except Exception:
        raise InvalidCredentialsException("")
    except KeyError:
        raise InvalidCredentialsException("")