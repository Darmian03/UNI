<?php
// Страница: Преглед на снимка към изискване

session_start();

// Проверка дали потребителят е влязъл
if (!isset($_SESSION['user_id']) || !isset($_SESSION['username'])) {
	header('Location: index.php');
	exit;
}

require_once __DIR__ . '/../classes/Database.php';

$database = new Database();
$conn = $database->getConnection();

$reqId = isset($_GET['req_id']) ? (int)$_GET['req_id'] : 0;

$imagePath = null;
$errorMessage = '';

if ($reqId <= 0) {
	$errorMessage = 'Невалиден идентификатор на изискване.';
} else {
	try {
		$stmt = $conn->prepare('SELECT id, title, image_path FROM requirements WHERE id = :id');
		$stmt->execute([':id' => $reqId]);
		$row = $stmt->fetch();

		if (!$row) {
			$errorMessage = 'Изискването не е намерено.';
		} else {
			$imagePath = isset($row['image_path']) ? (string)$row['image_path'] : '';
			if ($imagePath === '') {
				$imagePath = null;
			}
		}
	} catch (PDOException $e) {
		$errorMessage = 'Възникна грешка при зареждане на снимката.';
	}
}

// Допълнителна защита: позволяваме само снимки от папка uploads/
$publicImagePath = null;
if ($errorMessage === '' && $imagePath !== null) {
	if (str_starts_with($imagePath, 'uploads/') && !str_contains($imagePath, '..')) {
		$uploadsDir = realpath(__DIR__ . '/../uploads');
		$fullPath = realpath(__DIR__ . '/../' . $imagePath);

		if ($uploadsDir !== false && $fullPath !== false && str_starts_with($fullPath, $uploadsDir) && is_file($fullPath)) {
			$publicImagePath = '../' . $imagePath;
		} else {
			$errorMessage = 'Снимката не е намерена на сървъра.';
		}
	} else {
		$errorMessage = 'Невалиден път до снимка.';
	}
}

require_once __DIR__ . '/header.php';
require_once __DIR__ . '/menu.php';
?>

<main class="content">
	<h2>Преглед на снимка</h2>

	<?php if ($errorMessage !== ''): ?>
		<p class="text-error"><?php echo htmlspecialchars($errorMessage, ENT_QUOTES, 'UTF-8'); ?></p>
		<p><a class="btn" href="javascript:history.back()">Назад</a></p>
	<?php elseif ($publicImagePath === null): ?>
		<p>Няма снимка за това изискване.</p>
		<p><a class="btn" href="javascript:history.back()">Назад</a></p>
	<?php else: ?>
		<p>
			<a class="btn" href="javascript:history.back()">Назад</a>
		</p>
		<img class="image-preview" src="<?php echo htmlspecialchars($publicImagePath, ENT_QUOTES, 'UTF-8'); ?>" alt="Снимка към изискване">
	<?php endif; ?>
</main>

</div>
</body>
</html>
