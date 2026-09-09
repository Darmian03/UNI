<?php
// Страница: Импорт на проект и функционалности от текстов/CSV файл

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

// Помощна функция за trim + htmlspecialchars (за показване в HTML)
function clean($value): string
{
	$value = (string)$value;
	$value = trim($value);
	return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
}

// Позволени стойности
$allowedLayers = ['client', 'routing', 'business', 'database', 'install_test'];
$allowedStatuses = ['not_started', 'in_progress', 'done'];

$statusLabels = [
	'not_started' => 'Не е започната',
	'in_progress' => 'В процес',
	'done' => 'Завършена',
];

$errors = [];
$successMessage = '';

// Полета от формата (ако файлът няма PROJECT ред)
$formProjectName = '';
$formProjectDescription = '';

// --------------
// Формат на файла (прост и учебен)
// --------------
// 1) Коментари: редове, които започват с # се игнорират.
// 2) Първият важен ред за проекта може да е:
//    PROJECT;Име на проект;Описание (по избор)
// 3) Редове за изисквания:
//    REQ;КОД;РОДИТЕЛ_КОД;type;Заглавие;Описание;layer;priority;importance;assigned_to;status;indicators
//    - КОД: уникален идентификатор в рамките на файла (пример: F1, F2, A10)
//    - РОДИТЕЛ_КОД: празно за корен; иначе трябва да сочи към вече дефиниран КОД (родителят трябва да е по-горе във файла)
//    - type: functional или nonfunctional (по избор, default functional)
//    - layer: client/routing/business/database/install_test (по избор, default business)
//    - priority и importance: 1..5 (по избор, default 3)
//    - assigned_to: username (по избор, може да е празно)
//    - status: not_started/in_progress/done (по избор, default not_started)
//    - indicators: name|description|unit|value || name|description|unit|value (само за nonfunctional)
// 4) Разделител: използвайте ; (точка и запетая). За CSV с , също работи, ако редовете са валиден CSV.

// Детектор за разделител (много опростено)
function detectDelimiter(string $line): string
{
	if (substr_count($line, ';') >= 2) {
		return ';';
	}
	if (substr_count($line, ',') >= 2) {
		return ',';
	}
	if (substr_count($line, "\t") >= 2) {
		return "\t";
	}
	return ';';
}

function isCommentOrEmpty(string $line): bool
{
	$trim = trim($line);
	return $trim === '' || substr($trim, 0, 1) === '#';
}

function stripBom(string $line): string
{
	if (str_starts_with($line, "\xEF\xBB\xBF")) {
		return substr($line, 3);
	}
	return $line;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	$formProjectName = clean($_POST['project_name'] ?? '');
	$formProjectDescription = clean($_POST['project_description'] ?? '');

	if (!isset($_FILES['file']) || !is_array($_FILES['file'])) {
		$errors[] = 'Моля, изберете файл за импорт.';
	} else {
		$fileErr = (int)($_FILES['file']['error'] ?? UPLOAD_ERR_NO_FILE);
		if ($fileErr !== UPLOAD_ERR_OK) {
			$errors[] = 'Грешка при качване на файла.';
		} else {
			$tmpName = (string)($_FILES['file']['tmp_name'] ?? '');
			$originalName = (string)($_FILES['file']['name'] ?? '');

			$ext = strtolower(pathinfo($originalName, PATHINFO_EXTENSION));
			$allowedExt = ['txt', 'csv'];
			if (!in_array($ext, $allowedExt, true)) {
				$errors[] = 'Позволени са само .txt или .csv файлове.';
			}

			if (empty($errors)) {
				$lines = @file($tmpName, FILE_IGNORE_NEW_LINES);
				if ($lines === false || empty($lines)) {
					$errors[] = 'Файлът е празен или не може да бъде прочетен.';
				}
			}

			if (empty($errors)) {
				try {
					$stmtCurrentUser = $conn->prepare('SELECT id FROM users WHERE id = :id');
					$stmtCurrentUser->execute([':id' => $createdBy]);
					if (!$stmtCurrentUser->fetch()) {
						$errors[] = 'Сесията е невалидна. Моля, влезте отново, за да импортирате проект.';
					}
				} catch (PDOException $e) {
					$errors[] = 'Възникна грешка при проверка на потребителя.';
				}
			}

			if (empty($errors)) {
				$delimiter = detectDelimiter((string)($lines[0] ?? ''));

				$projectName = '';
				$projectDescription = '';
				$projectId = 0;

				// Съответствие код -> id (за parent_id)
				$codeToId = [];

				// Индексиране за грешки
				$lineNumber = 0;

				// Първо търсим PROJECT ред (ако има)
				foreach ($lines as $idx => $rawLine) {
					$lineNumber = $idx + 1;
					$rawLine = stripBom($rawLine);
					if (isCommentOrEmpty($rawLine)) {
						continue;
					}

					$del = detectDelimiter($rawLine);
					$parts = str_getcsv($rawLine, $del);
					$first = strtoupper(trim((string)($parts[0] ?? '')));

					if ($first === 'PROJECT') {
						$projectName = trim((string)($parts[1] ?? ''));
						$projectDescription = trim((string)($parts[2] ?? ''));
						break;
					}
				}

				// Ако са попълнени полетата във формата, те имат приоритет
				$formNameRaw = html_entity_decode($formProjectName, ENT_QUOTES, 'UTF-8');
				$formDescRaw = html_entity_decode($formProjectDescription, ENT_QUOTES, 'UTF-8');
				if (trim($formNameRaw) !== '') {
					$projectName = $formNameRaw;
					$projectDescription = $formDescRaw;
				} elseif ($projectName === '') {
					$projectName = $formNameRaw;
					$projectDescription = $formDescRaw;
				}

				if (trim($projectName) === '') {
					$errors[] = 'Липсва име на проект. Добавете PROJECT ред във файла или попълнете полето „Име на проект“.';
				}

				// Създаваме проекта
				if (empty($errors)) {
					try {
						$stmtCreateProject = $conn->prepare('INSERT INTO projects (name, description, created_by) VALUES (:name, :description, :created_by)');
						$stmtCreateProject->execute([
							':name' => $projectName,
							':description' => $projectDescription !== '' ? $projectDescription : null,
							':created_by' => $createdBy,
						]);
						$projectId = (int)$conn->lastInsertId();
					} catch (PDOException $e) {
						$errors[] = 'Възникна грешка при създаване на проекта.';
					}
				}

				// Импорт на функционалности
				if (empty($errors) && $projectId > 0) {
					try {
						$stmtUserExists = $conn->prepare('SELECT id FROM users WHERE username = :username');

						foreach ($lines as $idx => $rawLine) {
							$lineNumber = $idx + 1;
							$rawLine = stripBom($rawLine);
							if (isCommentOrEmpty($rawLine)) {
								continue;
							}

							$del = detectDelimiter($rawLine);
							$parts = str_getcsv($rawLine, $del);
							$first = strtoupper(trim((string)($parts[0] ?? '')));

							// Пропускаме PROJECT реда
							if ($first === 'PROJECT') {
								continue;
							}

							// Позволяваме и header ред (например: code,parent_code,title,...)
							if ($first === 'CODE' || $first === 'REQ_ID' || $first === 'ID') {
								continue;
							}

							if ($first !== 'REQ') {
								$errors[] = 'Невалиден ред на линия ' . $lineNumber . '. Очаквам "REQ;...".';
								break;
							}

							// Нов формат: REQ;CODE;PARENT_CODE;TYPE;TITLE;DESCRIPTION;LAYER;PRIORITY;IMPORTANCE;ASSIGNED_TO;STATUS;INDICATORS
							$code = trim((string)($parts[1] ?? ''));
							$parentCode = trim((string)($parts[2] ?? ''));
							$type = trim((string)($parts[3] ?? ''));
							$title = trim((string)($parts[4] ?? ''));
							$description = trim((string)($parts[5] ?? ''));
							$layer = trim((string)($parts[6] ?? ''));
							$priority = trim((string)($parts[7] ?? ''));
							$importance = trim((string)($parts[8] ?? ''));
							$assignedTo = trim((string)($parts[9] ?? ''));
							$status = trim((string)($parts[10] ?? ''));
							$indicatorsRaw = trim((string)($parts[11] ?? ''));

							if ($type === '') {
								$type = 'functional';
							}
							$type = strtolower($type);
							if (!in_array($type, ['functional', 'nonfunctional'], true)) {
								$errors[] = 'Невалиден тип на линия ' . $lineNumber . ' (functional/nonfunctional).';
								break;
							}

							if ($code === '') {
								$errors[] = 'Липсва КОД на линия ' . $lineNumber . '.';
								break;
							}

							if (isset($codeToId[$code])) {
								$errors[] = 'Дублиран КОД "' . $code . '" на линия ' . $lineNumber . '.';
								break;
							}

							if ($title === '') {
								$errors[] = 'Липсва заглавие на линия ' . $lineNumber . '.';
								break;
							}

							if ($description === '') {
								$errors[] = 'Липсва описание на линия ' . $lineNumber . '.';
								break;
							}

							if ($layer === '') {
								$layer = 'business';
							}
							if (!in_array($layer, $allowedLayers, true)) {
								$errors[] = 'Невалиден слой на линия ' . $lineNumber . '.';
								break;
							}

							$priorityInt = $priority !== '' ? (int)$priority : 3;
							$importanceInt = $importance !== '' ? (int)$importance : 3;
							if ($priorityInt < 1 || $priorityInt > 5) {
								$errors[] = 'Невалиден приоритет на линия ' . $lineNumber . ' (1-5).';
								break;
							}
							if ($importanceInt < 1 || $importanceInt > 5) {
								$errors[] = 'Невалидна важност на линия ' . $lineNumber . ' (1-5).';
								break;
							}

							if ($status === '') {
								$status = 'not_started';
							}
							if (!in_array($status, $allowedStatuses, true)) {
								$errors[] = 'Невалиден статус на линия ' . $lineNumber . '.';
								break;
							}

							// Валидация на assigned_to
							$assignedToOrNull = null;
							if ($assignedTo !== '') {
								$stmtUserExists->execute([':username' => $assignedTo]);
								if (!$stmtUserExists->fetch()) {
									$errors[] = 'Потребителят във „assigned_to“ не съществува (линия ' . $lineNumber . ').';
									break;
								}
								$assignedToOrNull = $assignedTo;
							}

							// Родител (по избор) - родителят трябва да е по-горе във файла
							$parentIdOrNull = null;
							if ($parentCode !== '') {
								if ($parentCode === $code) {
									$errors[] = 'Невалиден parent_code на линия ' . $lineNumber . ' (не може да е равен на кода).';
									break;
								}
								if (!isset($codeToId[$parentCode])) {
									$errors[] = 'Родителят (parent_code=' . $parentCode . ') не е дефиниран преди детето (линия ' . $lineNumber . ').';
									break;
								}
								$parentIdOrNull = (int)$codeToId[$parentCode];
							}

							// Insert
							$stmtInsertReq = $conn->prepare("INSERT INTO requirements
								(project_id, parent_id, title, description, type, status, priority, importance, layer, assigned_to, image_path, created_by)
								VALUES
								(:project_id, :parent_id, :title, :description, :type, :status, :priority, :importance, :layer, :assigned_to, NULL, :created_by)");
							$stmtInsertReq->execute([
								':project_id' => $projectId,
								':parent_id' => $parentIdOrNull,
								':title' => $title,
								':description' => $description,
								':type' => $type,
								':status' => $status,
								':priority' => $priorityInt,
								':importance' => $importanceInt,
								':layer' => $layer,
								':assigned_to' => $assignedToOrNull,
								':created_by' => $createdBy,
							]);

							$newId = (int)$conn->lastInsertId();
							$codeToId[$code] = $newId;

							// Индикатори (само за нефункционални)
							if ($type === 'nonfunctional' && $indicatorsRaw !== '') {
								$indicatorChunks = explode('||', $indicatorsRaw);
								$stmtInsertInd = $conn->prepare('INSERT INTO indicators (requirement_id, name, description, unit, value) VALUES (:rid, :name, :description, :unit, :value)');
								foreach ($indicatorChunks as $chunk) {
									$chunk = trim($chunk);
									if ($chunk === '') {
										continue;
									}
									$partsInd = explode('|', $chunk);
									$name = trim((string)($partsInd[0] ?? ''));
									$desc = trim((string)($partsInd[1] ?? ''));
									$unit = trim((string)($partsInd[2] ?? ''));
									$value = trim((string)($partsInd[3] ?? ''));

									if ($name === '' || $desc === '') {
										$errors[] = 'Невалиден индикатор на линия ' . $lineNumber . ' (име и описание са задължителни).';
										break;
									}

									$stmtInsertInd->execute([
										':rid' => $newId,
										':name' => $name,
										':description' => $desc,
										':unit' => $unit !== '' ? $unit : null,
										':value' => $value !== '' ? $value : null,
									]);
								}

								if (!empty($errors)) {
									break;
								}
							}
						}
					} catch (PDOException $e) {
						$errors[] = 'Възникна грешка при импорт на изискванията (линия ' . $lineNumber . ').';
					}
				}

				// Ако има грешки след създаване на проекта, чистим проекта (каскадно трие и функционалностите)
				if (!empty($errors) && $projectId > 0) {
					try {
						$stmtDelProject = $conn->prepare('DELETE FROM projects WHERE id = :id');
						$stmtDelProject->execute([':id' => $projectId]);
					} catch (PDOException $e) {
						// Ако изтриването се провали, просто показваме грешка (без да продължаваме импорта)
					}
				}

				if (empty($errors)) {
					$successMessage = 'Импортът приключи успешно. Създаден е проект и ' . count($codeToId) . ' функционалности.';
					// Изчистваме формата
					$formProjectName = '';
					$formProjectDescription = '';
				}
			}
		}
	}
}

require_once __DIR__ . '/header.php';
require_once __DIR__ . '/menu.php';
?>

<main class="content">
	<h2>Импорт</h2>

	<section class="card">
		<h3>Формат на файла</h3>
		<p>Файлът може да е <strong>.txt</strong> или <strong>.csv</strong>. Използвайте <strong>;</strong> като разделител (препоръчително).</p>
		<p><strong>Проект (по избор във файла):</strong></p>
		<pre>PROJECT;Име на проект;Описание (по избор)</pre>
		<p><strong>Изисквания (по една на ред):</strong></p>
		<pre>REQ;КОД;РОДИТЕЛ_КОД;type;Заглавие;Описание;layer;priority;importance;assigned_to;status;indicators</pre>
		<ul>
			<li><strong>КОД</strong> трябва да е уникален във файла (пример: F1, F2, A10).</li>
			<li><strong>РОДИТЕЛ_КОД</strong> е по избор. Ако е попълнен, родителят трябва да е дефиниран по-горе във файла.</li>
			<li><strong>type</strong>: functional или nonfunctional (по избор, default functional).</li>
			<li><strong>layer</strong>: client/routing/business/database/install_test (по избор, default business).</li>
			<li><strong>priority</strong> и <strong>importance</strong>: 1..5 (по избор, default 3).</li>
			<li><strong>assigned_to</strong>: username (по избор, може да е празно).</li>
			<li><strong>status</strong>: not_started/in_progress/done (по избор, default not_started).</li>
			<li><strong>indicators</strong>: name|description|unit|value || name|description|unit|value (само за nonfunctional).</li>
		</ul>
		<p>Коментари: редове, които започват с <strong>#</strong>, се игнорират.</p>
	</section>

	<?php if ($successMessage !== ''): ?>
		<p class="text-success"><?php echo clean($successMessage); ?></p>
	<?php endif; ?>

	<?php if (!empty($errors)): ?>
		<ul class="text-error">
			<?php foreach ($errors as $err): ?>
				<li><?php echo clean($err); ?></li>
			<?php endforeach; ?>
		</ul>
	<?php endif; ?>

	<section class="card">
		<h3>Качи файл за импорт</h3>
		<form method="post" action="import.php" enctype="multipart/form-data">
			<p><strong>Ако файлът няма PROJECT ред, попълнете тук:</strong></p>

			<label for="project_name">Име на проект</label><br>
			<input type="text" id="project_name" name="project_name" value="<?php echo $formProjectName; ?>">
			<br><br>

			<label for="project_description">Описание на проект</label><br>
			<textarea id="project_description" name="project_description"><?php echo $formProjectDescription; ?></textarea>
			<br><br>

			<label for="file">Файл (.txt или .csv)</label><br>
			<input type="file" id="file" name="file" accept=".txt,.csv,text/plain,text/csv" required>
			<br><br>

			<button type="submit">Импортирай</button>
		</form>
	</section>
</main>

</div>
</body>
</html>
