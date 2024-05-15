-- drop database if exists hacking;

-- create database hacking;
USE hacking;

CREATE TABLE Users(
	ID_USER INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    NAME VARCHAR(20) NOT NULL,
    SECOND_NAME VARCHAR(40) NOT NULL,
    NICKNAME VARCHAR(20) NOT NULL UNIQUE,
    EMAIL LONGTEXT NOT NULL,
    PASSWORD LONGTEXT NOT NULL,
    SALT VARBINARY(20) NOT NULL,
    SIGNUP_DATE DATE NOT NULL
);
CREATE TABLE Funcionalidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255)
);
INSERT INTO Funcionalidades (nombre) VALUES ('NMAP');
INSERT INTO Funcionalidades (nombre) VALUES ('GOOGLEDORKS');
INSERT INTO Funcionalidades (nombre) VALUES ('SOCIALMEDIA');
INSERT INTO Funcionalidades (nombre) VALUES ('CURL');
INSERT INTO Funcionalidades (nombre) VALUES ('GEOLOCATION');

DELIMITER //
CREATE PROCEDURE RecorrerFuncionalidades()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE func_nombre VARCHAR(255);
    DECLARE cur CURSOR FOR SELECT nombre FROM Funcionalidades;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO func_nombre;
        IF done THEN
            LEAVE read_loop;
        END IF;
         -- Crear la tabla con el nombre de la funcionalidad
        SET @sql = CONCAT('CREATE TABLE IF NOT EXISTS ', func_nombre, '_funct (
            ID_HISTORY_', func_nombre, ' INT AUTO_INCREMENT PRIMARY KEY,
            DATA LONGTEXT,
            RESULT_', func_nombre, ' LONGTEXT,
            EXECUTE_DATE DATETIME,
            USER_ID INT,
            FOREIGN KEY (USER_ID) REFERENCES users(ID_USER)
        )');
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        SELECT func_nombre;
    END LOOP;

    CLOSE cur;
END//
DELIMITER ;

CALL RecorrerFuncionalidades();

-- drop user 'uhacking';

-- create user 'uhacking' identified by 'uhacking';

-- grant all privileges on hacking.* to uhacking;
