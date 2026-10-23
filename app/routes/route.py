from fastapi import APIRouter, Depends, status,UploadFile,File
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.schemas.schemas import InvoiceCreate, InvoicePatch,InvoiceFileResponse,InvoiceResponse
from app.dependency import get_invoice_service
invoice_router = APIRouter(prefix="/invoices", tags=["Invoices"])


@invoice_router.post("/",status_code=status.HTTP_201_CREATED )
async def create_invoice(invoice: InvoiceCreate, 
                         db: AsyncSession = Depends(get_db) , 
                         invoice_service = Depends(get_invoice_service)
                         ):
    return await invoice_service.create_invoice(db , invoice)


@invoice_router.get("" , response_model = list[InvoiceResponse])
async def get_invoices(limit: int = 10,
                       offset: int = 0,
                       db: AsyncSession = Depends(get_db) ,
                       invoice_service = Depends(get_invoice_service)
                       ):
    return await invoice_service.get_invoices(db , limit , offset)



@invoice_router.get("/{invoice_id}" )
async def get_invoice(invoice_id: int, 
                      db: AsyncSession = Depends(get_db) ,
                      invoice_service = Depends(get_invoice_service)
                      ):
    return await invoice_service.get_invoice_by_id(db, invoice_id)


@invoice_router.put("/{invoice_id}")
async def update_invoice(
    invoice_id: int,
     invoice: InvoiceCreate,db: AsyncSession = Depends(get_db) , invoice_service = Depends(get_invoice_service)):
    return await invoice_service.update_invoice(db , invoice_id , invoice)


@invoice_router.patch("/{invoice_id}")
async def patch_invoice(
    invoice_id: int,
    invoice: InvoicePatch,db: AsyncSession = Depends(get_db) , 
    invoice_service = Depends(get_invoice_service)
    ):
    return await invoice_service.patch_invoice(db , invoice_id , invoice)


@invoice_router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invoice(
    invoice_id: int,
    db: AsyncSession = Depends(get_db) , 
    invoice_service = Depends(get_invoice_service)
    ):
    await invoice_service.delete_invoice(db , invoice_id)


@invoice_router.post("/{invoice_id}/warranty-document" )
async def upload_warranty_document(
    invoice_id: int,
    photo: UploadFile = File(...),
    db: AsyncSession = Depends(get_db) , 
    invoice_service = Depends(get_invoice_service)
    ):
    return await invoice_service.upload_warranty_document(db , invoice_id , photo)


