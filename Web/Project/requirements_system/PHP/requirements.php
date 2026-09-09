<?php
// Страница: Всички изисквания

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

// Зареждаме проектите за филтъра
$projects = [];
try {
	$stmtProjects = $conn->prepare('SELECT id, name FROM projects ORDER BY name ASC');
	$stmtProjects->execute();
	$projects = $stmtProjects->fetchAll();
} catch (PDOException $e) {
	$projects = [];
}

// Филтри (GET) - много проста логика за учебен проект
$allowedTypes = ['all', 'functional', 'nonfunctional'];
$allowedLayers = ['all', 'client', 'routing', 'business', 'database', 'install_test'];
$allowedOrderBy = ['priority', 'importance', 'created_at'];

$filterProjectId = isset($_GET['project_id']) ? (int)$_GET['project_id'] : 0;

$filterType = isset($_GET['type']) ? trim((string)$_GET['type']) : 'all';
$filterLayer = isset($_GET['layer']) ? trim((string)$_GET['layer']) : 'all';
$filterAssignedTo = isset($_GET['assigned_to']) ? trim((string)$_GET['assigned_to']) : '';
$orderBy = isset($_GET['order_by']) ? trim((string)$_GET['order_by']) : 'created_at';

if (!in_array($filterType, $allowedTypes, true)) {
	$filterType = 'all';
}
if (!in_array($filterLayer, $allowedLayers, true)) {
	$filterLayer = 'all';
}
if (!in_array($orderBy, $allowedOrderBy, true)) {
	$orderBy = 'created_at';
}

// Подготовка на SQL заявката
// Показваме и името на проекта.
$sql = "SELECT
		r.id,
		p.name AS project_name,
		r.title,
		r.layer,
		r.priority,
		r.importance,
		r.status,
		r.assigned_to,
		r.image_path,
		r.type,
		r.created_at
	FROM requirements r
	INNER JOIN projects p ON p.id = r.project_id";

$whereParts = [];
$params = [];

if ($filterType !== 'all') {
	$whereParts[] = 'r.type = :type';
	$params[':type'] = $filterType;
}

if ($filterLayer !== 'all') {
	$whereParts[] = 'r.layer = :layer';
	$params[':layer'] = $filterLayer;
}

if ($filterProjectId > 0) {
	$whereParts[] = 'r.project_id = :project_id';
	$params[':project_id'] = $filterProjectId;
}

if ($filterAssignedTo !== '') {
	$whereParts[] = 'r.assigned_to LIKE :assigned_to';
	$params[':assigned_to'] = '%' . $filterAssignedTo . '%';
}

if (!empty($whereParts)) {
	$sql .= ' WHERE ' . implode(' AND ', $whereParts);
}

// Сортиране (само по позволени колони)
$orderBySql = 'r.created_at DESC';
if ($orderBy === 'priority') {
	$orderBySql = 'r.priority DESC';
} elseif ($orderBy === 'importance') {
	$orderBySql = 'r.importance DESC';
} elseif ($orderBy === 'created_at') {
	$orderBySql = 'r.created_at DESC';
}

$sql .= ' ORDER BY ' . $orderBySql;

$requirements = [];
$errorMessage = '';

try {
	$stmt = $conn->prepare($sql);
	$stmt->execute($params);
	$requirements = $stmt->fetchAll();
} catch (PDOException $e) {
	$errorMessage = 'Възникна грешка при зареждане на изискванията.';
}

require_once __DIR__ . '/header.php';
require_once __DIR__ . '/menu.php';
?>


<main class="content">
	<h2>Всички изисквания</h2>

	<!-- Филтри (GET) -->
	<section class="card">
		<h3>Филтри</h3>
		<form method="get" action="requirements.php">
			<label for="project_id">Проект</label><br>
			<select id="project_id" name="project_id">
				<option value="0" <?php echo ($filterProjectId === 0) ? 'selected' : ''; ?>>Всички</option>
				<?php foreach ($projects as $p): ?>
					<option value="<?php echo (int)$p['id']; ?>" <?php echo ($filterProjectId === (int)$p['id']) ? 'selected' : ''; ?>>
						<?php echo htmlspecialchars((string)$p['name'], ENT_QUOTES, 'UTF-8'); ?>
					</option>
				<?php endforeach; ?>
			</select>
			<br><br>

			<label for="type">Тип</label><br>
			<select id="type" name="type">
				<option value="all" <?php echo ($filterType === 'all') ? 'selected' : ''; ?>>Всички</option>
				<option value="functional" <?php echo ($filterType === 'functional') ? 'selected' : ''; ?>>Функционални</option>
				<option value="nonfunctional" <?php echo ($filterType === 'nonfunctional') ? 'selected' : ''; ?>>Нефункционални</option>
			</select>
			<br><br>

			<label for="layer">Слой</label><br>
			<select id="layer" name="layer">
				<option value="all" <?php echo ($filterLayer === 'all') ? 'selected' : ''; ?>>Всички</option>
				<option value="client" <?php echo ($filterLayer === 'client') ? 'selected' : ''; ?>>client</option>
				<option value="routing" <?php echo ($filterLayer === 'routing') ? 'selected' : ''; ?>>routing</option>
				<option value="business" <?php echo ($filterLayer === 'business') ? 'selected' : ''; ?>>business</option>
				<option value="database" <?php echo ($filterLayer === 'database') ? 'selected' : ''; ?>>database</option>
				<option value="install_test" <?php echo ($filterLayer === 'install_test') ? 'selected' : ''; ?>>install_test</option>
			</select>
			<br><br>

			<label for="assigned_to">Възложено на</label><br>
			<input type="text" id="assigned_to" name="assigned_to" value="<?php echo htmlspecialchars($filterAssignedTo, ENT_QUOTES, 'UTF-8'); ?>">
			<br><br>

			<label for="order_by">Сортиране по</label><br>
			<select id="order_by" name="order_by">
				<option value="priority" <?php echo ($orderBy === 'priority') ? 'selected' : ''; ?>>Приоритет</option>
				<option value="importance" <?php echo ($orderBy === 'importance') ? 'selected' : ''; ?>>Важност</option>
				<option value="created_at" <?php echo ($orderBy === 'created_at') ? 'selected' : ''; ?>>Дата на създаване</option>
			</select>
			<br><br>

			<button type="submit">Приложи</button>
			<a class="btn" href="requirements.php">Изчисти</a>
		</form>
	</section>

	<?php if ($errorMessage !== ''): ?>
		<p class="text-error"><?php echo htmlspecialchars($errorMessage, ENT_QUOTES, 'UTF-8'); ?></p>
	<?php endif; ?>

	<?php if (empty($requirements) && $errorMessage === ''): ?>
		<p>Няма добавени изисквания.</p>
	<?php else: ?>
		<table>
			<thead>
				<tr>
					<th>Проект</th>
					<th>Заглавие</th>
					<th>Тип</th>
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
						<td><?php echo ($row['type'] === 'functional') ? 'Функционално' : 'Нефункционално'; ?></td>
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
