CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
   invoice_number VARCHAR(50) UNIQUE NOT NULL,
   customer_name VARCHAR(100) NOT NULL,
    customer_email VARCHAR(150),
    invoice_date DATE NOT NULL,
    product_name VARCHAR(150) NOT NULL,
    quantity INT NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    discount_percentage NUMERIC(5, 2) DEFAULT 0,
    discount_amount NUMERIC(10, 2) DEFAULT 0,
    tax_percentage NUMERIC(5, 2) DEFAULT 0,
    tax_amount NUMERIC(10, 2) DEFAULT 0,
    subtotal NUMERIC(10, 2) NOT NULL,
    taxable_amount NUMERIC(10, 2) NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL
);