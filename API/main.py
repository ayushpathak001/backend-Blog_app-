from fastapi import FastAPI
from routes import auth , users , password_reset
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve static files 
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/" , tags=["Check Route API"])
def read_root():
    return {
        "Hello" : "World.."
    }


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(password_reset.router)

