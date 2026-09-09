<?php
// Табло (dashboard) - показва основна статистика

session_start();

// Проверка дали потребителят е влязъл
if (!isset($_SESSION['user_id']) || !isset($_SESSION['username'])) {
	// Ако не е влязъл, връщаме към страницата за вход
	header('Location: index.php');
	exit;
}

$username = (string)$_SESSION['username'];
$safeUsername = htmlspecialchars($username, ENT_QUOTES, 'UTF-8');

require_once __DIR__ . '/../classes/Database.php';

$database = new Database();
$conn = $database->getConnection();

// Статистики
$totalProjects = 0;
$totalFunctional = 0;
$myFunctional = 0;
$statsError = '';

try {
	// 1) Общ брой проекти
	$stmtProjects = $conn->prepare('SELECT COUNT(*) AS cnt FROM projects');
	$stmtProjects->execute();
	$totalProjects = (int)($stmtProjects->fetch()['cnt'] ?? 0);

	// 2) Общ брой функционалности (функционални изисквания)
	// По изискване: броим и нефункционалните.
	$stmtFunctional = $conn->prepare("SELECT COUNT(*) AS cnt FROM requirements");
	$stmtFunctional->execute();
	$totalFunctional = (int)($stmtFunctional->fetch()['cnt'] ?? 0);

	// 3) Мои функционалности (assigned_to = текущия потребител)
	// По изискване: броим и нефункционалните.
	$stmtMy = $conn->prepare("SELECT COUNT(*) AS cnt FROM requirements WHERE assigned_to = :assigned_to");
	$stmtMy->execute([':assigned_to' => $username]);
	$myFunctional = (int)($stmtMy->fetch()['cnt'] ?? 0);
} catch (PDOException $e) {
	$statsError = 'Възникна грешка при зареждане на статистиката.';
}

// Включваме общия header и менюто.
require_once __DIR__ . '/header.php';
require_once __DIR__ . '/menu.php';
?>


<main class="content">
	<h2>Табло</h2>
	<p>Добре дошли, <strong><?php echo $safeUsername; ?></strong>!</p>

	<?php if ($statsError !== ''): ?>
		<p class="text-error"><?php echo htmlspecialchars($statsError, ENT_QUOTES, 'UTF-8'); ?></p>
	<?php endif; ?>

	<section class="card">
		<h3>Общ брой проекти</h3>
		<p><strong><?php echo (int)$totalProjects; ?></strong></p>
	</section>

	<section class="card">
		<h3>Общ брой функционалности</h3>
		<p><strong><?php echo (int)$totalFunctional; ?></strong></p>
	</section>

	<section class="card">
		<h3>Мои функционалности</h3>
		<p><strong><?php echo (int)$myFunctional; ?></strong></p>
	</section>

</main>

</div>
</body>
</html>

