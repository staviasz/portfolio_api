import asyncio
from sqlalchemy.orm import Session

from src.configs.repository.client_repository_config import SessionLocal
from src.infra.repository.models.tech_model_repository_infra import Tech


techs = [
    "adobe",
    "adonisjs",
    "alchemy",
    "amazon aws",
    "anaconda",
    "android",
    "android studio",
    "angular",
    "angularjs",
    "apache",
    "apple",
    "app Store",
    "aws lambda",
    "axios",
    "babel",
    "bit bucket",
    "bootstrap",
    "csharp",
    "css3",
    "cypress",
    "delphi",
    "django",
    "discord",
    "docker",
    ".net",
    "drupal",
    "eletron",
    "eslint",
    "express",
    "fastapi",
    "fastfy",
    "figma",
    "firebase",
    "flask",
    "flutter",
    "git",
    "gimp",
    "github",
    "gitlab",
    "go",
    "graphql",
    "gulp",
    "grunt",
    "html5",
    "javascript",
    "jenkins",
    "jest",
    "jira",
    "jquery",
    "kotlin",
    "kubernetes",
    "linux",
    "macos",
    "mariadb",
    "microsoft",
    "mocha",
    "mongodb",
    "mongoose",
    "mysql",
    "nestjs",
    "next.js",
    "nginx",
    "node.js",
    "notion",
    "npm",
    "numpy",
    "oracle",
    "pandas",
    "php",
    "phpstorm",
    "postman",
    "powerbi",
    "powershell",
    "postgresql",
    "prettier",
    "prisma",
    "prometheus",
    "pycharm",
    "pydantic",
    "pytest",
    "python",
    "pytorch",
    "rabbitmq",
    "react",
    "raspberry pi",
    "redis",
    "redux",
    "ruby",
    "ruby on rails",
    "rust",
    "selenium",
    "sequelize",
    "slack",
    "solid",
    "spring",
    "spring boot",
    "sqlalchemy",
    "sqlite",
    "storybook",
    "styled components",
    "swagger",
    "swarm",
    "tailwind css",
    "testing library",
    "trello",
    "typescript",
    "vercel",
    "virtual box",
    "vue.js",
    "visual studio code",
    "vite",
    "vitest",
    "vitex",
    "vuetify",
    "webpack",
    "wordpress",
    "windows",
    "yarn",
]

session = SessionLocal()


async def tech_exist(session: Session, tech: str):
    query = session.query(Tech).filter(Tech.name == tech).first()
    if not query:
        return tech
    return


async def techs_seed():
    techs_add = await asyncio.gather(*[tech_exist(session, tech) for tech in techs])

    for index, tech in enumerate(techs_add):
        if tech:
            add = {"id": index + 1, "name": tech}
            session.add(Tech(**add))

    session.commit()
