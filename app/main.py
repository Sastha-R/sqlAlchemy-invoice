from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import InvoiceAlreadyExistsError, InvoiceNotFoundError
from app.routes.route import invoice_router
from app.routes.cookies import cookie_router
from sqlalchemy.exc import SQLAlchemyError
from app.routes.reports import report_route

app = FastAPI(title="Invoice Management CRUD API")
app.include_router(invoice_router)
app.include_router(report_route)
app.include_router(cookie_router)



@app.exception_handler(InvoiceNotFoundError)
def invoice_not_found_handler(request: Request, exc: InvoiceNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": str(exc)})


@app.exception_handler(InvoiceAlreadyExistsError)
def invoice_already_exists_handler(request: Request, exc: InvoiceAlreadyExistsError) -> JSONResponse:
    return JSONResponse(status_code=409, content={"message": str(exc)})


@app.exception_handler(SQLAlchemyError)
def  sqlalchemy_error_handler(request : Request , exc : SQLAlchemyError) -> JSONResponse:
    return JSONResponse(status_code=500 , content={"message": str(exc)})