<?php
// Абстрактен клас Requirement (Функционалност/изискване)
// Използва се като базов клас за функционални и нефункционални записи в таблица `requirements`.

require_once __DIR__ . '/Database.php';

abstract class Requirement
{
	protected PDO $conn;

	protected int $project_id;
	protected ?int $parent_id;

	protected string $title;
	protected string $description;
	protected int $priority;
	protected int $importance;
	protected string $layer;
	protected ?string $assigned_to;
	protected ?string $image_path;
	protected int $created_by;

	public function __construct(
		Database $database,
		int $project_id,
		?int $parent_id,
		string $title,
		string $description,
		int $priority,
		int $importance,
		string $layer,
		?string $assigned_to,
		?string $image_path,
		int $created_by
	) {
		$this->conn = $database->getConnection();

		$this->project_id = (int)$project_id;
		$this->parent_id = $parent_id !== null ? (int)$parent_id : null;

		$this->title = trim($title);
		$this->description = trim($description);
		$this->priority = (int)$priority;
		$this->importance = (int)$importance;
		$this->layer = trim($layer);
		$this->assigned_to = $assigned_to !== null ? trim($assigned_to) : null;
		$this->image_path = $image_path !== null ? trim($image_path) : null;
		$this->created_by = (int)$created_by;
	}

	// Записва изискването/функционалността в базата
	abstract public function save(): bool;
}
