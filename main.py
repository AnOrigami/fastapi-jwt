import uvicorn
from fastapi import FastAPI
from api import apiRouter
app = FastAPI()
app.include_router(apiRouter)
if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)
