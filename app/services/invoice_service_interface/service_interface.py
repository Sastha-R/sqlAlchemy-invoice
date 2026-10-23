from abc import ABC,abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import InvoiceCreate

class ServiceInterface(ABC):
    @abstractmethod
    async def create_invoice(self, db: AsyncSession, invoice: InvoiceCreate):
        pass
     
    @abstractmethod
    async def get_invoices(self, db: AsyncSession, limit: int, offset: int):
        pass   

    @abstractmethod 
    async def get_invoice_by_id(self, db: AsyncSession, invoice_id: int):
        pass

    @abstractmethod
    async def update_invoice(self, db: AsyncSession, invoice_id: int, invoice: InvoiceCreate):
        pass
    
    @abstractmethod
    async def patch_invoice(self, db: AsyncSession, invoice_id: int, invoice: InvoicePatch):
        pass

    @abstractmethod
    async def delete_invoice(self, db: AsyncSession, invoice_id: int):
        pass

    @abstractmethod
    async def check_invoice_number_available(self, db: AsyncSession, invoice_number: str, current_invoice_id: int):
        pass

    @abstractmethod
    async def build_invoice_data(self, invoice: InvoiceCreate):
        pass


    @abstractmethod
    async def upload_warranty_document(self,db: AsyncSession,invoice_id: int,photo):
        pass
       
    