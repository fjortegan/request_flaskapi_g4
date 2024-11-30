from jwcrypto import jwt, jwk
from token_processing import generate_token,deserialize_token,token_correcto

usuario = "juan"
contraseña = "1234"

key,token = generate_token(usuario,contraseña)

print(key,token)

payloads = deserialize_token(key,token)

print(payloads)

print(token_correcto({"juan" : "1234"},payloads))