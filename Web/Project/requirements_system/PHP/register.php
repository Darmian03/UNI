<?php
// Страница за регистрация (семпла, за учебен проект)

require_once __DIR__ . '/../classes/Database.php';
require_once __DIR__ . '/../classes/Users.php';

$message = '';
$isSuccess = false;

$username = '';
$password = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	// Вземаме данните от формата
	$username = isset($_POST['username']) ? trim((string)$_POST['username']) : '';
	$password = isset($_POST['password']) ? trim((string)$_POST['password']) : '';

	// Базова валидация (без JavaScript)
	if ($username === '' || $password === '') {
		$message = 'Моля, попълнете потребителско име и парола.';
	} elseif (mb_strlen($username) < 3) {
		$message = 'Потребителското име трябва да е поне 3 символа.';
	} elseif (mb_strlen($password) < 4) {
		$message = 'Паролата трябва да е поне 4 символа.';
	} else {
		// Създаваме обекти и опитваме регистрация
		$database = new Database();
		$user = new User($database);

		if ($user->register($username, $password)) {
			$isSuccess = true;
			$message = 'Регистрацията е успешна. Вече можете да влезете в системата.';

			// Изчистваме полетата след успешна регистрация
			$username = '';
			$password = '';
		} else {
			// Показваме грешката от класа User (на български)
			$message = $user->error !== '' ? $user->error : 'Неуспешна регистрация.';
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
		<title>Регистрация</title>
		<link rel="stylesheet" href="../Assets/style.css">
	</head>
	<body class="auth-page">
		<main class="auth-card">
			<h1>Регистрация</h1>

		<?php if ($message !== ''): ?>
			<p class="<?php echo $isSuccess ? 'text-success' : 'text-error'; ?>">
				<?php echo htmlspecialchars($message, ENT_QUOTES, 'UTF-8'); ?>
			</p>
		<?php endif; ?>

		<form method="post" action="register.php">
			<label for="username">Потребителско име</label><br>
			<input type="text" id="username" name="username" value="<?php echo $safeUsername; ?>" required><br><br>

			<label for="password">Парола</label><br>
			<input type="password" id="password" name="password" value="" required><br><br>

			<button type="submit">Регистрация</button>
		</form>

		<div class="auth-actions">
			<p>
				<a href="index.php">Към страницата за вход</a>
			</p>
		</div>
		</main>
	</body>
</html>

