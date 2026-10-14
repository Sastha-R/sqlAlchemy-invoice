from decimal import Decimal
from sqlalchemy.orm import Session
from exceptions.custom_exceptions import InvoiceAlreadyExistsError, InvoiceNotFoundError
from repository.repository import InvoiceRepository
from schemas.schemas import InvoiceCreate, InvoiceData, InvoicePatch


class InvoiceService:
    def __init__(self) -> None:
        self.repository = InvoiceRepository()

    def create_invoice(self, db: Session, invoice: InvoiceCreate):
        existing_invoice = self.repository.get_by_invoice_number(db, invoice.invoice_number)
        if existing_invoice:
            raise InvoiceAlreadyExistsError("Invoice number already exists")

        invoice_data = self.build_invoice_data(invoice)
        return self.repository.create(db, invoice_data)

    def get_invoices(self, db: Session, limit: int, offset: int):
        return self.repository.get_all(db, limit, offset)

    def get_invoice_by_id(self, db: Session, invoice_id: int):
        invoice = self.repository.get_by_id(db, invoice_id)
        if invoice is None:
            raise InvoiceNotFoundError("Invoice not found")
        return invoice

    def update_invoice(self, db: Session, invoice_id: int, invoice: InvoiceCreate):
        existing_invoice = self.get_invoice_by_id(db, invoice_id)
        self.check_invoice_number_available(db, invoice.invoice_number, invoice_id)

        invoice_data = self.build_invoice_data(invoice)
        return self.repository.update(db, existing_invoice, invoice_data)

    def patch_invoice(self, db: Session, invoice_id: int, invoice: InvoicePatch):
        existing_invoice = self.get_invoice_by_id(db, invoice_id)
        updated_data = {
            "invoice_number": existing_invoice.invoice_number,
            "customer_name": existing_invoice.customer_name,
            "customer_email": existing_invoice.customer_email,
            "invoice_date": existing_invoice.invoice_date,
            "product_name": existing_invoice.product_name,
            "quantity": existing_invoice.quantity,
            "unit_price": existing_invoice.unit_price,
        }
        updated_data.update(invoice.model_dump(exclude_unset=True))

        self.check_invoice_number_available(db, updated_data["invoice_number"], invoice_id)

        invoice_create = InvoiceCreate(**updated_data)
        invoice_data = self.build_invoice_data(invoice_create)
        return self.repository.update(db, existing_invoice, invoice_data)

    def delete_invoice(self, db: Session, invoice_id: int) -> None:
        invoice = self.get_invoice_by_id(db, invoice_id)
        self.repository.delete(db, invoice)

    def check_invoice_number_available(
        self, db: Session, invoice_number: str, current_invoice_id: int
    ) -> None:
        invoice = self.repository.get_by_invoice_number(db, invoice_number)
        if invoice and invoice.id != current_invoice_id:
            raise InvoiceAlreadyExistsError("Invoice number already exists")

    def build_invoice_data(self, invoice: InvoiceCreate) -> InvoiceData:
        subtotal = invoice.quantity * invoice.unit_price

        if subtotal < 10000:
            discount_percentage = 5
        elif subtotal <= 50000:
            discount_percentage =10
        else:
            discount_percentage =15

        discount_amount = subtotal * discount_percentage / 100
        taxable_amount = subtotal - discount_amount
        tax_percentage = 18
        tax_amount = taxable_amount * tax_percentage / 100
        total_amount = taxable_amount + tax_amount

        return InvoiceData(
            invoice_number=invoice.invoice_number,
            customer_name=invoice.customer_name,
            customer_email=invoice.customer_email,
            invoice_date=invoice.invoice_date,
            product_name=invoice.product_name,
            quantity=invoice.quantity,
            unit_price=invoice.unit_price,
            discount_percentage=discount_percentage,
            discount_amount=discount_amount,
            tax_percentage=tax_percentage,
            tax_amount=tax_amount,
            subtotal=subtotal,
            taxable_amount=taxable_amount,
            total_amount=total_amount,
        )

    