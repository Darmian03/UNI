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
- `torch` (NN обучение/инференс)
- `numpy` (входни тензори)
- `pygame` (GUI)

## Команди (от `AI/Project`)

Инсталация:

pip install python-chess numpy torch pygame

Генериране на данни (50k позиции, low elo):

python data_generation/main.py --num_positions 50 --elo low

Обучение на модел:

python NN_model/train_nn.py --dataset stockfish_eval_50k_low_elo.csv --epochs 5

Експерименти:

python run_experiments.py --num_games 10 --model_a stockfish --model_a_depth 8 --model_b custom --model_b_depth 3

GUI:

python gui.py

Stockfish се взима от `STOCKFISH_PATH` или от `C:\Program Files\stockfish\`.
