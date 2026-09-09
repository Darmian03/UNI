<?php
// Страница: Статус на изисквания (моите изисквания)

session_start();

// Проверка дали потребителят е влязъл
if (!isset($_SESSION['user_id']) || !isset($_SESSION['username'])) {
	header('Location: index.php');
	exit;
}

require_once __DIR__ . '/../classes/Database.php';

$database = new Database();
$conn = $database->getConnection();

$currentUsername = (string)$_SESSION['username'];

$allowedStatuses = ['not_started', 'in_progress', 'done'];
$statusLabels = [
	'not_started' => 'Не е започнато',
	'in_progress' => 'В процес',
	'done' => 'Завършено',
];

$message = '';
$messageType = ''; // success / error

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	$requirementId = isset($_POST['requirement_id']) ? (int)$_POST['requirement_id'] : 0;
	$status = isset($_POST['status']) ? trim((string)$_POST['status']) : '';

	if ($requirementId <= 0) {
		$message = 'Невалиден идентификатор на изискване.';
		$messageType = 'error';
	} elseif (!in_array($status, $allowedStatuses, true)) {
		$message = 'Невалиден статус.';
		$messageType = 'error';
	} else {
		try {
			// Обновяваме изисквания, възложени на текущия потребител (functional + nonfunctional)
			$sqlUpdate = "UPDATE requirements
				SET status = :status
				WHERE id = :id
					AND assigned_to = :assigned_to";
			$stmtUpdate = $conn->prepare($sqlUpdate);
			$stmtUpdate->execute([
				':status' => $status,
				':id' => $requirementId,
				':assigned_to' => $currentUsername,
			]);

			if ($stmtUpdate->rowCount() <= 0) {
				$message = 'Неуспешна промяна: изискването не е намерено или не е възложено на вас.';
				$messageType = 'error';
			} else {
				// Пренасочване, за да избегнем повторно изпращане при refresh
				header('Location: features.php');
				exit;
			}
		} catch (PDOException $e) {
			$message = 'Възникна грешка при промяна на статуса.';
			$messageType = 'error';
		}
	}
}

// Зареждаме изискванията, възложени на текущия потребител
$requirements = [];
$errorMessage = '';

try {
	$sql = "SELECT
			r.id,
			p.name AS project_name,
			r.type,
			r.layer,
			r.title,
			r.status
		FROM requirements r
		INNER JOIN projects p ON p.id = r.project_id
		WHERE r.assigned_to = :assigned_to
		ORDER BY p.name ASC, r.id DESC";
	$stmt = $conn->prepare($sql);
	$stmt->execute([':assigned_to' => $currentUsername]);
	$requirements = $stmt->fetchAll();
} catch (PDOException $e) {
	$errorMessage = 'Възникна грешка при зареждане на изискванията.';
}

require_once __DIR__ . '/header.php';
require_once __DIR__ . '/menu.php';
?>


<main class="content">
	<h2>Статус на моите изисквания</h2>
	<p>Потребител: <strong><?php echo htmlspecialchars($currentUsername, ENT_QUOTES, 'UTF-8'); ?></strong></p>

	<?php if ($message !== ''): ?>
		<p class="<?php echo $messageType === 'error' ? 'text-error' : 'text-success'; ?>">
			<?php echo htmlspecialchars($message, ENT_QUOTES, 'UTF-8'); ?>
		</p>
	<?php endif; ?>

	<?php if ($errorMessage !== ''): ?>
		<p class="text-error"><?php echo htmlspecialchars($errorMessage, ENT_QUOTES, 'UTF-8'); ?></p>
	<?php endif; ?>

	<?php if (empty($requirements) && $errorMessage === ''): ?>
		<p>Няма възложени изисквания за вас.</p>
	<?php else: ?>
		<table>
			<thead>
				<tr>
					<th>Проект</th>
					<th>Тип</th>
					<th>Слой</th>
					<th>Заглавие</th>
					<th>Текущ статус</th>
					<th>Нов статус</th>
					<th>Запази</th>
				</tr>
			</thead>
			<tbody>
				<?php foreach ($requirements as $row): ?>
					<tr>
						<?php $formId = 'status_form_' . (int)$row['id']; ?>
						<td><?php echo htmlspecialchars((string)($row['project_name'] ?? ''), ENT_QUOTES, 'UTF-8'); ?></td>
						<td>
							<?php
							$type = (string)($row['type'] ?? '');
							echo htmlspecialchars($type === 'nonfunctional' ? 'Нефункционално' : 'Функционално', ENT_QUOTES, 'UTF-8');
							?>
						</td>
						<td><?php echo htmlspecialchars((string)($row['layer'] ?? ''), ENT_QUOTES, 'UTF-8'); ?></td>
						<td><?php echo htmlspecialchars((string)($row['title'] ?? ''), ENT_QUOTES, 'UTF-8'); ?></td>
						<td>
							<?php
							$currentStatus = (string)($row['status'] ?? '');
							echo htmlspecialchars($statusLabels[$currentStatus] ?? $currentStatus, ENT_QUOTES, 'UTF-8');
							?>
						</td>
						<td>
							<select form="<?php echo htmlspecialchars($formId, ENT_QUOTES, 'UTF-8'); ?>" name="status" required>
								<?php foreach ($allowedStatuses as $st): ?>
									<option value="<?php echo htmlspecialchars($st, ENT_QUOTES, 'UTF-8'); ?>" <?php echo ($st === (string)$row['status']) ? 'selected' : ''; ?>>
										<?php echo htmlspecialchars($statusLabels[$st] ?? $st, ENT_QUOTES, 'UTF-8'); ?>
									</option>
								<?php endforeach; ?>
							</select>
						</td>
						<td>
							<form id="<?php echo htmlspecialchars($formId, ENT_QUOTES, 'UTF-8'); ?>" method="post" action="features.php" style="margin: 0;">
								<input type="hidden" name="requirement_id" value="<?php echo (int)$row['id']; ?>">
								<button type="submit">Запази</button>
							</form>
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
