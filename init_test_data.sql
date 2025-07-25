CREATE TABLE IF NOT EXISTS test_data (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    value INTEGER NOT NULL
);

DO $$
BEGIN
    FOR i IN 1..1000 LOOP
        INSERT INTO test_data (name, value) VALUES (CONCAT('TestName_', i), i * 10);
    END LOOP;
END $$;
