from abc import ABC,abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class RepositoryInterface(ABC):
    @abstractmethod
    async def create(self , db : AsyncSession, invoice_data):
        pass

    @abstractmethod
    async def get_all(self , db : AsyncSession , limit : int, offset : int):
        pass

    @abstractmethod
    async def get_by_id(self , db : AsyncSession , invoice_id : int):
        pass

    @abstractmethod
    async def get_by_invoice_number(self , db : AsyncSession , invoice_number : str):
        pass

    @abstractmethod
    async def update(self , db : AsyncSession , invoice , invoice_data):
        pass

    @abstractmethod
    async def delete(self , db : AsyncSession , invoice):
        pass

    @abstractmethod
    async def save_file_record(
        self ,
        db : AsyncSession ,
        invoice_id : int , 
        filename : str ,
        file_type : str , 
        filepath : str
        ):

        pass

    @abstractmethod
    async def customer_summary(self , total : int , db : AsyncSession):
        pass

    @abstractmethod
    async def get_invoices_with_warranty(self , db : AsyncSession):
        pass

    @abstractmethod
    async def get_invoices_without_warranty(self , db : AsyncSession):
        pass

    @abstractmethod
    async def get_repeat_customers(self, db: AsyncSession):
        pass
