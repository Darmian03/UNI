<?php

require_once __DIR__ . '/Database.php';

/**
 * Клас User
 * - Прост модел за потребител и базова автентикация.
 * - Подходящ за учебен проект (не е за production).
 */
class User
{
	public ?int $id = null;
	public string $username = '';
	public string $password = '';

	// Последна грешка (текст на български)
	public string $error = '';

	private PDO $conn;

	/**
	 * Създаваме User обект с връзка към базата.
	 */
	public function __construct(Database $database)
	{
		$this->conn = $database->getConnection();
	}

	/**
	 * Регистрация на нов потребител.
	 * - Връща true при успех, false при грешка.
	 */
	public function register($username, $password): bool
	{
		$this->error = '';

		$username = $this->sanitizeInput($username);
		$password = $this->sanitizeInput($password);

		// Базова валидация
		if ($username === '' || $password === '') {
			$this->error = 'Моля, попълнете потребителско име и парола.';
			return false;
		}

		if (mb_strlen($username) < 3) {
			$this->error = 'Потребителското име трябва да е поне 3 символа.';
			return false;
		}

		if (mb_strlen($password) < 4) {
			$this->error = 'Паролата трябва да е поне 4 символа.';
			return false;
		}

		// За учебен проект може да използваме прост хеш (md5).
		// В реални проекти се използва password_hash().
		$hashedPassword = $this->hashPassword($password);

		try {
			$sql = 'INSERT INTO users (username, password) VALUES (:username, :password)';
			$stmt = $this->conn->prepare($sql);
			$stmt->execute([
				':username' => $username,
				':password' => $hashedPassword,
			]);

			$this->id = (int)$this->conn->lastInsertId();
			$this->username = $username;
			$this->password = $hashedPassword;

			return true;
		} catch (PDOException $e) {
			// Най-честата причина е дублирано потребителско име (UNIQUE)
			$this->error = 'Неуспешна регистрация. Възможно е потребителското име да е заето.';
			return false;
		}
	}

	/**
	 * Вход в системата.
	 * - Проверява дали има потребител с това име и дали паролата съвпада.
	 * - Връща true при успех, false при грешка.
	 */
	public function login($username, $password): bool
	{
		$this->error = '';

		$username = $this->sanitizeInput($username);
		$password = $this->sanitizeInput($password);

		if ($username === '' || $password === '') {
			$this->error = 'Моля, попълнете потребителско име и парола.';
			return false;
		}

		if (mb_strlen($username) < 3 || mb_strlen($password) < 4) {
			$this->error = 'Невалидни данни за вход.';
			return false;
		}

		try {
			$sql = 'SELECT id, username, password FROM users WHERE username = :username LIMIT 1';
			$stmt = $this->conn->prepare($sql);
			$stmt->execute([':username' => $username]);
			$row = $stmt->fetch();

			if (!$row) {
				$this->error = 'Грешно потребителско име или парола.';
				return false;
			}

			$hashedPassword = $this->hashPassword($password);
			if ($row['password'] !== $hashedPassword) {
				$this->error = 'Грешно потребителско име или парола.';
				return false;
			}

			$this->id = (int)$row['id'];
			$this->username = (string)$row['username'];
			$this->password = (string)$row['password'];

			return true;
		} catch (PDOException $e) {
			$this->error = 'Грешка при вход. Опитайте отново.';
			return false;
		}
	}

	/**
	 * Премахва празни символи и прави базова защита за показване в HTML.
	 */
	private function sanitizeInput($value): string
	{
		$value = (string)$value;
		$value = trim($value);
		return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
	}

	/**
	 * Прост хеш на парола (за учебни цели).
	 */
	private function hashPassword(string $password): string
	{
		return md5($password);
	}
}

