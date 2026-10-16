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



-- PROCEDURE: public.create_invoice(character varying, character varying, character varying, date, character varying, integer, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric)

-- DROP PROCEDURE IF EXISTS public.create_invoice(character varying, character varying, character varying, date, character varying, integer, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric);

CREATE OR REPLACE PROCEDURE public.create_invoice(
	IN p_invoice_number character varying,
	IN p_customer_name character varying,
	IN p_customer_email character varying,
	IN p_invoice_date date,
	IN p_product_name character varying,
	IN p_quantity integer,
	IN p_unit_price numeric,
	IN p_discount_percentage numeric,
	IN p_discount_amount numeric,
	IN p_tax_percentage numeric,
	IN p_tax_amount numeric,
	IN p_subtotal numeric,
	IN p_taxable_amount numeric,
	IN p_total_amount numeric)
LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
IF EXISTS (SELECT 1 FROM invoices WHERE invoice_number = p_invoice_number)
THEN 
RAISE EXCEPTION 'Number already exist';
END IF; 
INSERT INTO invoices(invoice_number  ,
   customer_name,
    customer_email,
    invoice_date,
    product_name,
    quantity,
    unit_price  ,
    discount_percentage,
    discount_amount,
    tax_percentage,
    tax_amount ,
    subtotal,
    taxable_amount,
    total_amount)
	VALUES(P_invoice_number,
    P_customer_name ,
    P_customer_email ,
    P_invoice_date ,
    P_product_name ,
    P_quantity ,
    P_unit_price,
    P_discount_percentage ,
    P_discount_amount ,
    P_tax_percentage ,
    P_tax_amount,
    P_subtotal ,
    P_taxable_amount ,
    P_total_amount );
	END;
	
$BODY$;
ALTER PROCEDURE public.create_invoice(character varying, character varying, character varying, date, character varying, integer, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric)
    OWNER TO postgres;

