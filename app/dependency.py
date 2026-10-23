from app.repository.invoice_repository.invoice_repository import InvoiceRepository
from app.services.invoice_service.services import InvoiceService
from app.services.invoice_service.invoice_reports import InvoiceReports

def get_invoice_service():
    repository = InvoiceRepository()    
    return InvoiceService(repository)

def get_invoice_reportS():
    repository = InvoiceRepository()    
    return InvoiceReports(repository)