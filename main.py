from fastapi  import FastAPI
app = FastAPI()

def welcome():
    return {"message": "Welcome to the FastAPI application!"}
@app.get("/")
async def root():
    return welcome()
@app.get("/welcome")
async def welcome_endpoint():
    return welcome()
@app.get("/health")
async def health_check():
    return {"status": "healthy"}