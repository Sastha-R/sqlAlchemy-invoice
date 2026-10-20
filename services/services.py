from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions.custom_exceptions import InvoiceAlreadyExistsError, InvoiceNotFoundError
from repository.repository import InvoiceRepository
from schemas.schemas import InvoiceCreate, InvoiceData, InvoicePatch
from utilities.file_handler import (FileHandler,WARRANTY_FOLDER)




class InvoiceService:
    def __init__(self) -> None:
        self.repository = InvoiceRepository()
        self.filehandler = FileHandler()

    async def create_invoice(self, db: AsyncSession, invoice: InvoiceCreate):
        existing_invoice = await self.repository.get_by_invoice_number(db, invoice.invoice_number)
        if existing_invoice:
            raise InvoiceAlreadyExistsError("Invoice number already exists")

        invoice_data = self.build_invoice_data(invoice)
        return await self.repository.create(db, invoice_data)

    async def get_invoices(self, db: AsyncSession, limit: int, offset: int):
        return await self.repository.get_all(db, limit, offset)

    async def get_invoice_by_id(self, db: AsyncSession, invoice_id: int):
        invoice = await self.repository.get_by_id(db, invoice_id)
        if invoice is None:
            raise InvoiceNotFoundError("Invoice not found")
        return invoice

    async def update_invoice(self, db: AsyncSession, invoice_id: int, invoice: InvoiceCreate):

        existing_invoice = await self.get_invoice_by_id(db, invoice_id)
        await self.check_invoice_number_available(db, invoice.invoice_number, invoice_id)
        invoice_data =  self.build_invoice_data(invoice)
        return await self.repository.update(db, existing_invoice, invoice_data)



    async def patch_invoice(self, db: AsyncSession, invoice_id: int, invoice: InvoicePatch):
        existing_invoice = await self.get_invoice_by_id(db, invoice_id)   
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

        await self.check_invoice_number_available(db, updated_data["invoice_number"], invoice_id)

        invoice_create = InvoiceCreate(**updated_data)
        invoice_data =  self.build_invoice_data(invoice_create)
        return await self.repository.update(db, existing_invoice, invoice_data)

    async def delete_invoice(self, db: AsyncSession, invoice_id: int):
        invoice = await self.get_invoice_by_id(db, invoice_id)
        await self.repository.delete(db, invoice)

    async def check_invoice_number_available(self, db: AsyncSession, invoice_number: str, current_invoice_id: int):
        invoice = await self.repository.get_by_invoice_number(db, invoice_number)
        if invoice and invoice.id != current_invoice_id:
            raise InvoiceAlreadyExistsError("Invoice number already exists")

    def build_invoice_data(self, invoice: InvoiceCreate):
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

    async def upload_warranty_proof(self,db: AsyncSession,invoice_id: int,photo):

        existing_invoice = await self.repository.get_by_id(db, invoice_id)
        if not existing_invoice:
            raise InvoiceNotFoundError("Invoice not found")

        extensions = [".pdf"]

        file_name, file_path = await self.filehandler.save_file(photo,WARRANTY_FOLDER,extensions)

        await self.repository.save_file_record(db=db,invoice_id=invoice_id,file_name=file_name,file_type="warranty_document",file_path=file_path)
        return {
            "message": "Warranty file saved successfully",
            "invoice_id": invoice_id,
            "photo": file_name
        }


        