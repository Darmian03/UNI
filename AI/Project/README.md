# Chess AI Project

Проектът реализира избор на ход с:
- Stockfish (UCI)
- Minimax + custom evaluation
- Minimax + Neural Network evaluator (supervised learning върху Stockfish оценки)

## Архитектура (1 минута)

- `data_generation/` → взима позиции от `data/games.pgn` и прави CSV в `data/` (`best_move`, `best_eval`).
- `NN_model/` → тренира NN модел от CSV и записва `.pt` в `trained_models/`.
- `minimax.py` + `custom_eval_engine.py` → търсене и ръчна оценка.
- `run_experiments.py` → пуска мачове и записва резултати JSON в `results/`.
- `gui.py` → pygame GUI за игра + post-game анализ.

## Библиотеки

- `python-chess` (board/engine/UCI)
- `torch` (NN обучение/инференс; CUDA build за GPU)
- `numpy` (входни тензори)
- `pygame-ce` (GUI; drop-in за pygame — официалният pygame няма wheel за Python 3.14)
- `tqdm` (progress bars при експерименти/обучение/генериране на данни)

## Команди (от `AI/Project`)

Инсталация:

pip install -r requirements.txt

Stockfish се намира автоматично от PATH (`stockfish`), от известни локации
(`/usr/games/stockfish`, `/usr/local/bin/stockfish`, `~/bin/stockfish`, Windows папки)
или чрез променливата `STOCKFISH_PATH`. Инсталация:

- Linux (Ubuntu/Debian): `sudo apt install stockfish`
- macOS: `brew install stockfish`
- Windows: https://stockfishchess.org/download/

GPU (по избор): torch от PyPI е CUDA-enabled; провери с
`python -c "import torch; print(torch.cuda.is_available())"`.

Генериране на данни (50k позиции, low elo):

python data_generation/main.py --num_positions 50 --elo low

Обучение на модел (`--device`: `auto` (по подразбиране) / `cpu` / `cuda` / `cuda:<n>`; без CUDA → автоматично CPU):

python NN_model/train_nn.py --dataset stockfish_eval_50k_low_elo.csv --epochs 5 --device auto

Експерименти (`--device` за NN оценките, същи стойности; по подразбиране `auto`):

python run_experiments.py --num_games 10 --model_a stockfish --model_a_depth 8 --model_b custom --model_b_depth 3

GUI:

python gui.py
