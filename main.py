from fastapi import FastAPI

from api.users import router as users_router
from core.config import settings
from core.database_utils import init_database

# from core.middleware import add_middleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for CRUD operations on widgets",
    version="1.0.0"
)

routers = [users_router, ]

# add_middleware(app)

for router in routers:
    app.include_router(router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    init_database()

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=443,
        reload=True,
        # ssl_keyfile=settings.SSL_KEYFILE,
        # ssl_certfile=settings.SSL_CERTFILE,
    )
