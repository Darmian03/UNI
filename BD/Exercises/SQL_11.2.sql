CREATE VIEW LPP
AS
	SELECT code, model, price
	FROM laptop
	UNION ALL
	SELECT code, model, price
	FROM pc
	UNION ALL
	SELECT code, model, price
	FROM printer;

GO

ALTER VIEW LPP
AS
	SELECT code, model, price, 'laptop' as type
	FROM laptop
	UNION ALL
	SELECT code, model, price, 'pc' as type
	FROM pc
	UNION ALL
	SELECT code, model, price, 'printer' as type
	FROM printer; 

GO

ALTER VIEW LPP
AS
	SELECT code, model, price, speed, 'laptop' as type
	FROM laptop
	UNION ALL
	SELECT code, model, price, speed, 'pc' as type
	FROM pc
	UNION ALL
	SELECT code, model, price, NULL, 'printer' as type
	FROM printer; 

GO

SELECT *
FROM LPP;

DROP VIEW LPP;
