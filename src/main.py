from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from db import settings
import uvicorn

import api.v1.routes

from exceptions import (
    AppException,
    AppExceptionCase,
    app_exception_handler,
    generic_exception_handler,
)

app = FastAPI(title='FastAPI Auth')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppExceptionCase)
def custom_app_exception_handler(request: Request, exc: AppException):
    print(exc)
    return app_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "detail": exc.errors(),
                "body": exc.body,
                "your_additional_errors": {
                    "Will be": "Inside",
                    "This": " Error message",
                },
            }
        ),
    )


@app.exception_handler(ValidationError)
def validation_exception_handler(request: Request, exc: ValidationError):
    print(exc)
    return app_exception_handler(request, AppException.BadRequest(exc))


@app.exception_handler(Exception)
def custom_generic_exception_handler(request: Request, exc: Exception):
    print(exc)
    return generic_exception_handler(request, exc)


# Root API
@app.get("/")
async def root():
    return {"message": "FastAPI Authentication!"}


app.include_router(api.v1.routes.api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="127.0.0.3", port=8000, reload=True, log_level="info"
    )
