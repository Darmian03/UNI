SELECT AVG(speed) as speed
FROM pc;

SELECT product.maker, AVG(laptop.screen) as screen
FROM product LEFT JOIN laptop ON product.model = laptop.model
GROUP BY product.maker;

SELECT AVG(speed) as speed
FROM laptop
WHERE price > 1000;

SELECT AVG(pc.price) as price
FROM product JOIN pc ON product.model = pc.model
WHERE product.maker = 'A';

SELECT AVG(p.price) as price
FROM ( SELECT pc.price
	   FROM pc JOIN product ON pc.model = product.model
	   WHERE maker = 'B'
	   UNION
	   SELECT laptop.price
	   FROM laptop JOIN product ON laptop.model = product.model
	   WHERE maker = 'B' ) p;

SELECT speed, AVG(price) as price
FROM pc
GROUP BY speed;

SELECT maker
FROM product
WHERE type = 'PC'
GROUP BY maker
HAVING COUNT(*) >= 3;

SELECT maker
FROM product JOIN pc ON product.model = pc.model
WHERE pc.price >= ( SELECT MAX(price)
					FROM pc );

SELECT AVG(price) as price
FROM pc
WHERE speed > 800;

SELECT AVG(pc.hd) as hd
FROM product JOIN pc ON product.model = pc.model
WHERE product.maker IN ( SELECT maker
						 FROM product
						 WHERE type = 'Printer' );

SELECT screen, MAX(price) - MIN(price) as price
FROM laptop
GROUP BY screen;

SELECT model, MAX(price) as price
FROM pc
GROUP BY model
ORDER BY price DESC;