// Сцена: фон + камера
background('#070818');
lookAt([0, 400, 0], [0, 0, 0]);


// Обекти в сцената
sun = sphere([0, 0, 0], 30, '#ffcc33');

earthOrbitSize = 200;
earth = sphere([earthOrbitSize / 2, 0, 0], 10, '#3b82f6');
earthOrbit = circle([0, 0, 0], earthOrbitSize, 'white').style({ wireframe: true });
earthOrbit.spinV = 90;


// Глобално състояние за интеракция
var grid = null;
var hideDetails = true;


// UI: checkbox-и (линии/детайли)
var chkGrid = document.getElementById('chkGridLines');
chkGrid.addEventListener('change', gridLines);

var chkHide = document.getElementById('chkHideDetails');
chkHide.addEventListener('change', applyHideDetails);

// UI: бутони за калкулаторите
var btnTemp = document.getElementById('btnTempConvert');
btnTemp.addEventListener('click', convertKelvinCelsius);

var btnTime = document.getElementById('btnTimeConvert');
btnTime.addEventListener('click', convertSecondsDays);


// Скриване/показване на детайлите в панела
function applyHideDetails() {
	hideDetails = !hideDetails;
	if (hideDetails) {
		// Скриване
		document.getElementById('valTemperature').textContent = '??? °C';
		document.getElementById('valSpeed').textContent = '??? km/s';
		document.getElementById('valYear').textContent = '??? дни';
	}
	else {
		// Показване
		planet = document.getElementById('planetName');
		if (planet.textContent == 'Земя') {
			details(earth);
		}
		if (planet.textContent == 'Слънце') {
			details(sun);
		}
	}
}


// Помощни линии (координатна мрежа)
function gridLines() {
	// Скриване/показване на линиите. Ако grid е null (не е създаден), създаваме го, ако е създаден - само променяме видимостта.
	if (!chkGrid.checked) {
		grid.visible = false;
		return;
	}
	if (chkGrid.checked && grid) {
		grid.visible = true;
		return;
	}

	// Линиите по x и z осите
	grid = group();
	grid.add(
		line([-400, 0, 0], [400, 0, 0], 'white'),
		line([0, 0, -400], [0, 0, 400], 'white')
	);

	// Допълнителни линии на всеки 10 единици, по-дебели на всеки 50
	for (var i = -200; i <= 200; i += 10) {
		if (i % 50 == 0) {
			grid.add(
				line([-5, 0, i], [5, 0, i], 'white'),
				line([i, 0, -5], [i, 0, 5], 'white')
			);
		}
		else {
			grid.add(
				line([-2, 0, i], [2, 0, i], 'gray'),
				line([i, 0, -2], [i, 0, 2], 'gray')
			);
		}
	}
}


// Pointer: избор на обект
function pointerDown(event) {
	obj = findObject(event); // По някаква причина не може да е var

	if (obj == earth || obj == sun) {
		// Показване на детайлите за избрания обект ако кликнем на него
		details(obj);
	}
}

// Pointer: край на влаченето
function pointerUp(event) {
	obj = null;
}

// Pointer: влачене на Земята (променя орбитата)
function pointerMove(event) {
	if (obj) {
		var newPos = findPosition(event);

		if (obj == earth) {
			// Разстоянието от центъра до Земята
			var r = Math.sqrt(newPos[0] * newPos[0] + newPos[1] * newPos[1]);
			// Нова позиция на Земята
			obj.x = 0.66 * newPos[0];
			obj.z = 0.66 * -newPos[1];
			// Нов размер на орбитата
			earthOrbit.width = 1.33 * r;
			earthOrbit.height = 1.33 * r;
			// Обновяване на детайлите
			details(earth);
		}
	}
}


// Обновяване на info панела (разстояние/температура/скорост/година)
function details(planet) {
	// Елементи в панела, където ще показваме стойностите
	var nameEl = document.getElementById('planetName');
	var dEl = document.getElementById('valDistance');
	var tEl = document.getElementById('valTemperature');
	var vEl = document.getElementById('valSpeed');
	var yEl = document.getElementById('valYear');

	// Име на избрания обект
	var name = 'Планета';
	if (planet == sun) name = 'Слънце';
	if (planet == earth) name = 'Земя';
	nameEl.textContent = name;

	// Разстояние (в равнината XZ)
	var distanceKm = Math.sqrt(planet.x * planet.x + planet.z * planet.z) * 1_000_000;

	// Специален случай: ако разстоянието е 0 (Слънцето)
	if (distanceKm <= 0 && !hideDetails) {
		dEl.textContent = '0 млн. km';
		tEl.textContent = 'Ден за скара';
		vEl.textContent = '??? km/s';
		yEl.textContent = '??? дни';
		return;
	}

	// Формули (вход r в километри) + конверсии
	var tempK = 3.5e6 / Math.sqrt(distanceKm);
	var tempC = tempK - 273.15;
	var speedKm = 3.6e5 / Math.sqrt(distanceKm);
	var yearS = 1.7e-5 * Math.pow(distanceKm, 1.5);
	var yearDays = yearS / 86400;

	// Показване в удобен формат на разстоянието
	dEl.textContent = (distanceKm / 1_000_000).toFixed(0) + ' млн. km';

	// Скриване на детайлите, ако е избрано
	if (hideDetails) {
		tEl.textContent = '??? °C';
		vEl.textContent = '??? km/s';
		yEl.textContent = '??? дни';
		return;
	}

	// Показване на изчислените стойности
	tEl.textContent = tempC.toFixed(2) + ' °C';
	vEl.textContent = speedKm.toFixed(2) + ' km/s';
	yEl.textContent = yearDays.toFixed(2) + ' дни';
}


// Калкулатори
// Температура: K <-> °C
function convertKelvinCelsius() {
	// Елементи в панела, където ще показваме/взимаме стойностите
	var kEl = document.getElementById('inpKelvin');
	var cEl = document.getElementById('inpCelsius');

	// Приоритет: ако има K, конвертираме към °C
	if (kEl.value != '') {
		cEl.value = (Number(kEl.value) - 273.15).toFixed(2);
		return;
	}
	if (cEl.value != '') {
		kEl.value = (Number(cEl.value) + 273.15).toFixed(2);
	}
}

// Време: секунди <-> дни
function convertSecondsDays() {
	// Елементи в панела, където ще показваме/взимаме стойностите
	var sEl = document.getElementById('inpSeconds');
	var dEl = document.getElementById('inpDays');

	// Приоритет: ако има секунди, конвертираме към дни
	if (sEl.value != '') {
		dEl.value = (Number(sEl.value) / 86400).toFixed(2);
		return;
	}
	if (dEl.value != '') {
		sEl.value = (Number(dEl.value) * 86400).toFixed(0);
	}
}