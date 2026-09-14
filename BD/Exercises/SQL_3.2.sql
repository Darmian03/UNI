SELECT maker
FROM product
WHERE model IN ( SELECT model
				 FROM pc
				 WHERE speed > 500 );

SELECT model
FROM laptop
WHERE speed < ALL ( SELECT speed
					FROM pc );

SELECT DISTINCT model
FROM ( SELECT model, price
	   FROM pc
	   UNION ALL
	   SELECT model, price
	   FROM laptop
	   UNION ALL
	   SELECT model, price
	   FROM printer ) ProductPrice
WHERE price >= ALL ( SELECT price
					 FROM pc
				     UNION ALL
					 SELECT price
				     FROM laptop
				     UNION ALL
	                 SELECT price
				     FROM printer );

SELECT model
FROM product
WHERE model IN ( SELECT model
				 FROM printer
				 WHERE color = 'y' AND price <= ALL ( SELECT price
													  FROM printer
													  WHERE color = 'y' ) );

SELECT DISTINCT maker
FROM product
WHERE model IN ( SELECT model
				 FROM pc
				 WHERE ram <= ALL ( SELECT ram
									FROM pc ) AND speed >= ALL ( SELECT speed
																 FROM pc
																 WHERE ram <= ALL ( SELECT ram
																					FROM pc ) ) );
