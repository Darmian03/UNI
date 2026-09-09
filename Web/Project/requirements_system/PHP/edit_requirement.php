<?php
// Страница: Редакция / изтриване на изискване (функционално или нефункционално)

session_start();

// Проверка дали потребителят е влязъл
if (!isset($_SESSION['user_id']) || !isset($_SESSION['username'])) {
	header('Location: index.php');
	exit;
}

require_once __DIR__ . '/../classes/Database.php';

$database = new Database();
$conn = $database->getConnection();

// Помощна функция за trim + htmlspecialchars
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

// ID на изискването
$reqId = 0;
if (isset($_GET['id'])) {
	$reqId = (int)$_GET['id'];
} elseif (isset($_GET['req_id'])) {
	$reqId = (int)$_GET['req_id'];
}

$errors = [];
$successMessage = '';
$errorMessage = '';

// Зареждаме проектите за падащото меню
$projects = [];
try {
	$stmtProjects = $conn->prepare('SELECT id, name FROM projects ORDER BY name ASC');
	$stmtProjects->execute();
	$projects = $stmtProjects->fetchAll();
} catch (PDOException $e) {
	$projects = [];
}

// Зареждаме изискването (functional или nonfunctional)
$requirement = null;
$requirementType = '';
if ($reqId > 0) {
	try {
		$stmtReq = $conn->prepare("SELECT id, project_id, parent_id, title, description, layer, priority, importance, assigned_to, status, image_path, type
			FROM requirements
			WHERE id = :id AND type IN ('functional','nonfunctional')");
		$stmtReq->execute([':id' => $reqId]);
		$requirement = $stmtReq->fetch();
		$requirementType = $requirement ? (string)($requirement['type'] ?? '') : '';
	} catch (PDOException $e) {
		$requirement = null;
		$errorMessage = 'Възникна грешка при зареждане на изискването.';
	}
} else {
	$errorMessage = 'Невалиден идентификатор на изискване.';
}

if (!$requirement && $errorMessage === '') {
	$errorMessage = 'Изискването не е намерено.';
}

// Състояние за формата
$project_id = $requirement ? (string)$requirement['project_id'] : '';
$title = $requirement ? (string)$requirement['title'] : '';
$description = $requirement ? (string)$requirement['description'] : '';
$layer = $requirement ? (string)$requirement['layer'] : 'business';
$priority = $requirement ? (string)$requirement['priority'] : '3';
$importance = $requirement ? (string)$requirement['importance'] : '3';
$assigned_to = $requirement ? (string)($requirement['assigned_to'] ?? '') : '';
$status = $requirement ? (string)$requirement['status'] : 'not_started';
$parent_id = $requirement ? (string)($requirement['parent_id'] ?? '') : '';
$currentImagePath = $requirement ? (string)($requirement['image_path'] ?? '') : '';

// Индикатори (само за нефункционални изисквания)
$indicatorsData = [
	['name' => '', 'description' => '', 'unit' => '', 'value' => ''],
	['name' => '', 'description' => '', 'unit' => '', 'value' => ''],
	['name' => '', 'description' => '', 'unit' => '', 'value' => ''],
];

if ($requirement && $requirementType === 'nonfunctional') {
	try {
		$stmtInd = $conn->prepare("SELECT name, description, unit, value FROM indicators WHERE requirement_id = :rid ORDER BY id ASC");
		$stmtInd->execute([':rid' => $reqId]);
		$rows = $stmtInd->fetchAll();
		$idx = 0;
		foreach ($rows as $r) {
			if ($idx >= 3) {
				break;
			}
			$indicatorsData[$idx]['name'] = (string)($r['name'] ?? '');
			$indicatorsData[$idx]['description'] = (string)($r['description'] ?? '');
			$indicatorsData[$idx]['unit'] = (string)($r['unit'] ?? '');
			$indicatorsData[$idx]['value'] = (string)($r['value'] ?? '');
			$idx++;
		}
	} catch (PDOException $e) {
		// Оставяме празни индикатори
	}
}

// Зареждаме родителските функционалности според избрания проект
$parentOptions = [];
$projectIdForParents = (int)$project_id;
if ($projectIdForParents > 0) {
	try {
		$stmtParents = $conn->prepare("SELECT id, title
			FROM requirements
			WHERE project_id = :project_id
				AND type = 'functional'
				AND id <> :current_id
			ORDER BY id DESC");
		$stmtParents->execute([
			':project_id' => $projectIdForParents,
			':current_id' => $reqId,
		]);
		$parentOptions = $stmtParents->fetchAll();
	} catch (PDOException $e) {
		$parentOptions = [];
	}
}

// Ако има избран родител, по изискване слой НЕ се избира - наследяваме слоя от родителя
$parentLockedLayer = '';
if ($requirement && (int)$parent_id > 0 && (int)$project_id > 0) {
	try {
		$stmtPL = $conn->prepare("SELECT layer FROM requirements WHERE id = :id AND project_id = :project_id AND type = 'functional'");
		$stmtPL->execute([
			':id' => (int)$parent_id,
			':project_id' => (int)$project_id,
		]);
		$pl = $stmtPL->fetch();
		if ($pl) {
			$parentLockedLayer = (string)($pl['layer'] ?? '');
			if ($parentLockedLayer !== '') {
				$layer = $parentLockedLayer;
			}
		}
	} catch (PDOException $e) {
		$parentLockedLayer = '';
	}
}

// Потвърждение за изтриване
$confirmDelete = isset($_GET['confirm_delete']) && $_GET['confirm_delete'] === '1';

// Обработка на POST
if ($_SERVER['REQUEST_METHOD'] === 'POST' && $requirement) {
	$action = clean($_POST['action'] ?? 'update');

	if ($action === 'update') {
		// Вземаме и чистим данните от формата
		$project_id = clean($_POST['project_id'] ?? '');
		$title = clean($_POST['title'] ?? '');
		$description = clean($_POST['description'] ?? '');
		$layer = clean($_POST['layer'] ?? '');
		$priority = clean($_POST['priority'] ?? '');
		$importance = clean($_POST['importance'] ?? '');
		$assigned_to = clean($_POST['assigned_to'] ?? '');
		$status = clean($_POST['status'] ?? '');
		$parent_id = clean($_POST['parent_id'] ?? '');

		// Индикатори (само при нефункционално изискване)
		$indicatorRowsToSave = [];
		if ($requirementType === 'nonfunctional') {
			for ($i = 1; $i <= 3; $i++) {
				$indicatorsData[$i - 1]['name'] = clean($_POST['indicator_name_' . $i] ?? '');
				$indicatorsData[$i - 1]['description'] = clean($_POST['indicator_description_' . $i] ?? '');
				$indicatorsData[$i - 1]['unit'] = clean($_POST['indicator_unit_' . $i] ?? '');
				$indicatorsData[$i - 1]['value'] = clean($_POST['indicator_value_' . $i] ?? '');
			}

			foreach ($indicatorsData as $idx => $row) {
				$hasAny = ($row['name'] !== '' || $row['description'] !== '' || $row['unit'] !== '' || $row['value'] !== '');
				if (!$hasAny) {
					continue;
				}
				if ($row['name'] === '' || $row['description'] === '') {
					$errors[] = 'Индикатор ' . ($idx + 1) . ': Име и описание са задължителни.';
					continue;
				}

				$indicatorRowsToSave[] = [
					'name' => $row['name'],
					'description' => $row['description'],
					'unit' => $row['unit'] !== '' ? $row['unit'] : null,
					'value' => $row['value'] !== '' ? $row['value'] : null,
				];
			}
		} else {
			// За функционални изисквания не показваме/не пазим индикатори
			$indicatorsData = [
				['name' => '', 'description' => '', 'unit' => '', 'value' => ''],
				['name' => '', 'description' => '', 'unit' => '', 'value' => ''],
				['name' => '', 'description' => '', 'unit' => '', 'value' => ''],
			];
		}

		// При смяна на проект - презареждаме родителите, за да се визуализират правилно
		$parentOptions = [];
		$projectIdForParents = (int)$project_id;
		if ($projectIdForParents > 0) {
			try {
				$stmtParents = $conn->prepare("SELECT id, title
					FROM requirements
					WHERE project_id = :project_id
						AND type = 'functional'
						AND id <> :current_id
					ORDER BY id DESC");
				$stmtParents->execute([
					':project_id' => $projectIdForParents,
					':current_id' => $reqId,
				]);
				$parentOptions = $stmtParents->fetchAll();
			} catch (PDOException $e) {
				$parentOptions = [];
			}
		}

		// Валидации
		if ($title === '') {
			$errors[] = 'Заглавието е задължително.';
		}
		if ($description === '') {
			$errors[] = 'Описанието е задължително.';
		}

		$projectIdInt = (int)$project_id;
		if ($projectIdInt <= 0) {
			$errors[] = 'Моля, изберете проект.';
		} else {
			try {
				$stmtProject = $conn->prepare('SELECT id FROM projects WHERE id = :id');
				$stmtProject->execute([':id' => $projectIdInt]);
				if (!$stmtProject->fetch()) {
					$errors[] = 'Избраният проект не съществува.';
				}
			} catch (PDOException $e) {
				$errors[] = 'Възникна грешка при проверка на проекта.';
			}
		}

		// parent_id (по избор)
		$parentIdInt = (int)$parent_id;
		if ($parent_id === '' || $parentIdInt <= 0) {
			$parentIdInt = 0;
		}

		// Ако има избран родител, не валидираме/не изискваме избор на слой от формата.
		if ($parentIdInt <= 0 && !in_array($layer, $allowedLayers, true)) {
			$errors[] = 'Моля, изберете валиден слой.';
		}
		if (!in_array($status, $allowedStatuses, true)) {
			$errors[] = 'Моля, изберете валиден статус.';
		}

		$priorityInt = (int)$priority;
		$importanceInt = (int)$importance;
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
				if (!$stmtUser->fetch()) {
					$errors[] = 'Потребителят във „Възложено на“ не съществува.';
				}
			} catch (PDOException $e) {
				$errors[] = 'Възникна грешка при проверка на потребителя.';
			}
		}

		if ($parentIdInt === $reqId) {
			$errors[] = 'Родителската функционалност не може да е същото изискване.';
		}

		// Проверка: ако има деца, не позволяваме смяна на проекта (за да не се наруши логиката на проекта)
		try {
			$oldProjectId = (int)$requirement['project_id'];
			if ($projectIdInt > 0 && $oldProjectId > 0 && $projectIdInt !== $oldProjectId) {
				$stmtChildCount = $conn->prepare("SELECT COUNT(*) AS cnt FROM requirements WHERE parent_id = :id");
				$stmtChildCount->execute([':id' => $reqId]);
				$childCnt = (int)($stmtChildCount->fetch()['cnt'] ?? 0);
				if ($childCnt > 0) {
					$errors[] = 'Не може да смените проекта, защото има подчинени изисквания. Първо преместете/изтрийте децата.';
				}
			}
		} catch (PDOException $e) {
			$errors[] = 'Възникна грешка при проверка на подчинени изисквания.';
		}

		// Валидация на parent_id: да съществува и да е в същия проект
		// По изискване: при избран родител наследяваме слоя от родителя.
		if ($parentIdInt > 0 && $projectIdInt > 0) {
			try {
				$stmtParent = $conn->prepare("SELECT id, parent_id, layer FROM requirements WHERE id = :id AND project_id = :project_id AND type = 'functional'");
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
						$parentLockedLayer = $parentLayer;
					}

					// Проверка за цикъл: не позволяваме да изберем потомък като родител
					$current = $parentIdInt;
					$steps = 0;
					while ($current > 0 && $steps < 50) {
						if ($current === $reqId) {
							$errors[] = 'Невалидна йерархия: избраният родител би създал цикъл.';
							break;
						}

						$stmtUp = $conn->prepare("SELECT parent_id FROM requirements WHERE id = :id");
						$stmtUp->execute([':id' => $current]);
						$upRow = $stmtUp->fetch();
						if (!$upRow) {
							break;
						}

						$next = isset($upRow['parent_id']) ? (int)$upRow['parent_id'] : 0;
						if ($next <= 0) {
							break;
						}
						$current = $next;
						$steps++;
					}
				}
			} catch (PDOException $e) {
				$errors[] = 'Възникна грешка при проверка на родителската функционалност.';
			}
		}

		// Качване на нова снимка (по избор) - ако има, заменяме старата
		$newImagePath = null;
		if (isset($_FILES['image']) && is_array($_FILES['image']) && ($_FILES['image']['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_NO_FILE) {
			$fileError = (int)($_FILES['image']['error'] ?? UPLOAD_ERR_NO_FILE);

			if ($fileError !== UPLOAD_ERR_OK) {
				$errors[] = 'Грешка при качване на снимката.';
			} else {
				$tmpName = (string)($_FILES['image']['tmp_name'] ?? '');
				$originalName = (string)($_FILES['image']['name'] ?? '');
				$fileSize = (int)($_FILES['image']['size'] ?? 0);

				if ($fileSize <= 0) {
					$errors[] = 'Невалиден файл.';
				} elseif ($fileSize > 2 * 1024 * 1024) {
					$errors[] = 'Снимката трябва да е до 2MB.';
				} else {
					$ext = strtolower(pathinfo($originalName, PATHINFO_EXTENSION));
					$allowedExt = ['jpg', 'jpeg', 'png'];

					if (!in_array($ext, $allowedExt, true)) {
						$errors[] = 'Позволени са само JPG и PNG снимки.';
					} else {
						$imgInfo = @getimagesize($tmpName);
						if ($imgInfo === false) {
							$errors[] = 'Файлът не е валидна снимка.';
						} else {
							$uploadDir = __DIR__ . '/../uploads';
							if (!is_dir($uploadDir)) {
								@mkdir($uploadDir, 0777, true);
							}

							$filename = 'req_' . $reqId . '_' . time() . '_' . bin2hex(random_bytes(4)) . '.' . $ext;
							$destination = $uploadDir . '/' . $filename;

							if (!move_uploaded_file($tmpName, $destination)) {
								$errors[] = 'Неуспешно записване на снимката.';
							} else {
								$newImagePath = 'uploads/' . $filename;
							}
						}
					}
				}
			}
		}

		if (empty($errors)) {
			$assignedToOrNull = $assigned_to !== '' ? $assigned_to : null;
			$parentOrNull = $parentIdInt > 0 ? $parentIdInt : null;
			$imagePathToSave = $newImagePath !== null ? $newImagePath : ($currentImagePath !== '' ? $currentImagePath : null);

			try {
				$conn->beginTransaction();

				$stmtUpdate = $conn->prepare("UPDATE requirements
					SET project_id = :project_id,
						parent_id = :parent_id,
						title = :title,
						description = :description,
						layer = :layer,
						priority = :priority,
						importance = :importance,
						assigned_to = :assigned_to,
						status = :status,
						image_path = :image_path
					WHERE id = :id AND type = :type");

				$stmtUpdate->execute([
					':project_id' => $projectIdInt,
					':parent_id' => $parentOrNull,
					':title' => $title,
					':description' => $description,
					':layer' => $layer,
					':priority' => $priorityInt,
					':importance' => $importanceInt,
					':assigned_to' => $assignedToOrNull,
					':status' => $status,
					':image_path' => $imagePathToSave,
					':id' => $reqId,
					':type' => $requirementType,
				]);

				// Индикатори: при нефункционално изискване заменяме всички индикатори
				if ($requirementType === 'nonfunctional') {
					$stmtDelInd = $conn->prepare('DELETE FROM indicators WHERE requirement_id = :rid');
					$stmtDelInd->execute([':rid' => $reqId]);

					if (!empty($indicatorRowsToSave)) {
						$stmtInsInd = $conn->prepare('INSERT INTO indicators (requirement_id, name, description, unit, value) VALUES (:rid, :name, :description, :unit, :value)');
						foreach ($indicatorRowsToSave as $r) {
							$stmtInsInd->execute([
								':rid' => $reqId,
								':name' => $r['name'],
								':description' => $r['description'],
								':unit' => $r['unit'],
								':value' => $r['value'],
							]);
						}
					}
				}

				$conn->commit();

				// Ако има нова снимка, изтриваме старата от диска
				if ($newImagePath !== null && $currentImagePath !== '' && $currentImagePath !== $newImagePath) {
					$oldFull = realpath(__DIR__ . '/../' . $currentImagePath);
					$uploadsDir = realpath(__DIR__ . '/../uploads');
					if ($oldFull !== false && $uploadsDir !== false && str_starts_with($oldFull, $uploadsDir) && is_file($oldFull)) {
						@unlink($oldFull);
					}
				}

				$successMessage = 'Промените са запазени успешно.';

				// Презареждаме изискването след update
				$stmtReq = $conn->prepare("SELECT id, project_id, parent_id, title, description, layer, priority, importance, assigned_to, status, image_path, type
					FROM requirements
					WHERE id = :id AND type = :type");
				$stmtReq->execute([':id' => $reqId, ':type' => $requirementType]);
				$requirement = $stmtReq->fetch();
				$requirementType = $requirement ? (string)($requirement['type'] ?? $requirementType) : $requirementType;

				$project_id = $requirement ? (string)$requirement['project_id'] : $project_id;
				$parent_id = $requirement ? (string)($requirement['parent_id'] ?? '') : $parent_id;
				$currentImagePath = $requirement ? (string)($requirement['image_path'] ?? '') : $currentImagePath;

				// Презареждаме индикаторите (ако е нефункционално)
				if ($requirement && $requirementType === 'nonfunctional') {
					$indicatorsData = [
						['name' => '', 'description' => '', 'unit' => '', 'value' => ''],
						['name' => '', 'description' => '', 'unit' => '', 'value' => ''],
						['name' => '', 'description' => '', 'unit' => '', 'value' => ''],
					];

					try {
						$stmtInd = $conn->prepare("SELECT name, description, unit, value FROM indicators WHERE requirement_id = :rid ORDER BY id ASC");
						$stmtInd->execute([':rid' => $reqId]);
						$rows = $stmtInd->fetchAll();
						$idx = 0;
						foreach ($rows as $r) {
							if ($idx >= 3) {
								break;
							}
							$indicatorsData[$idx]['name'] = (string)($r['name'] ?? '');
							$indicatorsData[$idx]['description'] = (string)($r['description'] ?? '');
							$indicatorsData[$idx]['unit'] = (string)($r['unit'] ?? '');
							$indicatorsData[$idx]['value'] = (string)($r['value'] ?? '');
							$idx++;
						}
					} catch (PDOException $e) {
						// Оставяме празни индикатори
					}
				}
			} catch (PDOException $e) {
				if ($conn->inTransaction()) {
					$conn->rollBack();
				}
				$errors[] = 'Възникна грешка при запис в базата данни.';

				// Ако сме качили нова снимка, но записът се провали, чистим файла
				if ($newImagePath !== null) {
					$full = __DIR__ . '/' . $newImagePath;
					if (is_file($full)) {
						@unlink($full);
					}
				}
			}
		}
	} elseif ($action === 'delete') {
		// Изтриване (изисква потвърждение)
		$confirm = clean($_POST['confirm'] ?? '');
		if ($confirm !== 'yes') {
			$errors[] = 'Моля, потвърдете изтриването.';
			$confirmDelete = true;
		} else {
			try {
				// Събираме всички ID-та в поддървото (за да изтрием снимките)
				$ids = [];
				$queue = [$reqId];
				$seen = [];

				$stmtChildren = $conn->prepare("SELECT id FROM requirements WHERE parent_id = :pid");
				while (!empty($queue)) {
					$current = array_shift($queue);
					if (isset($seen[$current])) {
						continue;
					}
					$seen[$current] = true;
					$ids[] = $current;

					$stmtChildren->execute([':pid' => $current]);
					$children = $stmtChildren->fetchAll();
					foreach ($children as $ch) {
						$cid = (int)$ch['id'];
						if ($cid > 0 && !isset($seen[$cid])) {
							$queue[] = $cid;
						}
					}
				}

				// Вземаме всички image_path за тези изисквания
				$imagePaths = [];
				if (!empty($ids)) {
					$placeholders = implode(',', array_fill(0, count($ids), '?'));
					$stmtImg = $conn->prepare("SELECT image_path FROM requirements WHERE id IN ($placeholders)");
					$stmtImg->execute($ids);
					$rowsImg = $stmtImg->fetchAll();
					foreach ($rowsImg as $r) {
						$ip = isset($r['image_path']) ? (string)$r['image_path'] : '';
						if ($ip !== '') {
							$imagePaths[] = $ip;
						}
					}
				}

				// Изтриваме основното изискване (децата ще се изтрият каскадно)
				$stmtDel = $conn->prepare("DELETE FROM requirements WHERE id = :id AND type = :type");
				$stmtDel->execute([':id' => $reqId, ':type' => $requirementType]);

				if ($stmtDel->rowCount() <= 0) {
					$errors[] = 'Неуспешно изтриване.';
				} else {
					// Изтриваме снимките от диска (само от uploads/)
					$uploadsDir = realpath(__DIR__ . '/../uploads');
					foreach ($imagePaths as $ip) {
						if (!str_starts_with($ip, 'uploads/') || str_contains($ip, '..')) {
							continue;
						}

						$full = realpath(__DIR__ . '/' . $ip);
						if ($uploadsDir !== false && $full !== false && str_starts_with($full, $uploadsDir) && is_file($full)) {
							@unlink($full);
						}
					}

					if ($requirementType === 'nonfunctional') {
						header('Location: nonfunctional.php');
					} else {
						header('Location: functional.php');
					}
					exit;
				}
			} catch (PDOException $e) {
				$errors[] = 'Възникна грешка при изтриване.';
			}
		}
	}
}

require_once __DIR__ . '/header.php';
require_once __DIR__ . '/menu.php';
?>

<main class="content">
	<h2>Редакция на изискване</h2>

	<p>
		<?php if ($requirementType === 'nonfunctional'): ?>
			<a class="btn" href="nonfunctional.php">Назад към нефункционални изисквания</a>
		<?php else: ?>
			<a class="btn" href="functional.php">Назад към функционални изисквания</a>
		<?php endif; ?>
	</p>

	<?php if ($errorMessage !== ''): ?>
		<p class="text-error"><?php echo htmlspecialchars($errorMessage, ENT_QUOTES, 'UTF-8'); ?></p>
	<?php endif; ?>

	<?php if ($successMessage !== ''): ?>
		<p class="text-success"><?php echo htmlspecialchars($successMessage, ENT_QUOTES, 'UTF-8'); ?></p>
	<?php endif; ?>

	<?php if (!empty($errors)): ?>
		<ul class="text-error">
			<?php foreach ($errors as $err): ?>
				<li><?php echo htmlspecialchars($err, ENT_QUOTES, 'UTF-8'); ?></li>
			<?php endforeach; ?>
		</ul>
	<?php endif; ?>

	<?php if ($requirement): ?>
		<section class="card">
			<h3>Данни за изискването</h3>
			<p>
				<strong>Тип:</strong>
				<?php echo htmlspecialchars($requirementType === 'nonfunctional' ? 'Нефункционално' : 'Функционално', ENT_QUOTES, 'UTF-8'); ?>
			</p>

			<form method="post" action="edit_requirement.php?id=<?php echo (int)$reqId; ?>" enctype="multipart/form-data">
				<input type="hidden" name="action" value="update">

				<label for="project_id">Проект</label><br>
				<select id="project_id" name="project_id" required>
					<option value="">-- Изберете проект --</option>
					<?php foreach ($projects as $p): ?>
						<option value="<?php echo (int)$p['id']; ?>" <?php echo ((int)$project_id === (int)$p['id']) ? 'selected' : ''; ?>>
							<?php echo htmlspecialchars((string)$p['name'], ENT_QUOTES, 'UTF-8'); ?>
						</option>
					<?php endforeach; ?>
				</select>
				<br><br>

				<label for="title">Заглавие</label><br>
				<input type="text" id="title" name="title" value="<?php echo $title; ?>" required>
				<br><br>

				<label for="description">Описание</label><br>
				<textarea id="description" name="description" required><?php echo $description; ?></textarea>
				<br><br>

				<label for="layer">Слой</label><br>
				<?php if ((int)$parent_id > 0): ?>
					<input type="hidden" name="layer" value="<?php echo htmlspecialchars($layer, ENT_QUOTES, 'UTF-8'); ?>">
					<p><strong><?php echo htmlspecialchars($layer, ENT_QUOTES, 'UTF-8'); ?></strong> <em>(наследен от родителя)</em></p>
				<?php else: ?>
					<select id="layer" name="layer" required>
						<?php foreach ($allowedLayers as $l): ?>
							<option value="<?php echo htmlspecialchars($l, ENT_QUOTES, 'UTF-8'); ?>" <?php echo ($layer === $l) ? 'selected' : ''; ?>>
								<?php echo htmlspecialchars($l, ENT_QUOTES, 'UTF-8'); ?>
							</option>
						<?php endforeach; ?>
					</select>
				<?php endif; ?>
				<br><br>

				<label for="priority">Приоритет (1-5)</label><br>
				<input type="text" id="priority" name="priority" value="<?php echo htmlspecialchars($priority, ENT_QUOTES, 'UTF-8'); ?>" required>
				<br><br>

				<label for="importance">Важност (1-5)</label><br>
				<input type="text" id="importance" name="importance" value="<?php echo htmlspecialchars($importance, ENT_QUOTES, 'UTF-8'); ?>" required>
				<br><br>

				<label for="assigned_to">Възложено на (username)</label><br>
				<input type="text" id="assigned_to" name="assigned_to" value="<?php echo htmlspecialchars($assigned_to, ENT_QUOTES, 'UTF-8'); ?>">
				<br><br>

				<label for="status">Статус</label><br>
				<select id="status" name="status" required>
					<?php foreach ($allowedStatuses as $st): ?>
						<option value="<?php echo htmlspecialchars($st, ENT_QUOTES, 'UTF-8'); ?>" <?php echo ($status === $st) ? 'selected' : ''; ?>>
							<?php echo htmlspecialchars($statusLabels[$st] ?? $st, ENT_QUOTES, 'UTF-8'); ?>
						</option>
					<?php endforeach; ?>
				</select>
				<br><br>

				<label for="parent_id">Родителска функционалност (по избор)</label><br>
				<select id="parent_id" name="parent_id">
					<option value="">-- Няма --</option>
					<?php foreach ($parentOptions as $p): ?>
						<option value="<?php echo (int)$p['id']; ?>" <?php echo ((string)$parent_id === (string)$p['id']) ? 'selected' : ''; ?>>
							<?php echo htmlspecialchars((string)$p['title'], ENT_QUOTES, 'UTF-8'); ?>
						</option>
					<?php endforeach; ?>
				</select>
				<br><br>

				<?php if ($requirementType === 'nonfunctional'): ?>
					<details open>
						<summary><strong>Индикатори</strong></summary>
						<p>Можете да добавите до 3 индикатора. Име и описание са задължителни.</p>

						<?php for ($i = 1; $i <= 3; $i++): ?>
							<fieldset style="margin-bottom: 12px;">
								<legend>Индикатор <?php echo $i; ?></legend>

								<label for="indicator_name_<?php echo $i; ?>">Име (задължително)</label><br>
								<input type="text" id="indicator_name_<?php echo $i; ?>" name="indicator_name_<?php echo $i; ?>"
									value="<?php echo $indicatorsData[$i - 1]['name']; ?>"><br><br>

								<label for="indicator_description_<?php echo $i; ?>">Описание (задължително)</label><br>
								<textarea id="indicator_description_<?php echo $i; ?>" name="indicator_description_<?php echo $i; ?>"><?php echo $indicatorsData[$i - 1]['description']; ?></textarea><br><br>

								<label for="indicator_unit_<?php echo $i; ?>">Единица (по избор)</label><br>
								<input type="text" id="indicator_unit_<?php echo $i; ?>" name="indicator_unit_<?php echo $i; ?>"
									value="<?php echo $indicatorsData[$i - 1]['unit']; ?>"><br><br>

								<label for="indicator_value_<?php echo $i; ?>">Стойност (по избор)</label><br>
								<input type="text" id="indicator_value_<?php echo $i; ?>" name="indicator_value_<?php echo $i; ?>"
									value="<?php echo $indicatorsData[$i - 1]['value']; ?>">
							</fieldset>
						<?php endfor; ?>
					</details>

					<br>
				<?php endif; ?>

				<label>Текуща снимка</label><br>
				<?php if ($currentImagePath !== ''): ?>
					<p>
						<a class="btn" href="image.php?req_id=<?php echo (int)$reqId; ?>">Преглед на снимка</a>
					</p>
				<?php else: ?>
					<p>Няма снимка</p>
				<?php endif; ?>

				<label for="image">Качи нова снимка (JPG/PNG, до 2MB)</label><br>
				<input type="file" id="image" name="image" accept="image/png, image/jpeg">
				<br><br>

				<button type="submit">Запази промените</button>
			</form>
		</section>

		<section class="card">
			<h3>Изтриване</h3>
			<p>Внимание: изтриването ще премахне и всички подчинени изисквания (каскадно).</p>

			<?php if (!$confirmDelete): ?>
				<a class="btn" href="edit_requirement.php?id=<?php echo (int)$reqId; ?>&confirm_delete=1">Изтрий</a>
			<?php else: ?>
				<form method="post" action="edit_requirement.php?id=<?php echo (int)$reqId; ?>&confirm_delete=1">
					<input type="hidden" name="action" value="delete">
					<p>Сигурни ли сте, че искате да изтриете това изискване?</p>
					<button type="submit" name="confirm" value="yes">Да, изтрий</button>
					<a class="btn" href="edit_requirement.php?id=<?php echo (int)$reqId; ?>">Отказ</a>
				</form>
			<?php endif; ?>
		</section>
	<?php endif; ?>
</main>

</div>
</body>
</html>
