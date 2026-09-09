<?php
// Клас FunctionalRequirement (Функционално изискване)

require_once __DIR__ . '/Requirement.php';

class FunctionalRequirement extends Requirement
{
	public function save(): bool
	{
		$sql = "INSERT INTO requirements
			(project_id, parent_id, title, description, type, status, priority, importance, layer, assigned_to, image_path, created_by)
			VALUES
			(:project_id, :parent_id, :title, :description, 'functional', 'not_started', :priority, :importance, :layer, :assigned_to, :image_path, :created_by)";

		try {
			$stmt = $this->conn->prepare($sql);
			return $stmt->execute([
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
		} catch (PDOException $e) {
			return false;
		}
	}
}
