<?php
// Страница: Нефункционални изисквания (с индикатори)

session_start();

// Проверка дали потребителят е влязъл
if (!isset($_SESSION['user_id']) || !isset($_SESSION['username'])) {
	header('Location: index.php');
	exit;
}

require_once __DIR__ . '/../classes/Database.php';

$database = new Database();
$conn = $database->getConnection();

// Помощни функции за визуализация
function getScoreClass(int $value): string
{
	if ($value <= 2) {
		return 'score score-green';
	}
	if ($value === 3) {
		return 'score score-orange';
	}
	return 'score score-red';
}

$statusLabels = [
	'not_started' => 'Не е започната',
	'in_progress' => 'В процес',
	'done' => 'Завършена',
];

// Вземаме само нефункционалните изисквания + име на проект
$sqlRequirements = "SELECT
		r.id,
		p.name AS project_name,
		r.title,
		r.description,
		r.layer,
		r.priority,
		r.importance,
		r.status,
		r.assigned_to,
		r.image_path
	FROM requirements r
	INNER JOIN projects p ON p.id = r.project_id
	WHERE r.type = 'nonfunctional'
	ORDER BY p.name ASC, r.id DESC";

$requirements = [];
$errorMessage = '';
$stmtIndicators = null;

try {
	$stmt = $conn->prepare($sqlRequirements);
	$stmt->execute();
	$requirements = $stmt->fetchAll();
} catch (PDOException $e) {
	$errorMessage = 'Възникна грешка при зареждане на нефункционалните изисквания.';
}

// Подготвяме заявка за индикатори (ще я използваме за всяко изискване)
$sqlIndicators = "SELECT id, name, description, unit, value
				FROM indicators
				WHERE requirement_id = :requirement_id
				ORDER BY id ASC";

try {
	$stmtIndicators = $conn->prepare($sqlIndicators);
} catch (PDOException $e) {
	$stmtIndicators = null;
}

require_once __DIR__ . '/header.php';
require_once __DIR__ . '/menu.php';
?>


<main class="content">
	<h2>Нефункционални изисквания</h2>

	<?php if ($errorMessage !== ''): ?>
		<p class="text-error"><?php echo htmlspecialchars($errorMessage, ENT_QUOTES, 'UTF-8'); ?></p>
	<?php endif; ?>

	<?php if (empty($requirements) && $errorMessage === ''): ?>
		<p>Няма добавени нефункционални изисквания.</p>
	<?php else: ?>
		<table>
			<thead>
				<tr>
					<th>Проект</th>
					<th>Заглавие</th>
					<th>Описание</th>
					<th>Слой</th>
					<th>Приоритет</th>
					<th>Важност</th>
					<th>Възложено на</th>
					<th>Статус</th>
					<th>Действия</th>
				</tr>
			</thead>
			<tbody>
				<?php foreach ($requirements as $row): ?>
					<tr>
						<td><?php echo htmlspecialchars((string)($row['project_name'] ?? ''), ENT_QUOTES, 'UTF-8'); ?></td>
						<td><?php echo htmlspecialchars((string)($row['title'] ?? ''), ENT_QUOTES, 'UTF-8'); ?></td>
						<td><?php echo htmlspecialchars((string)($row['description'] ?? ''), ENT_QUOTES, 'UTF-8'); ?></td>
						<td><?php echo htmlspecialchars((string)($row['layer'] ?? ''), ENT_QUOTES, 'UTF-8'); ?></td>
						<td><span class="<?php echo htmlspecialchars(getScoreClass((int)($row['priority'] ?? 0)), ENT_QUOTES, 'UTF-8'); ?>"><?php echo (int)($row['priority'] ?? 0); ?></span></td>
						<td><span class="<?php echo htmlspecialchars(getScoreClass((int)($row['importance'] ?? 0)), ENT_QUOTES, 'UTF-8'); ?>"><?php echo (int)($row['importance'] ?? 0); ?></span></td>
						<td><?php echo htmlspecialchars((string)($row['assigned_to'] ?? '-'), ENT_QUOTES, 'UTF-8'); ?></td>
						<td>
							<?php
							$st = (string)($row['status'] ?? '');
							echo htmlspecialchars($statusLabels[$st] ?? $st, ENT_QUOTES, 'UTF-8');
							?>
						</td>
						<td>
							<a class="btn" href="edit_requirement.php?id=<?php echo (int)$row['id']; ?>">Редакция</a>
							<?php if (!empty($row['image_path'])): ?>
								<a class="btn" href="image.php?req_id=<?php echo (int)$row['id']; ?>">Преглед на снимка</a>
							<?php else: ?>
								Няма снимка
							<?php endif; ?>
						</td>
					</tr>

					<tr>
						<td colspan="8">
							<strong>Индикатори:</strong>
							<?php
							$indicators = [];
							try {
								if ($stmtIndicators !== null) {
									$stmtIndicators->execute([':requirement_id' => (int)$row['id']]);
									$indicators = $stmtIndicators->fetchAll();
								}
							} catch (PDOException $e) {
								$indicators = [];
							}
							?>

							<?php if (empty($indicators)): ?>
								<p>Няма дефинирани индикатори</p>
							<?php else: ?>
								<table>
									<thead>
										<tr>
											<th>Име</th>
											<th>Описание</th>
											<th>Единица</th>
											<th>Стойност</th>
										</tr>
									</thead>
									<tbody>
										<?php foreach ($indicators as $ind): ?>
											<tr>
												<td><?php echo htmlspecialchars((string)$ind['name'], ENT_QUOTES, 'UTF-8'); ?></td>
												<td><?php echo htmlspecialchars((string)$ind['description'], ENT_QUOTES, 'UTF-8'); ?></td>
												<td><?php echo htmlspecialchars((string)($ind['unit'] ?? ''), ENT_QUOTES, 'UTF-8'); ?></td>
												<td><?php echo htmlspecialchars((string)($ind['value'] ?? ''), ENT_QUOTES, 'UTF-8'); ?></td>
											</tr>
										<?php endforeach; ?>
									</tbody>
								</table>
							<?php endif; ?>
						</td>
					</tr>

					<tr class="nf-separator">
						<td colspan="8"></td>
					</tr>

				<?php endforeach; ?>
			</tbody>
		</table>
	<?php endif; ?>

</main>

</div>
</body>
</html>
