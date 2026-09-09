<?php
// Страница: Редакция на проект

session_start();

// Проверка дали потребителят е влязъл
if (!isset($_SESSION['user_id']) || !isset($_SESSION['username'])) {
	header('Location: index.php');
	exit;
}

require_once __DIR__ . '/../classes/Database.php';

$database = new Database();
$conn = $database->getConnection();

// Помощна функция за trim
function clean_text($value): string
{
	$value = (string)$value;
	return trim($value);
}

$projectId = isset($_GET['id']) ? (int)$_GET['id'] : 0;
if ($projectId <= 0) {
	header('Location: projects.php');
	exit;
}

$errorMessage = '';
$successMessage = '';

// Зареждаме проекта
$project = null;
try {
	$stmt = $conn->prepare('SELECT id, name, description FROM projects WHERE id = :id');
	$stmt->execute([':id' => $projectId]);
	$project = $stmt->fetch();
} catch (PDOException $e) {
	$project = null;
}

if ($project === false || $project === null) {
	$errorMessage = 'Проектът не е намерен.';
}

$name = $project ? (string)$project['name'] : '';
$description = $project ? (string)($project['description'] ?? '') : '';

// Запис на редакция
if ($_SERVER['REQUEST_METHOD'] === 'POST' && $project && $errorMessage === '') {
	$name = clean_text($_POST['name'] ?? '');
	$description = clean_text($_POST['description'] ?? '');

	if ($name === '') {
		$errorMessage = 'Името на проекта е задължително.';
	} else {
		try {
			$sql = 'UPDATE projects SET name = :name, description = :description WHERE id = :id';
			$stmt = $conn->prepare($sql);
			$stmt->execute([
				':name' => $name,
				':description' => ($description !== '' ? $description : null),
				':id' => $projectId,
			]);

			$successMessage = 'Промените са записани.';
		} catch (PDOException $e) {
			$errorMessage = 'Възникна грешка при запис.';
		}
	}
}

require_once __DIR__ . '/header.php';
require_once __DIR__ . '/menu.php';
?>

<main class="content">
	<h2>Редакция на проект</h2>

	<?php if ($errorMessage !== ''): ?>
		<p class="text-error"><?php echo htmlspecialchars($errorMessage, ENT_QUOTES, 'UTF-8'); ?></p>
	<?php endif; ?>

	<?php if ($successMessage !== ''): ?>
		<p class="text-success"><?php echo htmlspecialchars($successMessage, ENT_QUOTES, 'UTF-8'); ?></p>
	<?php endif; ?>

	<?php if ($project && $errorMessage === ''): ?>
		<section class="card">
			<form method="post" action="edit_project.php?id=<?php echo (int)$projectId; ?>">
				<label for="name">Име (задължително)</label><br>
				<input type="text" id="name" name="name" value="<?php echo htmlspecialchars($name, ENT_QUOTES, 'UTF-8'); ?>" required><br><br>

				<label for="description">Описание (по избор)</label><br>
				<textarea id="description" name="description"><?php echo htmlspecialchars($description, ENT_QUOTES, 'UTF-8'); ?></textarea><br><br>

				<button type="submit">Запази</button>
				<a class="btn" href="projects.php">Назад</a>
			</form>
		</section>
	<?php else: ?>
		<p><a class="btn" href="projects.php">Към проектите</a></p>
	<?php endif; ?>

</main>

</div>
</body>
</html>
