SELECT maker, speed
FROM product JOIN laptop ON product.model = laptop.model
WHERE hd > 9;

(SELECT product.model, price
 FROM product JOIN pc ON product.model = pc.model
 WHERE maker = 'B')
UNION
(SELECT product.model, price
 FROM product JOIN laptop ON product.model = laptop.model
 WHERE maker = 'B')
UNION
(SELECT product.model, price
 FROM product JOIN printer ON product.model = printer.model
 WHERE maker = 'B')
ORDER BY price DESC;

SELECT DISTINCT pc1.hd
FROM pc pc1 JOIN pc pc2 ON pc1.hd = pc2.hd AND pc1.code <> pc2.code;

SELECT DISTINCT pc1.model, pc1.model
FROM pc pc1 JOIN pc pc2 ON pc1.speed = pc2.speed and pc1.ram = pc2.ram
WHERE pc1.model < pc2.model;

SELECT DISTINCT p1.maker
FROM product p1 JOIN pc pc1 ON p1.model = pc1.model
JOIN product p2 ON p1.model = p2.maker JOIN PC pc2 ON p2.model = pc2.model
WHERE pc1.speed >= 500 AND pc2.speed >= 500 AND pc1.model <> pc2.model;