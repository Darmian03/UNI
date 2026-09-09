<?php
// Клас NonFunctionalRequirement (Нефункционално изискване)
// Записва изискването в `requirements` и индикаторите в `indicators`.

require_once __DIR__ . '/Requirement.php';
require_once __DIR__ . '/Indicator.php';

class NonFunctionalRequirement extends Requirement
{
	/** @var Indicator[] */
	private array $indicators;

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
		int $created_by,
		array $indicators
	) {
		parent::__construct(
			$database,
			$project_id,
			$parent_id,
			$title,
			$description,
			$priority,
			$importance,
			$layer,
			$assigned_to,
			$image_path,
			$created_by
		);

		$this->indicators = $indicators;
	}

	public function save(): bool
	{
		try {
			$this->conn->beginTransaction();

			$sqlReq = "INSERT INTO requirements
				(project_id, parent_id, title, description, type, status, priority, importance, layer, assigned_to, image_path, created_by)
				VALUES
				(:project_id, :parent_id, :title, :description, 'nonfunctional', 'not_started', :priority, :importance, :layer, :assigned_to, :image_path, :created_by)";

			$stmtReq = $this->conn->prepare($sqlReq);
			$stmtReq->execute([
				':project_id' => $this->project_id,
				':parent_id' => $this->parent_id,
				':title' => $this->title,
				':description' => $this->description,
				':priority' => $this->priority,
				':importance' => $this->importance,
				':layer' => $this->layer,
				':assigned_to' => $this->assigned_to,
				':image_path' => $this->image_path,
				':created_by' => $this->created_by,
			]);

			$requirementId = (int)$this->conn->lastInsertId();

			if (!empty($this->indicators)) {
				$sqlInd = "INSERT INTO indicators (requirement_id, name, description, unit, value)
					VALUES (:requirement_id, :name, :description, :unit, :value)";
				$stmtInd = $this->conn->prepare($sqlInd);

				foreach ($this->indicators as $ind) {
					$stmtInd->execute([
						':requirement_id' => $requirementId,
						':name' => $ind->name,
						':description' => $ind->description,
						':unit' => $ind->unit,
						':value' => $ind->value,
					]);
				}
			}

			$this->conn->commit();
			return true;
		} catch (PDOException $e) {
			if ($this->conn->inTransaction()) {
				$this->conn->rollBack();
			}
			return false;
		}
	}
}
