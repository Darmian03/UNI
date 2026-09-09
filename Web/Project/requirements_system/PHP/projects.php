<?php
// Страница: Управление на проекти

session_start();

// Проверка дали потребителят е влязъл
if (!isset($_SESSION['user_id']) || !isset($_SESSION['username'])) {
	header('Location: index.php');
	exit;
}

require_once __DIR__ . '/../classes/Database.php';

$database = new Database();
$conn = $database->getConnection();

$createdBy = (int)$_SESSION['user_id'];

// Помощна функция за trim
function clean_text($value): string
{
	$value = (string)$value;
	return trim($value);
}

$message = '';
$messageType = ''; // success / error

// Добавяне на проект
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'create') {
	$name = clean_text($_POST['name'] ?? '');
	$description = clean_text($_POST['description'] ?? '');

	if ($name === '') {
		$message = 'Името на проекта е задължително.';
		$messageType = 'error';
	} else {
		try {
			$sql = 'INSERT INTO projects (name, description, created_by) VALUES (:name, :description, :created_by)';
			$stmt = $conn->prepare($sql);
			$stmt->execute([
				':name' => $name,
				':description' => ($description !== '' ? $description : null),
				':created_by' => $createdBy,
			]);

			$message = 'Проектът е създаден успешно.';
			$messageType = 'success';
		} catch (PDOException $e) {
			$message = 'Възникна грешка при създаване на проекта.';
			$messageType = 'error';
		}
	}
}

// Изтриване на проект (с потвърждение)
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'delete') {
	$projectId = isset($_POST['project_id']) ? (int)$_POST['project_id'] : 0;
	$confirm = isset($_POST['confirm']) ? (string)$_POST['confirm'] : '';

	if ($projectId <= 0) {
		$message = 'Невалиден проект.';
		$messageType = 'error';
	} elseif ($confirm !== 'yes') {
		$message = 'Изтриването е отказано.';
		$messageType = 'error';
	} else {
		try {
			$sql = 'DELETE FROM projects WHERE id = :id';
			$stmt = $conn->prepare($sql);
			$stmt->execute([':id' => $projectId]);

			$message = 'Проектът е изтрит.';
			$messageType = 'success';
		} catch (PDOException $e) {
			$message = 'Възникна грешка при изтриване на проекта.';
			$messageType = 'error';
		}
	}
}

// Данни за потвърждение (GET)
$deleteProject = null;
$deleteId = isset($_GET['delete_id']) ? (int)$_GET['delete_id'] : 0;
if ($deleteId > 0) {
	try {
		$stmt = $conn->prepare('SELECT id, name FROM projects WHERE id = :id');
		$stmt->execute([':id' => $deleteId]);
		$deleteProject = $stmt->fetch();
	} catch (PDOException $e) {
		$deleteProject = null;
	}
}

// Зареждане на проекти
$projects = [];
$errorMessage = '';

try {
	$sql = 'SELECT id, name, description, created_at FROM projects ORDER BY id DESC';
	$stmt = $conn->prepare($sql);
	$stmt->execute();
	$projects = $stmt->fetchAll();
} catch (PDOException $e) {
	$errorMessage = 'Възникна грешка при зареждане на проектите.';
}

require_once __DIR__ . '/header.php';
require_once __DIR__ . '/menu.php';
?>

<main class="content">
	<h2>Проекти</h2>

	<?php if ($message !== ''): ?>
		<p class="<?php echo $messageType === 'error' ? 'text-error' : 'text-success'; ?>">
			<?php echo htmlspecialchars($message, ENT_QUOTES, 'UTF-8'); ?>
		</p>
	<?php endif; ?>

	<?php if ($errorMessage !== ''): ?>
		<p class="text-error"><?php echo htmlspecialchars($errorMessage, ENT_QUOTES, 'UTF-8'); ?></p>
	<?php endif; ?>

	<section class="card">
		<h3>Нов проект</h3>
		<form method="post" action="projects.php">
			<input type="hidden" name="action" value="create">

			<label for="name">Име (задължително)</label><br>
			<input type="text" id="name" name="name" value="" required><br><br>

			<label for="description">Описание (по избор)</label><br>
			<textarea id="description" name="description"></textarea><br><br>

			<button type="submit">Създай</button>
		</form>
	</section>

	<?php if ($deleteProject !== null): ?>
		<section class="card">
			<h3>Потвърждение за изтриване</h3>
			<p>
				Сигурни ли сте, че искате да изтриете проект
				<strong><?php echo htmlspecialchars((string)$deleteProject['name'], ENT_QUOTES, 'UTF-8'); ?></strong>?
			</p>
			<p>
				Забележка: При изтриване ще се изтрият и всички свързани функционалности.
			</p>

			<form method="post" action="projects.php" style="margin-top: 12px;">
				<input type="hidden" name="action" value="delete">
				<input type="hidden" name="project_id" value="<?php echo (int)$deleteProject['id']; ?>">
				<input type="hidden" name="confirm" value="yes">
				<button type="submit">Да, изтрий</button>
				<a class="btn" href="projects.php">Отказ</a>
			</form>
		</section>
	<?php endif; ?>

	<section class="card">
		<h3>Списък с проекти</h3>

		<?php if (empty($projects) && $errorMessage === ''): ?>
			<p>Няма създадени проекти.</p>
		<?php else: ?>
			<table>
				<thead>
					<tr>
						<th>Име</th>
						<th>Описание</th>
						<th>Създаден на</th>
						<th>Действия</th>
					</tr>
				</thead>
				<tbody>
					<?php foreach ($projects as $p): ?>
						<tr>
							<td><?php echo htmlspecialchars((string)$p['name'], ENT_QUOTES, 'UTF-8'); ?></td>
							<td><?php echo htmlspecialchars((string)($p['description'] ?? ''), ENT_QUOTES, 'UTF-8'); ?></td>
							<td><?php echo htmlspecialchars((string)$p['created_at'], ENT_QUOTES, 'UTF-8'); ?></td>
							<td>
								<a class="btn" href="edit_project.php?id=<?php echo (int)$p['id']; ?>">Редакция</a>
								<a class="btn" href="projects.php?delete_id=<?php echo (int)$p['id']; ?>">Изтрий</a>
							</td>
						</tr>
					<?php endforeach; ?>
				</tbody>
			</table>
		<?php endif; ?>
	</section>

</main>

</div>
</body>
</html>
