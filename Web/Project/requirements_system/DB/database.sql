-- Препоръка: За учебен проект е най-лесно да изтрием и създадем наново базата.
-- Така се избягват проблеми с остатъчни таблици/ключове при повторен импорт.
DROP DATABASE IF EXISTS requirements_system;

-- Създаване на база данни (UTF-8 за български текст)
CREATE DATABASE requirements_system
	CHARACTER SET utf8mb4
	COLLATE utf8mb4_unicode_ci;

USE requirements_system;

-- Изтриване на таблици (за да може файлът да се пуска многократно)
-- Понякога при частичен импорт/стари таблици може да има остатъчни FK зависимости.
-- Затова временно изключваме FK проверките по време на DROP.
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS indicators;
DROP TABLE IF EXISTS requirements;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS users;

SET FOREIGN_KEY_CHECKS = 1;

-- 1) users
CREATE TABLE users (
	id INT AUTO_INCREMENT PRIMARY KEY, -- Уникален идентификатор на потребител
	username VARCHAR(50) NOT NULL, -- Потребителско име (уникално)
	password VARCHAR(255) NOT NULL, -- Парола
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Дата и час на регистрация

	UNIQUE KEY uq_users_username (username)
) ENGINE=InnoDB
	DEFAULT CHARSET=utf8mb4
	COLLATE=utf8mb4_unicode_ci;

-- 2) projects
CREATE TABLE projects (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(150) NOT NULL COMMENT 'Име на проекта',
	description TEXT NULL COMMENT 'Описание на проекта',
	created_by INT NOT NULL COMMENT 'Създаден от (users.id)',
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата и час на създаване',

	KEY idx_projects_created_by (created_by),
	CONSTRAINT fk_projects_created_by
		FOREIGN KEY (created_by) REFERENCES users(id)
		ON UPDATE CASCADE
		ON DELETE RESTRICT
) ENGINE=InnoDB
	DEFAULT CHARSET=utf8mb4
	COLLATE=utf8mb4_unicode_ci;

-- 3) requirements
-- Забележка: Таблица requirements представлява функционалности (и поддържа йерархия).
CREATE TABLE requirements (
	id INT AUTO_INCREMENT PRIMARY KEY, -- Уникален идентификатор на изискване
	project_id INT NOT NULL COMMENT 'Проект, към който принадлежи функционалността',
	parent_id INT NULL COMMENT 'Родителска функционалност (йерархия)',
	title VARCHAR(200) NOT NULL, -- Заглавие на изискването
	description TEXT NOT NULL, -- Описание на изискването
	type ENUM('functional', 'nonfunctional') NOT NULL, -- Тип
	status ENUM('not_started','in_progress','done') NOT NULL DEFAULT 'not_started' COMMENT 'Статус на функционалността',
	priority TINYINT NOT NULL, -- Приоритет (1-5)
	importance TINYINT NOT NULL, -- Важност (1-5)
	layer ENUM('client', 'routing', 'business', 'database', 'install_test') NOT NULL, -- Слой
	component VARCHAR(120) NULL, -- Компонент
	assigned_to VARCHAR(50) NULL, -- Възложено на
	image_path VARCHAR(255) NULL COMMENT 'Път до качена снимка',
	created_by INT NOT NULL, -- Създадено от (ID на потребител)
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Дата и час на създаване

	KEY idx_requirements_project_id (project_id),
	KEY idx_requirements_parent_id (parent_id),
	KEY idx_requirements_created_by (created_by),
	CONSTRAINT fk_requirements_project
		FOREIGN KEY (project_id) REFERENCES projects(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	CONSTRAINT fk_requirements_parent
		FOREIGN KEY (parent_id) REFERENCES requirements(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	CONSTRAINT fk_requirements_created_by
		FOREIGN KEY (created_by) REFERENCES users(id)
		ON UPDATE CASCADE
		ON DELETE RESTRICT
) ENGINE=InnoDB
	DEFAULT CHARSET=utf8mb4
	COLLATE=utf8mb4_unicode_ci;

-- 4) indicators
-- (само за нефункционални изисквания, но таблицата е обща)
CREATE TABLE indicators (
	id INT AUTO_INCREMENT PRIMARY KEY, -- Уникален идентификатор на индикатор
	requirement_id INT NOT NULL, -- ID на изискване
	name VARCHAR(120) NOT NULL, -- Име на индикатора
	description TEXT NOT NULL, -- Описание на индикатора
	unit VARCHAR(50) NULL, -- Единица
	value VARCHAR(100) NULL, -- Стойност

	KEY idx_indicators_requirement_id (requirement_id),
	CONSTRAINT fk_indicators_requirement
		FOREIGN KEY (requirement_id) REFERENCES requirements(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE
) ENGINE=InnoDB
	DEFAULT CHARSET=utf8mb4
	COLLATE=utf8mb4_unicode_ci;

-- 5) tags
CREATE TABLE tags (
	id INT AUTO_INCREMENT PRIMARY KEY, -- Уникален идентификатор на таг
	requirement_id INT NOT NULL, -- ID на изискване
	tag VARCHAR(60) NOT NULL, -- Таг

	KEY idx_tags_requirement_id (requirement_id),
	CONSTRAINT fk_tags_requirement
		FOREIGN KEY (requirement_id) REFERENCES requirements(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE
) ENGINE=InnoDB
	DEFAULT CHARSET=utf8mb4
	COLLATE=utf8mb4_unicode_ci;
