<?php

require_once __DIR__ . '/../classes/Database.php';
require_once __DIR__ . '/../classes/Users.php';

$message = '';

$username = '';
$password = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	// Вземаме данните от формата
	$username = isset($_POST['username']) ? trim((string)$_POST['username']) : '';
	$password = isset($_POST['password']) ? trim((string)$_POST['password']) : '';

	// Базова валидация
	if ($username === '' || $password === '') {
		$message = 'Моля, попълнете потребителско име и парола.';
	} elseif (mb_strlen($username) < 3 || mb_strlen($password) < 4) {
		$message = 'Невалидни данни за вход.';
	} else {
		// Проверка на входните данни през класа User
		$database = new Database();
		$user = new User($database);

		if ($user->login($username, $password)) {
			// Стартираме сесия и записваме данните на потребителя
			session_start();
			$_SESSION['user_id'] = $user->id;
			$_SESSION['username'] = $user->username;

			// Пренасочване към табло
			header('Location: dashboard.php');
			exit;
		} else {
			$message = $user->error !== '' ? $user->error : 'Грешно потребителско име или парола.';
		}
	}
}

// За безопасно показване в HTML
$safeUsername = htmlspecialchars($username, ENT_QUOTES, 'UTF-8');
?>

<!doctype html>
<html lang="bg">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>Вход в системата</title>
		<link rel="stylesheet" href="../Assets/style.css">
	</head>
	<body class="auth-page">
		<main class="auth-card">
			<h1>Вход в системата</h1>

		<?php if ($message !== ''): ?>
			<p class="text-error">
				<?php echo htmlspecialchars($message, ENT_QUOTES, 'UTF-8'); ?>
			</p>
		<?php endif; ?>

		<form method="post" action="index.php">
			<label for="username">Потребителско име</label><br>
			<input type="text" id="username" name="username" value="<?php echo $safeUsername; ?>" required><br><br>

			<label for="password">Парола</label><br>
			<input type="password" id="password" name="password" value="" required><br><br>

			<button type="submit">Вход</button>
		</form>

		<div class="auth-actions">
			<p>
				Нямате профил? <a href="register.php">Регистрация</a>
			</p>
		</div>
		</main>
	</body>
</html>

