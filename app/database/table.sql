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


CREATE TABLE invoice_files (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER NOT NULL,
    file_name VARCHAR(200) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_path VARCHAR(500) NOT NULL,

    CONSTRAINT fk_invoice_files
        FOREIGN KEY (invoice_id)
        REFERENCES invoices(id)
        ON DELETE CASCADE
);

CREATE OR REPLACE PROCEDURE create_invoice(
     p_invoice_number VARCHAR,
     p_customer_name VARCHAR,
     p_customer_email VARCHAR,
     p_invoice_date DATE,
     p_product_name VARCHAR,
     p_quantity INTEGER,
     p_unit_price NUMERIC,
     p_discount_percentage NUMERIC,
     p_discount_amount NUMERIC,
     p_tax_percentage NUMERIC,
     p_tax_amount NUMERIC,
     p_subtotal NUMERIC,
     p_taxable_amount NUMERIC,
     p_total_amount NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
 IF EXISTS (SELECT 1
    FROM invoices
    WHERE invoice_number = p_invoice_number) 
	THEN
        RAISE EXCEPTION 'Invoice number already exists';
    END IF;
    INSERT INTO invoices (invoice_number,
        customer_name,
        customer_email,
        invoice_date,
        product_name,
        quantity,
        unit_price,
        discount_percentage,
        discount_amount,
        tax_percentage,
        tax_amount,
        subtotal,
        taxable_amount,
        total_amount)
    VALUES (
        p_invoice_number,
        p_customer_name,
        p_customer_email,
        p_invoice_date,
        p_product_name,
        p_quantity,
        p_unit_price,
        p_discount_percentage,
        p_discount_amount,
        p_tax_percentage,
        p_discount_amount,
        p_subtotal,
        p_taxable_amount,
        p_total_amount);
END;
$$;
select * from invoices
select * from invoice_files

thranish