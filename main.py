import uvicorn
from fastapi import APIRouter, FastAPI

# from src.configs.pydantic_env.pydantic_settings_config import PydanticEnv
# from src.infra.repository.run_migrations_repository_infra import (
#     run_migrations_repository,
# )
# from src.main.routes.login.login_routes import LoginRoutes
# from src.main.routes.user.user_routes import UserRoutes


# run_migrations_repository()

# app = FastAPI()

# user_router = UserRoutes(APIRouter(), "/user")
# user_router.setup_routes()
# login_router = LoginRoutes(APIRouter(), "/login")
# login_router.setup_routes()


# app.include_router(user_router._router)
# app.include_router(login_router._router)


if __name__ == "__main__":
    port = 8000  # PydanticEnv().port
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
