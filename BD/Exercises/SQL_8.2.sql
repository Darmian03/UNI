begin transaction;

INSERT INTO product
VALUES ('C', '1100', 'PC');
INSERT INTO pc
VALUES (12, '1100', 2400, 2048, 500, '52x', 399);

DELETE FROM pc
WHERE model = '1100';
DELETE FROM product
WHERE model = '1100';

INSERT INTO product (model, maker, type)
SELECT DISTINCT model, 'Z', 'Laptop' 
FROM pc;
INSERT INTO laptop
SELECT DISTINCT code+100, model, speed, ram, hd, price+500, 15 
FROM pc;

DELETE FROM laptop
WHERE model IN ( SELECT model
				 FROM product
				 WHERE maker NOT IN ( SELECT maker
									  FROM product JOIN printer ON product.model = printer.model ) );
DELETE FROM product
WHERE maker NOT IN ( SELECT maker
					 FROM product JOIN printer ON product.model = printer.model );

UPDATE product
SET maker = 'A'
WHERE maker = 'B';

UPDATE pc
SET price = price/2, hd = hd+20;

UPDATE laptop
SET screen = screen+1
WHERE model IN ( SELECT model
				 FROM product
				 WHERE maker = 'B' );

rollback transaction;