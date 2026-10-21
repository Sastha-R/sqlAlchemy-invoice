from repository.repository import InvoiceRepository
from services.services import InvoiceService

def get_invoice_service():
    repository = InvoiceRepository()    
    return InvoiceService(repository)