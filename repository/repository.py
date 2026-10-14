from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.models import Invoice
from schemas.schemas import InvoiceData


class InvoiceRepository:
    def create(self, db: Session, invoice_data: InvoiceData) -> Invoice:
        invoice = Invoice(**invoice_data.model_dump())
        try:
            db.add(invoice)
            db.commit()
            db.refresh(invoice)
            return invoice
        except SQLAlchemyError:
            db.rollback()
            raise

    def get_all(self, db: Session, limit: int, offset: int) -> list[Invoice]:
        statement = select(Invoice).order_by(Invoice.id).limit(limit).offset(offset)
        return list(db.execute(statement).scalars().all())

    def get_by_id(self, db: Session, invoice_id: int) -> Invoice | None:
        return db.get(Invoice, invoice_id)

    def get_by_invoice_number(self, db: Session, invoice_number: str) -> Invoice | None:
        statement = select(Invoice).where(Invoice.invoice_number == invoice_number)
        return db.execute(statement).scalar_one_or_none()

    def update(self, db: Session, invoice: Invoice, invoice_data: InvoiceData) -> Invoice:
        for field, value in invoice_data.model_dump().items():
            setattr(invoice, field, value)

        try:
            db.commit()
            db.refresh(invoice)
            return invoice
        except SQLAlchemyError:
            db.rollback()
            raise

    def delete(self, db: Session, invoice: Invoice) -> None:
        try:
            db.delete(invoice)
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise
