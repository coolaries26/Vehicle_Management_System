from fastapi import FastAPI
from fastapi import Request

from fastapi.responses import JSONResponse

from app.services.exceptions import (
    DuplicateRecordException,
    NotFoundException,
    ValidationException,
)


def register_exception_handlers(
    app: FastAPI,
) -> None:

    @app.exception_handler(
        NotFoundException
    )
    async def not_found_handler(
        request: Request,
        exc: NotFoundException,
    ):

        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": str(exc),
            },
        )

    @app.exception_handler(
        DuplicateRecordException
    )
    async def duplicate_handler(
        request: Request,
        exc: DuplicateRecordException,
    ):

        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "message": str(exc),
            },
        )

    @app.exception_handler(
        ValidationException
    )
    async def validation_handler(
        request: Request,
        exc: ValidationException,
    ):

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": str(exc),
            },
        )

    @app.exception_handler(
        Exception
    )
    async def generic_handler(
        request: Request,
        exc: Exception,
    ):

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message":
                "Internal Server Error",
            },
        )