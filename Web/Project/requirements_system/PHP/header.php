<?php
// Общ header за страниците (заглавие + информация за потребителя)

$username = '';
if (session_status() === PHP_SESSION_ACTIVE && isset($_SESSION['username'])) {
	$username = (string)$_SESSION['username'];
}

$safeUsername = htmlspecialchars($username, ENT_QUOTES, 'UTF-8');
?>

<!doctype html>
<html lang="bg">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>Система за управление на изисквания</title>
		<link rel="stylesheet" href="../Assets/style.css">
	</head>
	<body>
		<header class="app-header">
			<h1 class="app-title">Система за управление на изисквания</h1>

			<div class="app-header__user">
				<?php if ($safeUsername !== ''): ?>
					<span class="user-info">Влезли сте като: <strong><?php echo $safeUsername; ?></strong></span>
					<a class="logout-link" href="logout.php">Изход</a>
				<?php else: ?>
					<span class="user-info">Не сте влезли в системата</span>
				<?php endif; ?>
			</div>
		</header>

		<!-- Контейнер за ляво меню + съдържание -->
		<div class="layout">

