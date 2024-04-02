import uvicorn
from fastapi import APIRouter, FastAPI
from src.configs.pydantic.pydantic_env_settings_config import PydanticEnv
from src.infra.repository.run_migrations_repository_infra import run_migrations

from src.infra.repository.seed.techs import techs_seed
from src.main.routes.login.login_routes import LoginRoutes
from src.main.routes.post.post_routes import PostRoutes
from src.main.routes.project.project_routes import ProjectRoutes
from src.main.routes.upload_image.upload_image_routes import UploadImageRoutes
from src.main.routes.user.user_routes import UserRoutes


run_migrations()
app = FastAPI()


async def execute_seeds():
    await techs_seed()


@app.on_event("startup")
async def startup_event():
    await execute_seeds()


user_router = UserRoutes(APIRouter(), "/user")
user_router.routes_setup()

login_router = LoginRoutes(APIRouter())
login_router.routes_setup()

project_router = ProjectRoutes(APIRouter(), "/project")
project_router.routes_setup()

upload_router = UploadImageRoutes(APIRouter(), "/upload")
upload_router.routes_setup()

post_router = PostRoutes(APIRouter(), "/post")
post_router.routes_setup()

app.include_router(user_router._router)
app.include_router(login_router._router)
app.include_router(project_router._router)
app.include_router(upload_router._router)
app.include_router(post_router._router)


if __name__ == "__main__":
    port = PydanticEnv().port
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
