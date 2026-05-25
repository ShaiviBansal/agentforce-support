from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.auth import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models import Token, ChatMessage, ChatResponse
from app.agent import run_agent
from app.knowledge_base import populate_knowledge_base

app = FastAPI(title="Agentforce Support API")

# Allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Populate knowledge base on startup
@app.on_event("startup")
async def startup_event():
    populate_knowledge_base()

# Health check endpoint
@app.get("/")
def root():
    return {"status": "Agentforce Support API is running"}

# Login endpoint — returns a JWT token
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Chat endpoint — protected by JWT
@app.post("/chat", response_model=ChatResponse)
async def chat(
    message: ChatMessage,
    current_user: dict = Depends(get_current_user)
):
    result = run_agent(message.message)
    return ChatResponse(
        response=result["response"],
        sources=result["sources"]
    )

# Get current user info
@app.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"]}