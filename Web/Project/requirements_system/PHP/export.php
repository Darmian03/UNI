<?php
// Страница: Експорт на проект и визуализация на йерархията (PlantUML MindMap)

session_start();

// Проверка дали потребителят е влязъл
if (!isset($_SESSION['user_id']) || !isset($_SESSION['username'])) {
	header('Location: index.php');
	exit;
}

require_once __DIR__ . '/../classes/Database.php';

$database = new Database();
$conn = $database->getConnection();

// Помощна функция за trim + htmlspecialchars (за показване в HTML)
function clean($value): string
{
	$value = (string)$value;
	$value = trim($value);
	return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
}

function normalizeTextForMindmap(string $text): string
{
	// Много проста нормализация, за да не чупим PlantUML редовете
	$text = str_replace(["\r", "\n"], ' ', $text);
	$text = trim($text);
	// Звездичката има специална роля в mindmap синтаксиса
	$text = str_replace('*', '\\*', $text);
	return $text;
}

$statusLabels = [
	'not_started' => 'Не е започната',
	'in_progress' => 'В процес',
	'done' => 'Завършена',
];

$allowedLayers = ['client', 'routing', 'business', 'database', 'install_test'];

// Вземаме проектите за избор
$projects = [];
try {
	$stmtProjects = $conn->prepare('SELECT id, name FROM projects ORDER BY name ASC');
	$stmtProjects->execute();
	$projects = $stmtProjects->fetchAll();
} catch (PDOException $e) {
	$projects = [];
}

$projectId = isset($_GET['project_id']) ? (int)$_GET['project_id'] : 0;
$download = isset($_GET['download']) ? (string)$_GET['download'] : '';

$errorMessage = '';
$projectName = '';
$projectDescription = '';
$requirements = [];

// Зареждаме функционалностите за даден проект
if ($projectId > 0) {
	try {
		$stmtProject = $conn->prepare('SELECT id, name, description FROM projects WHERE id = :id');
		$stmtProject->execute([':id' => $projectId]);
		$proj = $stmtProject->fetch();
		if (!$proj) {
			$errorMessage = 'Избраният проект не съществува.';
		} else {
			$projectName = (string)$proj['name'];
			$projectDescription = (string)($proj['description'] ?? '');

			$stmtReq = $conn->prepare("SELECT id, project_id, parent_id, title, description, layer, status, priority, importance, assigned_to, type
				FROM requirements
				WHERE project_id = :project_id AND type IN ('functional','nonfunctional')
				ORDER BY id ASC");
			$stmtReq->execute([':project_id' => $projectId]);
			$requirements = $stmtReq->fetchAll();
		}
	} catch (PDOException $e) {
		$errorMessage = 'Възникна грешка при зареждане на данните за експорт.';
	}
}

// Помощни структури за йерархия
$reqById = [];
$childrenByParent = []; // parent_id => [childId, ...]
foreach ($requirements as $r) {
	$id = (int)$r['id'];
	$parentId = isset($r['parent_id']) ? (int)$r['parent_id'] : 0;
	if ($parentId <= 0) {
		$parentId = 0;
	}

	$reqById[$id] = $r;
	if (!isset($childrenByParent[$parentId])) {
		$childrenByParent[$parentId] = [];
	}
	$childrenByParent[$parentId][] = $id;
}

function buildCsv(
	PDO $conn,
	string $projectName,
	string $projectDescription,
	array $requirements,
	array $reqById,
	array $childrenByParent
): string
{
	$fp = fopen('php://temp', 'r+');
	if ($fp === false) {
		return '';
	}

	// UTF-8 BOM (по-удобно за Excel)
	fwrite($fp, "\xEF\xBB\xBF");

	// Формат за импорт: PROJECT/REQ редове
	$projectLine = ['PROJECT', $projectName, $projectDescription];
	fputcsv($fp, $projectLine, ';');

	// Изнасяме всички изисквания (functional + nonfunctional)
	$allIds = [];
	foreach ($requirements as $r) {
		$allIds[] = (int)$r['id'];
	}

	$allSet = array_fill_keys($allIds, true);

	// Подреждаме така, че родителите да са преди децата
	$visited = [];
	$queue = [$childrenByParent[0] ?? []];
	$orderedIds = [];

	// DFS по слой не е нужен за импорт - просто йерархично
	$stack = [];
	if (!empty($childrenByParent[0])) {
		for ($i = count($childrenByParent[0]) - 1; $i >= 0; $i--) {
			$stack[] = (int)$childrenByParent[0][$i];
		}
	}

	while (!empty($stack)) {
		$nodeId = array_pop($stack);
		if (isset($visited[$nodeId])) {
			continue;
		}
		$visited[$nodeId] = true;
		$orderedIds[] = $nodeId;
		$childIds = $childrenByParent[$nodeId] ?? [];
		for ($i = count($childIds) - 1; $i >= 0; $i--) {
			$stack[] = (int)$childIds[$i];
		}
	}

	// Добавяме останалите, ако са били пропуснати (например липсващ parent)
	foreach ($allIds as $rid) {
		if (!isset($visited[$rid])) {
			$orderedIds[] = $rid;
		}
	}

	// Подготвяме индикаторите
	$indicatorsByReq = [];
	try {
		$idsForIndicators = array_values(array_unique($orderedIds));
		if (!empty($idsForIndicators)) {
			$placeholders = implode(',', array_fill(0, count($idsForIndicators), '?'));
			$stmtInd = $conn->prepare("SELECT requirement_id, name, description, unit, value FROM indicators WHERE requirement_id IN ($placeholders) ORDER BY id ASC");
			$stmtInd->execute($idsForIndicators);
			$rows = $stmtInd->fetchAll();
			foreach ($rows as $row) {
				$rid = (int)($row['requirement_id'] ?? 0);
				if (!isset($indicatorsByReq[$rid])) {
					$indicatorsByReq[$rid] = [];
				}
				$indicatorsByReq[$rid][] = [
					'name' => (string)($row['name'] ?? ''),
					'description' => (string)($row['description'] ?? ''),
					'unit' => (string)($row['unit'] ?? ''),
					'value' => (string)($row['value'] ?? ''),
				];
			}
		}
	} catch (PDOException $e) {
		$indicatorsByReq = [];
	}

	foreach ($orderedIds as $id) {
		if (!isset($reqById[$id])) {
			continue;
		}
		$r = $reqById[$id];
		$parentId = isset($r['parent_id']) ? (int)$r['parent_id'] : 0;

		$code = 'R' . $id;
		$parentCode = ($parentId > 0 && isset($allSet[$parentId])) ? ('R' . $parentId) : '';

		$type = (string)($r['type'] ?? 'functional');

		// Индикатори: name|description|unit|value || name|description|unit|value
		$indicatorsSerialized = '';
		if (!empty($indicatorsByReq[$id])) {
			$parts = [];
			foreach ($indicatorsByReq[$id] as $ind) {
				$parts[] = implode('|', [
					$ind['name'],
					$ind['description'],
					$ind['unit'],
					$ind['value'],
				]);
			}
			$indicatorsSerialized = implode('||', $parts);
		}

		$row = [
			'REQ',
			$code,
			$parentCode,
			$type,
			(string)($r['title'] ?? ''),
			(string)($r['description'] ?? ''),
			(string)($r['layer'] ?? ''),
			(int)($r['priority'] ?? 0),
			(int)($r['importance'] ?? 0),
			(string)($r['assigned_to'] ?? ''),
			(string)($r['status'] ?? ''),
			$indicatorsSerialized,
		];
		fputcsv($fp, $row, ';');
	}

	rewind($fp);
	$content = stream_get_contents($fp);
	fclose($fp);

	return $content !== false ? $content : '';
}

function buildMindmapText(
	string $projectName,
	array $allowedLayers,
	array $reqById,
	array $childrenByParent
): string {
	$lines = [];
	$lines[] = '@startmindmap';
	$lines[] = '* ' . normalizeTextForMindmap($projectName);

	// Групиране по слой - първо намираме корените (parent_id = NULL/0) и ги разпределяме по слой
	$rootsByLayer = [];
	foreach ($allowedLayers as $layer) {
		$rootsByLayer[$layer] = [];
	}

	$rootIds = $childrenByParent[0] ?? [];
	foreach ($rootIds as $rid) {
		$layer = (string)($reqById[$rid]['layer'] ?? '');
		if (!isset($rootsByLayer[$layer])) {
			$rootsByLayer[$layer] = [];
		}
		$rootsByLayer[$layer][] = $rid;
	}

	// Използваме прост DFS със стек (учебно и без външни библиотеки)
	$maxDepth = 50;
	foreach ($rootsByLayer as $layer => $layerRoots) {
		if (empty($layerRoots)) {
			continue;
		}

		$lines[] = '** ' . normalizeTextForMindmap($layer);

		foreach ($layerRoots as $rootId) {
			// Стек за DFS: [id, depth]
			$stack = [[(int)$rootId, 3]];
			$visited = [];

			while (!empty($stack)) {
				$item = array_pop($stack);
				$nodeId = (int)$item[0];
				$depth = (int)$item[1];

				if ($depth > $maxDepth) {
					continue;
				}
				if (isset($visited[$nodeId])) {
					continue;
				}
				$visited[$nodeId] = true;

				$title = (string)($reqById[$nodeId]['title'] ?? '');
				$type = (string)($reqById[$nodeId]['type'] ?? 'functional');
				if ($type === 'nonfunctional') {
					$title .= ' (НФ)';
				}
				$lines[] = str_repeat('*', $depth) . ' ' . normalizeTextForMindmap($title);

				// Деца
				$childIds = $childrenByParent[$nodeId] ?? [];
				// За да запазим реда, пушваме обратно
				for ($i = count($childIds) - 1; $i >= 0; $i--) {
					$cid = (int)$childIds[$i];
					$stack[] = [$cid, $depth + 1];
				}
			}
		}
	}

	$lines[] = '@endmindmap';
	return implode("\n", $lines) . "\n";
}

$csvContent = '';
$mindmapText = '';

if ($projectId > 0 && $errorMessage === '') {
	$csvContent = buildCsv($conn, $projectName, $projectDescription, $requirements, $reqById, $childrenByParent);
	$mindmapText = buildMindmapText($projectName, $allowedLayers, $reqById, $childrenByParent);
}

// Download endpoints (без да печатаме HTML)
if ($download !== '' && $projectId > 0 && $errorMessage === '') {
	$safeBaseName = preg_replace('/[^a-zA-Z0-9_\-]+/u', '_', $projectName);
	if ($safeBaseName === '' || $safeBaseName === null) {
		$safeBaseName = 'project';
	}

	if ($download === 'csv') {
		header('Content-Type: text/csv; charset=utf-8');
		header('Content-Disposition: attachment; filename="' . $safeBaseName . '_export.csv"');
		echo $csvContent;
		exit;
	}

	if ($download === 'mindmap') {
		header('Content-Type: text/plain; charset=utf-8');
		header('Content-Disposition: attachment; filename="' . $safeBaseName . '_mindmap.txt"');
		echo $mindmapText;
		exit;
	}
}

require_once __DIR__ . '/header.php';
require_once __DIR__ . '/menu.php';
?>

<main class="content">
	<h2>Експорт</h2>

	<section class="card">
		<h3>Избор на проект</h3>
		<form method="get" action="export.php">
			<label for="project_id">Проект</label><br>
			<select id="project_id" name="project_id" required>
				<option value="">-- Изберете проект --</option>
				<?php foreach ($projects as $p): ?>
					<option value="<?php echo (int)$p['id']; ?>" <?php echo ((int)$projectId === (int)$p['id']) ? 'selected' : ''; ?>>
						<?php echo htmlspecialchars((string)$p['name'], ENT_QUOTES, 'UTF-8'); ?>
					</option>
				<?php endforeach; ?>
			</select>
			<br><br>
			<button type="submit">Зареди</button>
		</form>
	</section>

	<?php if ($errorMessage !== ''): ?>
		<p class="text-error"><?php echo clean($errorMessage); ?></p>
	<?php endif; ?>

	<?php if ($projectId > 0 && $errorMessage === ''): ?>
		<section class="card">
			<h3>Експорт като CSV</h3>
			<p>CSV файлът е съвместим с импорта (PROJECT/REQ редове) и включва всички изисквания (вкл. нефункционални), с индикатори.</p>
			<p>
				<a class="btn" href="export.php?project_id=<?php echo (int)$projectId; ?>&download=csv">Изтегли CSV</a>
			</p>
		</section>

		<section class="card">
			<h3>PlantUML MindMap</h3>
			<p>
				Линк към документацията: <a href="https://plantuml.com/mindmap-diagram" target="_blank" rel="noopener noreferrer">https://plantuml.com/mindmap-diagram</a>
			</p>
			<p>
				<a class="btn" href="export.php?project_id=<?php echo (int)$projectId; ?>&download=mindmap">Изтегли като .txt</a>
			</p>

			<label for="mindmap">Генериран текст</label><br>
			<textarea id="mindmap" readonly style="width: 100%; min-height: 320px;"><?php echo htmlspecialchars($mindmapText, ENT_QUOTES, 'UTF-8'); ?></textarea>
		</section>
	<?php endif; ?>
</main>

</div>
</body>
</html>
