SELECT product.maker, product.model, product.type
FROM product LEFT JOIN pc ON product.model = pc.model
			 LEFT JOIN laptop ON product.model = laptop.model
			 LEFT JOIN printer ON product.model = printer.model
WHERE pc.code IS NULL AND laptop.code IS NULL AND printer.code IS NULL;