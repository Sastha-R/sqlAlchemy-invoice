from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Invoice
from schemas.schemas import InvoiceData
from sqlalchemy import text


class InvoiceRepository:
    async def create(self, db: AsyncSession, invoice_data: InvoiceData):
        # invoice = Invoice(**invoice_data.model_dump())
        invoice = invoice_data.model_dump()
        try:
            statement = text("""call create_invoice(
                           :invoice_number,
                            :customer_name,
                            :customer_email,
                            :invoice_date,
                            :product_name,
                            :quantity,
                            :unit_price,
                            :discount_percentage,
                            :discount_amount,
                            :tax_percentage,
                            :tax_amount,
                            :subtotal,
                            :taxable_amount,
                            :total_amount)""")
            result = await db.execute(statement , invoice)
            await db.commit()
            return invoice
        finally:
            pass
        # try:    
        #     db.add(invoice)
        #     await db.commit()
        #     await db.refresh(invoice)
        #     return invoice
        
        # except SQLAlchemyError:
        #     await db.rollback()
        #     raise

    async def get_all(self, db: AsyncSession, limit: int, offset: int):
        statement = select(Invoice).order_by(Invoice.id).limit(limit).offset(offset)
        result = await db.execute(statement)
        return list(result.scalars().all())

    async def get_by_id(self, db: AsyncSession, invoice_id: int):
        return await db.get(Invoice, invoice_id)

    async def get_by_invoice_number(self, db: AsyncSession, invoice_number: str):
        statement = select(Invoice).where(Invoice.invoice_number == invoice_number)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def update(self, db: AsyncSession, invoice: Invoice, invoice_data: InvoiceData):
        for field, value in invoice_data.model_dump().items():
            setattr(invoice, field, value)

        try:
            await db.commit()
            await db.refresh(invoice)
            return invoice

        
        except SQLAlchemyError:
            await db.rollback()
            raise

    async def delete(self, db: AsyncSession, invoice: Invoice):
        try:
            await db.delete(invoice)
            await db.commit()
        except SQLAlchemyError:
            await db.rollback()
            raise

    