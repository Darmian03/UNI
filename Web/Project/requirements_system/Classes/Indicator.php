<?php

/**
 * Клас Indicator (Индикатор)
 * - Използва се при нефункционални изисквания.
 * - Държи данните, които ще се запишат в таблица `indicators`.
 */
class Indicator
{
	public string $name;
	public string $description;
	public ?string $unit;
	public ?string $value;

	// Конструктор - инициализира полетата.
	public function __construct(string $name, string $description, ?string $unit = null, ?string $value = null)
	{
		$this->name = trim($name);
		$this->description = trim($description);
		$this->unit = $unit !== null ? trim($unit) : null;
		$this->value = $value !== null ? trim($value) : null;
	}
}