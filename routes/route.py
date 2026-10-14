from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.schemas import InvoiceCreate, InvoicePatch
from services.services import InvoiceService

invoice_router = APIRouter(prefix="/invoices", tags=["Invoices"])
invoice_service = InvoiceService()


@invoice_router.post("/",status_code=status.HTTP_201_CREATED,)
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    return invoice_service.create_invoice(db, invoice)


@invoice_router.get("",)
def get_invoices(limit: int = 10,offset: int = 0,db: Session = Depends(get_db),):
    return invoice_service.get_invoices(db, limit, offset)


@invoice_router.get("/{invoice_id}")
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    return invoice_service.get_invoice_by_id(db, invoice_id)


@invoice_router.put("/{invoice_id}")
def update_invoice(invoice_id: int, invoice: InvoiceCreate,db: Session = Depends(get_db),):
    return invoice_service.update_invoice(db, invoice_id, invoice)


@invoice_router.patch("/{invoice_id}")
def patch_invoice(invoice_id: int,invoice: InvoicePatch,db: Session = Depends(get_db)):
    return invoice_service.patch_invoice(db, invoice_id, invoice)


@invoice_router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice_service.delete_invoice(db, invoice_id)
