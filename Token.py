import time
import jwt
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()
security = HTTPBearer()
SECRET_KEY = "mysecretkey"

@app.get("/generate_token")
async def generate_token():
    payload = {
        "sub": "1234567890",
        "name": "Aaron Mojica",
        "iat": int(time.time()),
        "exp": int(time.time()) + 300  # expires in 5 minutes
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return {"token": token}

@app.get("/protected_directory")
async def protected_directory(authorization: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = authorization.credentials
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # Verify expiration time
        if time.time() > decoded_token["exp"]:
            raise HTTPException(status_code=401, detail="Token has expired")
        return {"content": "Bienvenido al directorio protegido!"}
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
