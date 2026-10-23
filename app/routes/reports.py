from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.dependency import get_invoice_reportS


report_route = APIRouter(prefix = "/reports" , tags = ["Reports"])


@report_route.get("/summary")
async def get_customer_summary(total : float = 0 , db : AsyncSession = Depends(get_db) , invoice_reports = Depends(get_invoice_reportS)):
     return await invoice_reports.get_customer_summary(total , db) 

@report_route.get("/invoice-with-warranty")
async def get_invoices_with_files(db: AsyncSession = Depends(get_db),invoice_reports = Depends(get_invoice_reportS)):
    return await invoice_reports.get_invoices_with_warranty(db)

@report_route.get("/invoice-without-warranty")
async def get_invoices_without_files(db: AsyncSession = Depends(get_db),invoice_reports = Depends(get_invoice_reportS)):
    return await invoice_reports.get_invoices_without_warranty(db)

@report_route.get("/repeated-customers")
async def get_repeat_customers(db: AsyncSession = Depends(get_db), invoice_reports = Depends(get_invoice_reportS)):
    return await invoice_reports.get_repeat_customers(db)