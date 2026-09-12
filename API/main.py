from fastapi import FastAPI
from routes import auth , users



app = FastAPI()


@app.get("/" , tags=["Check Route API"])
def read_root():
    return {
        "Hello" : "World.."
    }


app.include_router(users.router)
app.include_router(auth.router)




