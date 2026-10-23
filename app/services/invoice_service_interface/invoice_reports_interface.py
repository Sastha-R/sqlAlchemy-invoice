from abc import ABC,abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

class ReportsInterface(ABC):

    @abstractmethod
    async def get_customer_summary(self, total : float , db: AsyncSession):
        pass

    @abstractmethod
    async def get_invoices_without_warranty(self, db: AsyncSession):
       pass

    @abstractmethod
    async def get_repeat_customers(self, db: AsyncSession):
        pass
    
    @abstractmethod
    async def get_invoices_with_warranty(self, db: AsyncSession):
        pass