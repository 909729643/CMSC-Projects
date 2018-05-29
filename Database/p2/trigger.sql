CREATE 
	OR REPLACE FUNCTION updateStatusCount ( ) RETURNS TRIGGER AS $updateStatus$ DECLARE
	old_status_count INTEGER;
BEGIN
SELECT
	numflights INTO old_status_count 
FROM
	NumberOfFlightsTaken 
WHERE
	customerid = NumberOfFlightsTaken.customerid;
IF
	( TG_OP = 'INSERT' ) THEN
IF
	EXISTS ( SELECT customerid FROM NumberOfFlightsTaken WHERE customerid = NEW.customerid ) THEN
	UPDATE NumberOfFlightsTaken 
	SET numflights = numflights + 1 
WHERE
	customerid = NEW.customerid;
ELSE INSERT INTO NumberOfFlightsTaken
VALUES
	( NEW.customerid, ( SELECT customers.NAME FROM customers WHERE customers.customerid = NEW.customerid ), 1 );
RETURN NEW;

END IF;

ELSEIF ( TG_OP = 'DELETE' AND old_status_count = 1 ) THEN
DELETE 
FROM
	NumberOfFlightsTaken 
WHERE
	customerid = OLD.customerid;

ELSEIF ( TG_OP = 'DELETE' AND old_status_count > 1 ) THEN
UPDATE NumberOfFlightsTaken 
SET numflights = numflights - 1 
WHERE
	customerid = OLD.customerid;

END IF;
RETURN OLD;

END;
$updateStatus$ LANGUAGE plpgsql;
CREATE TRIGGER update_num_status AFTER INSERT 
OR DELETE ON flewon FOR EACH ROW
EXECUTE PROCEDURE updateStatusCount ( );
END;