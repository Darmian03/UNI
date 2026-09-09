	// За показване/скриване на индикаторите
	(function () {
		var indicatorsBlock = document.getElementById('indicatorsBlock');
		var indicatorsHint = document.getElementById('indicatorsHint');
		var typeRadios = document.querySelectorAll('input[name="type"]');

		function setIndicatorsEnabled(enabled) {
			if (!indicatorsBlock) return;
			var fields = indicatorsBlock.querySelectorAll('input, textarea, select');
			for (var i = 0; i < fields.length; i++) {
				fields[i].disabled = !enabled;
			}
		}

		function updateIndicatorsVisibility() {
			var selected = document.querySelector('input[name="type"]:checked');
			var isNonFunctional = selected && selected.value === 'nonfunctional';

			if (indicatorsBlock) {
				indicatorsBlock.style.display = isNonFunctional ? 'block' : 'none';
			}
			if (indicatorsHint) {
				indicatorsHint.style.display = isNonFunctional ? 'none' : 'block';
			}

			// Когато са скрити, изключваме полетата, за да не се изпращат случайно
			setIndicatorsEnabled(isNonFunctional);
		}

		for (var i = 0; i < typeRadios.length; i++) {
			typeRadios[i].addEventListener('change', updateIndicatorsVisibility);
		}

		// При зареждане на страницата
		updateIndicatorsVisibility();
	})();