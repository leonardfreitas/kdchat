import secrets

def gen(public_key, secret_key):
    token = secret_key+public_key
    return token

def decrypt(secret_key, token):
    public_key = token.split(secret_key)
    return public_key
