SELECT model, speed as MHz, hd as GB
FROM pc
WHERE price < 1200;

SELECT model, price * 1.1 as EUR
FROM laptop
ORDER BY price;

SELECT model, ram, screen
FROM laptop
WHERE price > 1000;

SELECT *
FROM printer
WHERE color = 'y';

SELECT model, speed, hd
FROM pc
WHERE (cd = '12x' OR cd = '16x') AND price < 2000;

SELECT code, model, (speed + ram + 10*screen) as rating
FROM laptop
ORDER BY rating DESC, code;