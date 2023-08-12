import jwt  

def encode(user_credentials ) :
    encode_jwt = jwt.encode(user_credentials,"secret",algorithm="HS256")
    return encode_jwt

def decode(encode) : 
    decode_jwt = jwt.decode(encode,"secret",algorithms=['HS256'])
    return decode_jwt
