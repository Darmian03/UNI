<?php
class Database
{
	// Данни за връзка към MySQL
	private string $host = 'localhost';
	private string $dbName = 'requirements_system';
	private string $username = 'root';
	private string $password = '';
	private string $charset = 'utf8mb4';

	// Обектът PDO се пази тук, за да не създаваме нова връзка всеки път
	private ?PDO $connection = null;

	// Връща PDO връзка. Ако още няма връзка, я създава.
	public function getConnection(): PDO
	{
		if ($this->connection !== null) {
			return $this->connection;
		}

		// DSN (Data Source Name) описва към коя база се свързваме
		$dsn = "mysql:host={$this->host};dbname={$this->dbName};charset={$this->charset}";

		// Опции за PDO - държим ги прости и полезни за дебъг
		$options = [
			PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, // показва грешки като изключения
			PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, // резултатите да са асоциативни масиви
			PDO::ATTR_EMULATE_PREPARES => false, // използва реални prepared statements
		];

		try {
			$this->connection = new PDO($dsn, $this->username, $this->password, $options);
		} catch (PDOException $e) {
			die('Грешка при връзка с базата данни: ' . $e->getMessage());
		}

		return $this->connection;
	}
}

