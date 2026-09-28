from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, users, password_reset, blog_content
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        # Add your deployed frontend URL here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", tags=["Check Route API"])
def read_root():
    return {
        "Hello": "World.."
    }

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(password_reset.router)
app.include_router(blog_content.router)