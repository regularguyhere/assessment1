from typing import Dict, Callable, List

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from app.api import error_handler, router
from app.core.middlewares import AuthenticationMiddleware
from app.core.exceptions import CoreException
from app.core.services.fhir.models import *
from app.database import Model, engine


def make_middleware() -> List[Middleware]:
    middleware = [
        # Just an example default middleware
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            route_prefixes=["/api"],
        )
    ]
    return middleware


def make_exception_handlers() -> Dict[Exception, Callable]:
    return {
        CoreException: error_handler,
    }


def init_db():
    """Initialize the database."""
    # TODO: use alembic
    Model.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="EMIS Group Data Engineer Technical Assesment",
        description=(
            "Application to receive a patient data from "
            "external system/supplier and transform it into "
            "more workeable for analytics team format."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        middleware=make_middleware(),
        exception_handlers=make_exception_handlers(),
    )
    app_.include_router(router)
    init_db()
    return app_


app = create_app()
