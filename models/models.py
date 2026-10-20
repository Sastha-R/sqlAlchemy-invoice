from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Integer, Numeric, String , ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship

from database.base import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    invoice_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    customer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    customer_email: Mapped[str] = mapped_column(String(150), nullable=False)
    invoice_date: Mapped[date] = mapped_column(Date, nullable=False)
    product_name: Mapped[str] = mapped_column(String(150), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    discount_percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    tax_percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    taxable_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    files: Mapped[list["InvoiceFile"]] = relationship(back_populates="invoice")





class InvoiceFile(Base):
    __tablename__ = "invoice_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    invoice_id : Mapped[int] = mapped_column(ForeignKey("invoices.id", ondelete="CASCADE"),nullable=False)
    file_name : Mapped[str] = mapped_column(String(255), nullable=False)
    file_type : Mapped[str] = mapped_column(String(50), nullable=False)
    file_path : Mapped[str] = mapped_column(String(500), nullable=False)
    uploaded_date : Mapped[date] =  mapped_column(Date, nullable=False)  #need to apply alembic migration
    invoice: Mapped["Invoice"] = relationship(back_populates="files")