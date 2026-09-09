<?php
// Страница: Функционални изисквания

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

// Вземаме само функционални изисквания + име на проект
$sql = "SELECT
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
	WHERE r.type = 'functional'
	ORDER BY p.name ASC, r.id DESC";

$requirements = [];
$errorMessage = '';

try {
	$stmt = $conn->prepare($sql);
	$stmt->execute();
	$requirements = $stmt->fetchAll();
} catch (PDOException $e) {
	$errorMessage = 'Възникна грешка при зареждане на функционалните изисквания.';
}

require_once __DIR__ . '/header.php';
require_once __DIR__ . '/menu.php';
?>


<main class="content">
	<h2>Функционални изисквания</h2>

	<?php if ($errorMessage !== ''): ?>
		<p class="text-error"><?php echo htmlspecialchars($errorMessage, ENT_QUOTES, 'UTF-8'); ?></p>
	<?php endif; ?>

	<?php if (empty($requirements) && $errorMessage === ''): ?>
		<p>Няма добавени функционални изисквания.</p>
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
				<?php endforeach; ?>
			</tbody>
		</table>
	<?php endif; ?>

</main>

</div>
</body>
</html>
