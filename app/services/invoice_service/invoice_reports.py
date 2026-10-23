from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.invoice_repository_interface.invoice_repository_interface import RepositoryInterface
from app.services.invoice_service_interface.invoice_reports_interface import ReportsInterface

class InvoiceReports(ReportsInterface):

    def __init__(self , repository : RepositoryInterface):
         self.repository = repository
         
     
    async def get_customer_summary(self, total : float , db: AsyncSession):
            return await self.repository.customer_summary(total , db)
    
    async def get_invoices_without_warranty(self, db: AsyncSession):
        return await self.repository.get_invoices_without_warranty(db)
    
    async def get_repeat_customers(self, db: AsyncSession):
        return await self.repository.get_repeat_customers(db)
    
    async def get_invoices_with_warranty(self, db: AsyncSession):
        return await self.repository.get_invoices_with_warranty(db)
