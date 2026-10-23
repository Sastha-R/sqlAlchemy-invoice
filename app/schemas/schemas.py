from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class InvoiceCreate(BaseModel):
    invoice_number: str = Field(min_length=1)
    customer_name: str = Field(min_length=1)
    customer_email: EmailStr
    invoice_date: date
    product_name: str = Field(min_length=1)
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(gt=0)


class InvoiceData(InvoiceCreate):
    
    discount_percentage: Decimal = Field(ge=0, le=100)
    discount_amount: Decimal = Field(ge=0)
    tax_percentage: Decimal = Field(ge=0, le=100)
    tax_amount: Decimal = Field(ge=0)
    subtotal: Decimal = Field(ge=0)
    taxable_amount: Decimal = Field(ge=0)
    total_amount: Decimal = Field(ge=0)


class InvoicePatch(BaseModel):
    invoice_number: str | None = Field(default=None, min_length=1)
    customer_name: str | None = Field(default=None, min_length=1)
    customer_email: EmailStr | None = None
    invoice_date: date | None = None
    product_name: str | None = Field(default=None, min_length=1)
    quantity: int | None = Field(default=None, gt=0)
    unit_price: Decimal | None = Field(default=None, gt=0)



class InvoiceFileResponse(BaseModel):
    id: int
    invoice_id: int
    file_name: str
    file_type: str
    file_path: str
    uploaded_date: date | None

    model_config = ConfigDict(from_attributes=True)


class InvoiceResponse(BaseModel):
    id: int
    invoice_number: str
    customer_name: str
    customer_email: str
    invoice_date: date
    product_name: str
    quantity: int
    unit_price: Decimal
    discount_percentage: Decimal
    discount_amount: Decimal
    tax_percentage: Decimal
    tax_amount: Decimal
    subtotal: Decimal
    taxable_amount: Decimal
    total_amount: Decimal
    files: list[InvoiceFileResponse]

    model_config = ConfigDict(from_attributes=True)

class CustomerSummaryResponse(BaseModel):
    customer_name: str
    total_amount: Decimal
    no_of_invoices: int
    no_of_invoice_files: int

class RepeatCustomerResponse(BaseModel):
    customer_name: str
    invoice_count: int