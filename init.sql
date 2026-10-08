CREATE TABLE IF NOT EXISTS erp_ledger (
    po_number VARCHAR(50) PRIMARY KEY,
    vendor_name VARCHAR(100) NOT NULL,
    authorized_amount NUMERIC(12, 2) NOT NULL
);

-- Seed standard enterprise financial logs for verification benchmarks
INSERT INTO erp_ledger (po_number, vendor_name, authorized_amount)
VALUES 
    ('PO-9901', 'Acme Corp', 1500.00),
    ('PO-9902', 'Delta Labs', 420.50),
    ('PO-9903', 'Vertex Media', 8900.00)
ON CONFLICT (po_number) DO NOTHING;
