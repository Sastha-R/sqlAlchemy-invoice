from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from database.database import init_db
from exceptions.custom_exceptions import InvoiceAlreadyExistsError, InvoiceNotFoundError
from routes.route import invoice_router

app = FastAPI(title="Invoice Management CRUD API")
app.include_router(invoice_router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.exception_handler(InvoiceNotFoundError)
def invoice_not_found_handler(request: Request, exc: InvoiceNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": str(exc)})


@app.exception_handler(InvoiceAlreadyExistsError)
def invoice_already_exists_handler(
    request: Request, exc: InvoiceAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"message": str(exc)})
