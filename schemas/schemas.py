from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class InvoiceCreate(BaseModel):
    invoice_number: str = Field(min_length=1, max_length=50)
    customer_name: str = Field(min_length=1, max_length=100)
    customer_email: EmailStr
    invoice_date: date
    product_name: str = Field(min_length=1, max_length=150)
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)


class InvoiceData(InvoiceCreate):
    discount_percentage: Decimal = Field(ge=0, le=100, max_digits=5, decimal_places=2)
    discount_amount: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    tax_percentage: Decimal = Field(ge=0, le=100, max_digits=5, decimal_places=2)
    tax_amount: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    subtotal: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    taxable_amount: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    total_amount: Decimal = Field(ge=0, max_digits=12, decimal_places=2)


class InvoicePatch(BaseModel):
    invoice_number: str | None = Field(default=None, min_length=1, max_length=50)
    customer_name: str | None = Field(default=None, min_length=1, max_length=100)
    customer_email: EmailStr | None = None
    invoice_date: date | None = None
    product_name: str | None = Field(default=None, min_length=1, max_length=150)
    quantity: int | None = Field(default=None, gt=0)
    unit_price: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)


class InvoiceResponse(InvoiceData):
    model_config = ConfigDict(from_attributes=True)

    id: int
