import uvicorn
from fastapi import APIRouter, FastAPI
from src.configs.pydantic.pydantic_env_settings_config import PydanticEnv

from src.main.routes.login.login_routes import LoginRoutes
from src.main.routes.post.post_routes import PostRoutes
from src.main.routes.project.project_routes import ProjectRoutes
from src.main.routes.tech.tech_routes import TechRoutes
from src.main.routes.upload_image.upload_image_routes import UploadImageRoutes
from src.main.routes.user.user_routes import UserRoutes


app = FastAPI(
    redoc_url="/redocs",
    title="Portfolio Api",
    description="""Bem-vindo à API de criação de portfólios! Esta API oferece recursos para
    gerenciar projetos, posts e tecnologias, permitindo aos usuários criar e personalizar
    seus portfólios online. Com endpoints para cadastrar projetos, criar posts, selecionar
    tecnologias para projetos e posts, esta API proporciona uma experiência flexível e robusta
    para os usuários compartilharem e destacarem seu trabalho e habilidades. Explore os
    endpoints disponíveis e comece a construir seu portfólio digital hoje mesmo!""",
    version="1.0.0",
)


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

tech_router = TechRoutes(APIRouter(), "/tech")
tech_router.routes_setup()

app.include_router(user_router._router)
app.include_router(login_router._router)
app.include_router(project_router._router)
app.include_router(upload_router._router)
app.include_router(post_router._router)
app.include_router(tech_router._router)


if __name__ == "__main__":
    port = PydanticEnv().port
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
