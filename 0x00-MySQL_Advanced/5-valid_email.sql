-- 5-valid_email.sql
-- Task 5: Email validation to sent

-- Create trigger to reset valid_email attribute only when the email has been changed
DELIMITER //
CREATE TRIGGER reset_valid_email BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email != OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END;
//
DELIMITER ;

