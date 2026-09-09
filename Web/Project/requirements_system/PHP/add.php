<?php
// Страница за добавяне на изискване

session_start();

// Проверка дали потребителят е влязъл
if (!isset($_SESSION['user_id']) || !isset($_SESSION['username'])) {
	header('Location: index.php');
	exit;
}

require_once __DIR__ . '/../classes/Database.php';
require_once __DIR__ . '/../classes/FunctionalRequirement.php';
require_once __DIR__ . '/../classes/NonFunctionalRequirement.php';
require_once __DIR__ . '/../classes/Indicator.php';

$createdBy = (int) $_SESSION['user_id'];

$databaseForLists = new Database();
$conn = $databaseForLists->getConnection();

// Зареждаме проектите за падащото меню
$projects = [];
try {
	$stmtProjects = $conn->prepare('SELECT id, name FROM projects ORDER BY id DESC');
	$stmtProjects->execute();
	$projects = $stmtProjects->fetchAll();
} catch (PDOException $e) {
	$projects = [];
}

// Родителските функционалности ще се зареждат според избрания проект (без JavaScript).
$parentOptions = [];

// Списъци с позволени стойности
$allowedLayers = ['client', 'routing', 'business', 'database', 'install_test'];
$allowedTypes = ['functional', 'nonfunctional'];

// Състояние за формата
$errors = [];
$successMessage = '';

$title = '';
$description = '';
$priority = '3';
$importance = '3';
$layer = 'business';
$assigned_to = '';
$type = 'functional';

$project_id = '';
$parent_id = '';

$imagePath = null;

$selectedProjectName = '';

// Ако има избран проект през GET, го използваме за зареждане на родители
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['project_id'])) {
	$project_id = clean($_GET['project_id']);
}

// Опитваме се да намерим името на избрания проект (за показване във формата)
$selectedProjectIdInt = (int)$project_id;
if ($selectedProjectIdInt > 0) {
	try {
		$stmtProjName = $conn->prepare('SELECT name FROM projects WHERE id = :id');
		$stmtProjName->execute([':id' => $selectedProjectIdInt]);
		$projRow = $stmtProjName->fetch();
		if ($projRow && isset($projRow['name'])) {
			$selectedProjectName = (string)$projRow['name'];
		}
	} catch (PDOException $e) {
		$selectedProjectName = '';
	}
}

// Зареждаме родителски функционалности (само ако има избран проект)
$projectIdForParents = (int)$project_id;
if ($projectIdForParents > 0) {
	try {
		$stmtParents = $conn->prepare("SELECT id, title FROM requirements WHERE project_id = :project_id AND type = 'functional' ORDER BY id DESC");
		$stmtParents->execute([':project_id' => $projectIdForParents]);
		$parentOptions = $stmtParents->fetchAll();
	} catch (PDOException $e) {
		$parentOptions = [];
	}
}

// Индикатори (до 3)
$indicatorsData = [
	['name' => '', 'description' => '', 'unit' => '', 'value' => ''],
	['name' => '', 'description' => '', 'unit' => '', 'value' => ''],
	['name' => '', 'description' => '', 'unit' => '', 'value' => ''],
];

// Помощна функция за trim + htmlspecialchars
function clean($value): string
{
	$value = (string) $value;
	$value = trim($value);
	return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	// Вземаме и чистим данните от формата
	$title = clean($_POST['title'] ?? '');
	$description = clean($_POST['description'] ?? '');
	$priority = clean($_POST['priority'] ?? '');
	$importance = clean($_POST['importance'] ?? '');
	$layer = clean($_POST['layer'] ?? '');
	$assigned_to = clean($_POST['assigned_to'] ?? '');
	$type = clean($_POST['type'] ?? 'functional');
	$project_id = clean($_POST['project_id'] ?? '');
	$parent_id = clean($_POST['parent_id'] ?? '');

	// При POST може да се е сменил проектът => презареждаме родителските опции за правилна валидация/показване
	$parentOptions = [];
	$projectIdForParents = (int)$project_id;
	if ($projectIdForParents > 0) {
		try {
			$stmtParents = $conn->prepare("SELECT id, title FROM requirements WHERE project_id = :project_id AND type = 'functional' ORDER BY id DESC");
			$stmtParents->execute([':project_id' => $projectIdForParents]);
			$parentOptions = $stmtParents->fetchAll();
		} catch (PDOException $e) {
			$parentOptions = [];
		}
	}

	// Индикатори има САМО при нефункционални изисквания.
	// Ако типът е функционален, игнорираме всички индикатор полета.
	if ($type === 'nonfunctional') {
		// Индикатори (до 3)
		for ($i = 1; $i <= 3; $i++) {
			$indicatorsData[$i - 1]['name'] = clean($_POST['indicator_name_' . $i] ?? '');
			$indicatorsData[$i - 1]['description'] = clean($_POST['indicator_description_' . $i] ?? '');
			$indicatorsData[$i - 1]['unit'] = clean($_POST['indicator_unit_' . $i] ?? '');
			$indicatorsData[$i - 1]['value'] = clean($_POST['indicator_value_' . $i] ?? '');
		}
	} else {
		// Нулираме индикаторите, за да няма объркване във формата
		$indicatorsData = [
			['name' => '', 'description' => '', 'unit' => '', 'value' => ''],
			['name' => '', 'description' => '', 'unit' => '', 'value' => ''],
			['name' => '', 'description' => '', 'unit' => '', 'value' => ''],
		];
	}

	// Валидация
	if ($title === '') {
		$errors[] = 'Заглавието е задължително.';
	}
	if ($description === '') {
		$errors[] = 'Описанието е задължително.';
	}

	$projectIdInt = (int)$project_id;
	if ($projectIdInt <= 0) {
		$errors[] = 'Моля, изберете проект.';
	} elseif (empty($projects)) {
		$errors[] = 'Няма налични проекти. Първо създайте проект.';
	} else {
		try {
			$stmtProject = $conn->prepare('SELECT id FROM projects WHERE id = :id');
			$stmtProject->execute([':id' => $projectIdInt]);
			$projectRow = $stmtProject->fetch();
			if (!$projectRow) {
				$errors[] = 'Избраният проект не съществува.';
			}
		} catch (PDOException $e) {
			$errors[] = 'Възникна грешка при проверка на проекта.';
		}
	}

	$parentIdInt = (int)$parent_id;
	if ($parent_id === '' || $parentIdInt <= 0) {
		$parentIdInt = 0;
	}

	// Валидация на parent_id (ако е избран): да съществува и да е в същия проект
	// По изискване: ако има избран родител, слой НЕ се избира - наследяваме слоя от родителя.
	if ($parentIdInt > 0 && $projectIdInt > 0) {
		try {
			$stmtParent = $conn->prepare("SELECT id, layer FROM requirements WHERE id = :id AND project_id = :project_id AND type = 'functional'");
			$stmtParent->execute([
				':id' => $parentIdInt,
				':project_id' => $projectIdInt,
			]);
			$parentRow = $stmtParent->fetch();
			if (!$parentRow) {
				$errors[] = 'Избраната родителска функционалност не съществува или не е в същия проект.';
			} else {
				$parentLayer = (string)($parentRow['layer'] ?? '');
				if ($parentLayer !== '') {
					$layer = $parentLayer;
				}
			}
		} catch (PDOException $e) {
			$errors[] = 'Възникна грешка при проверка на родителската функционалност.';
		}
	}

	if (!in_array($layer, $allowedLayers, true)) {
		$errors[] = 'Моля, изберете валиден слой.';
	}
	if (!in_array($type, $allowedTypes, true)) {
		$errors[] = 'Моля, изберете валиден тип изискване.';
	}

	$priorityInt = (int) $priority;
	$importanceInt = (int) $importance;
	if ($priorityInt < 1 || $priorityInt > 5) {
		$errors[] = 'Приоритетът трябва да е число от 1 до 5.';
	}
	if ($importanceInt < 1 || $importanceInt > 5) {
		$errors[] = 'Важността трябва да е число от 1 до 5.';
	}

	// assigned_to: ако е попълнено, потребителят трябва да съществува
	if ($assigned_to !== '') {
		try {
			$stmtUser = $conn->prepare('SELECT id FROM users WHERE username = :username');
			$stmtUser->execute([':username' => $assigned_to]);
			$userRow = $stmtUser->fetch();
			if (!$userRow) {
				$errors[] = 'Потребителят във „Възложено на“ не съществува.';
			}
		} catch (PDOException $e) {
			$errors[] = 'Възникна грешка при проверка на потребителя.';
		}
	}

	// Качване на снимка (по избор)
	// - позволени: jpg, jpeg, png
	// - максимален размер: ~2MB
	if (isset($_FILES['image']) && isset($_FILES['image']['error']) && $_FILES['image']['error'] !== UPLOAD_ERR_NO_FILE) {
		$fileError = (int)$_FILES['image']['error'];
		if ($fileError !== UPLOAD_ERR_OK) {
			$errors[] = 'Възникна грешка при качване на снимката.';
		} else {
			$fileSize = (int)$_FILES['image']['size'];
			if ($fileSize > 2 * 1024 * 1024) {
				$errors[] = 'Снимката е твърде голяма (максимум 2MB).';
			} else {
				$originalName = (string)($_FILES['image']['name'] ?? '');
				$ext = strtolower(pathinfo($originalName, PATHINFO_EXTENSION));
				$allowedExt = ['jpg', 'jpeg', 'png'];
				if (!in_array($ext, $allowedExt, true)) {
					$errors[] = 'Позволени формати за снимка: JPG, JPEG, PNG.';
				} else {
					$tmpName = (string)($_FILES['image']['tmp_name'] ?? '');
					$imgInfo = @getimagesize($tmpName);
					if ($imgInfo === false) {
						$errors[] = 'Каченият файл не е валидна снимка.';
					} else {
						$uploadDir = __DIR__ . '/../uploads';
						if (!is_dir($uploadDir)) {
							@mkdir($uploadDir, 0777, true);
						}

						$filename = 'img_' . date('Ymd_His') . '_' . bin2hex(random_bytes(8)) . '.' . $ext;
						$targetPath = $uploadDir . '/' . $filename;
						$relativePath = 'uploads/' . $filename;

						if (!@move_uploaded_file($tmpName, $targetPath)) {
							$errors[] = 'Неуспешно записване на снимката.';
						} else {
							$imagePath = $relativePath;
						}
					}
				}
			}
		}
	}

	// Ако имаме валидно качена снимка, но след това има други грешки,
	// чистим файла, за да не остават излишни снимки.
	if (!empty($errors) && $imagePath !== null) {
		$fullPath = __DIR__ . '/../' . $imagePath;
		if (is_file($fullPath)) {
			@unlink($fullPath);
		}
		$imagePath = null;
	}

	// Индикатори (само при нефункционално изискване):
	// - до 3 броя
	// - name и description са задължителни
	// - unit и value са по избор
	$indicatorObjects = [];
	if ($type === 'nonfunctional') {
		foreach ($indicatorsData as $idx => $row) {
			$hasAny = ($row['name'] !== '' || $row['description'] !== '' || $row['unit'] !== '' || $row['value'] !== '');
			if (!$hasAny) {
				continue;
			}

			// Име и описание са задължителни
			if ($row['name'] === '' || $row['description'] === '') {
				$errors[] = 'Индикатор ' . ($idx + 1) . ': Име и описание са задължителни.';
				continue;
			}

			$unit = $row['unit'] !== '' ? $row['unit'] : null;
			$value = $row['value'] !== '' ? $row['value'] : null;
			$indicatorObjects[] = new Indicator($row['name'], $row['description'], $unit, $value);
		}
	}

	// Запис в базата (ако няма грешки)
	if (empty($errors)) {
		$database = new Database();
		$parentIdOrNull = $parentIdInt > 0 ? $parentIdInt : null;
		$assignedToOrNull = $assigned_to !== '' ? $assigned_to : null;
		$imagePathOrNull = $imagePath !== null && $imagePath !== '' ? $imagePath : null;

		if ($type === 'functional') {
			$req = new FunctionalRequirement(
				$database,
				$projectIdInt,
				$parentIdOrNull,
				$title,
				$description,
				$priorityInt,
				$importanceInt,
				$layer,
				$assignedToOrNull,
				$imagePathOrNull,
				$createdBy
			);
		} else {
			// NonFunctionalRequirement::save() записва първо изискването,
			// после записва индикаторите в таблица `indicators` с requirement_id.
			$req = new NonFunctionalRequirement(
				$database,
				$projectIdInt,
				$parentIdOrNull,
				$title,
				$description,
				$priorityInt,
				$importanceInt,
				$layer,
				$assignedToOrNull,
				$imagePathOrNull,
				$createdBy,
				$indicatorObjects
			);
		}

		if ($req->save()) {
			$successMessage = 'Изискването е добавено успешно.';

			// Изчистваме полетата след успех
			$title = '';
			$description = '';
			$priority = '3';
			$importance = '3';
			$layer = 'business';
			$assigned_to = '';
			$type = 'functional';
			$project_id = '';
			$parent_id = '';
			$imagePath = null;
			$indicatorsData = [
				['name' => '', 'description' => '', 'unit' => '', 'value' => ''],
				['name' => '', 'description' => '', 'unit' => '', 'value' => ''],
				['name' => '', 'description' => '', 'unit' => '', 'value' => ''],
			];
		} else {
			$errors[] = 'Възникна грешка при запис в базата данни.';

			// Ако има качена снимка, но записът е неуспешен, чистим файла
			if ($imagePath !== null) {
				$fullPath = __DIR__ . '/' . $imagePath;
				if (is_file($fullPath)) {
					@unlink($fullPath);
				}
			}
		}
	}
}

require_once __DIR__ . '/header.php';
require_once __DIR__ . '/menu.php';
?>


<main class="content">
	<h2>Добавяне на изискване</h2>

	<?php if ($successMessage !== ''): ?>
		<p class="text-success"><?php echo htmlspecialchars($successMessage, ENT_QUOTES, 'UTF-8'); ?></p>
	<?php endif; ?>

	<?php if (!empty($errors)): ?>
		<div class="card">
			<h3>Грешки</h3>
			<ul>
				<?php foreach ($errors as $err): ?>
					<li class="text-error"><?php echo htmlspecialchars($err, ENT_QUOTES, 'UTF-8'); ?></li>
				<?php endforeach; ?>
			</ul>
		</div>
	<?php endif; ?>

	<section class="card">
		<h3>Избор на проект</h3>
		<form method="get" action="add.php">
			<label for="project_id">Проект</label><br>
			<select id="project_id" name="project_id" required>
				<option value="">-- Изберете проект --</option>
				<?php foreach ($projects as $p): ?>
					<option value="<?php echo (int)$p['id']; ?>" <?php echo ((string)$project_id === (string)$p['id']) ? 'selected' : ''; ?>>
						<?php echo htmlspecialchars((string)$p['name'], ENT_QUOTES, 'UTF-8'); ?>
					</option>
				<?php endforeach; ?>
			</select>
			<br><br>
			<button type="submit">Избери</button>
		</form>
	</section>

	<?php if ((int)$project_id <= 0): ?>
		<p><em>Изберете проект, за да добавите функционалност/изискване.</em></p>
	<?php else: ?>
		<section class="card">
			<h3>Нова функционалност / изискване</h3>
			<p>
				Проект: <strong><?php echo htmlspecialchars($selectedProjectName !== '' ? $selectedProjectName : ('ID ' . (int)$project_id), ENT_QUOTES, 'UTF-8'); ?></strong>
				(<a href="add.php">смени</a>)
			</p>
			<form method="post" action="add.php" enctype="multipart/form-data">
				<input type="hidden" name="project_id" value="<?php echo (int)$project_id; ?>">

			<label for="parent_id">Родителска функционалност (по избор)</label><br>
			<select id="parent_id" name="parent_id">
				<option value="">-- Няма --</option>
				<?php foreach ($parentOptions as $opt): ?>
					<option value="<?php echo (int)$opt['id']; ?>" <?php echo ((string)$parent_id === (string)$opt['id']) ? 'selected' : ''; ?>>
						<?php echo (int)$opt['id']; ?> - <?php echo htmlspecialchars((string)$opt['title'], ENT_QUOTES, 'UTF-8'); ?>
					</option>
				<?php endforeach; ?>
			</select>
			<br><br>

			<label for="title">Заглавие</label><br>
			<input type="text" id="title" name="title" value="<?php echo $title; ?>" required><br><br>

			<label for="description">Описание</label><br>
			<textarea id="description" name="description" required><?php echo $description; ?></textarea><br><br>

			<label for="priority">Приоритет</label><br>
			<select id="priority" name="priority">
				<?php for ($p = 1; $p <= 5; $p++): ?>
					<option value="<?php echo $p; ?>" <?php echo ((string) $p === (string) $priority) ? 'selected' : ''; ?>>
						<?php echo $p; ?></option>
				<?php endfor; ?>
			</select><br><br>

			<label for="importance">Важност</label><br>
			<select id="importance" name="importance">
				<?php for ($im = 1; $im <= 5; $im++): ?>
					<option value="<?php echo $im; ?>" <?php echo ((string) $im === (string) $importance) ? 'selected' : ''; ?>>
						<?php echo $im; ?></option>
				<?php endfor; ?>
			</select><br><br>


			<label for="layer">Слой</label><br>
			<?php if ((int)$parent_id > 0): ?>
				<input type="hidden" name="layer" value="<?php echo htmlspecialchars($layer, ENT_QUOTES, 'UTF-8'); ?>">
				<p><strong><?php echo htmlspecialchars($layer, ENT_QUOTES, 'UTF-8'); ?></strong> <em>(наследен от родителя)</em></p>
			<?php else: ?>
				<select id="layer" name="layer">
					<?php foreach ($allowedLayers as $l): ?>
						<option value="<?php echo htmlspecialchars($l, ENT_QUOTES, 'UTF-8'); ?>" <?php echo ($l === $layer) ? 'selected' : ''; ?>><?php echo htmlspecialchars($l, ENT_QUOTES, 'UTF-8'); ?></option>
					<?php endforeach; ?>
				</select>
			<?php endif; ?>
			<br><br>

			<label for="assigned_to">Възложено на</label><br>
			<input type="text" id="assigned_to" name="assigned_to" value="<?php echo $assigned_to; ?>"><br><br>

			<label for="image">Снимка (по избор)</label><br>
			<input type="file" id="image" name="image" accept=".jpg,.jpeg,.png">
			<p><em>Позволени формати: JPG/JPEG/PNG, максимум 2MB.</em></p>
			<br>

			<p><strong>Тип изискване</strong></p>
			<label>
				<input type="radio" name="type" value="functional" <?php echo ($type === 'functional') ? 'checked' : ''; ?>>
				Функционално
			</label><br>
			<label>
				<input type="radio" name="type" value="nonfunctional" <?php echo ($type === 'nonfunctional') ? 'checked' : ''; ?>>
				Нефункционално
			</label>
			<br><br>

			<!-- Индикатори (само при тип „Нефункционално“).
				Без JavaScript: когато е избран функционален тип, секцията е скрита (свита).
			-->
			<details <?php echo ($type === 'nonfunctional') ? 'open' : ''; ?>>
				<summary><strong>Индикатори (само за нефункционални изисквания)</strong></summary>
				<p><em>Ако типът е „Функционално“, тези полета се игнорират.</em></p>
				<p>Можете да добавите до 3 индикатора. Име и описание са задължителни.</p>

				<?php for ($i = 1; $i <= 3; $i++): ?>
					<fieldset style="margin-bottom: 12px;">
						<legend>Индикатор <?php echo $i; ?></legend>

						<label for="indicator_name_<?php echo $i; ?>">Име (задължително)</label><br>
						<input type="text" id="indicator_name_<?php echo $i; ?>" name="indicator_name_<?php echo $i; ?>"
							value="<?php echo $indicatorsData[$i - 1]['name']; ?>"><br><br>

						<label for="indicator_description_<?php echo $i; ?>">Описание (задължително)</label><br>
						<textarea id="indicator_description_<?php echo $i; ?>"
							name="indicator_description_<?php echo $i; ?>"><?php echo $indicatorsData[$i - 1]['description']; ?></textarea><br><br>

						<label for="indicator_unit_<?php echo $i; ?>">Единица (по избор)</label><br>
						<input type="text" id="indicator_unit_<?php echo $i; ?>" name="indicator_unit_<?php echo $i; ?>"
							value="<?php echo $indicatorsData[$i - 1]['unit']; ?>"><br><br>

						<label for="indicator_value_<?php echo $i; ?>">Стойност (по избор)</label><br>
						<input type="text" id="indicator_value_<?php echo $i; ?>"
							name="indicator_value_<?php echo $i; ?>"
							value="<?php echo $indicatorsData[$i - 1]['value']; ?>">
					</fieldset>
				<?php endfor; ?>
			</details>

			<br>

			<button type="submit">Запази</button>
			</form>
		</section>
	<?php endif; ?>

</main>

</div>
</body>
</html>