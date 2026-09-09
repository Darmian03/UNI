USE requirements_system;

INSERT INTO projects (id, name, description, created_by, created_at) VALUES
(1, 'Requirements Management System', 'Web system for managing functional and non-functional requirements.', 1, '2026-02-01 10:00:00'),
(2, 'Smart Library Portal', 'Portal for library services, reservations, and notifications.', 3, '2026-02-01 10:30:00');

INSERT INTO requirements (id, project_id, parent_id, title, description, type, status, priority, importance, layer, component, assigned_to, image_path, created_by, created_at) VALUES
(1, 1, NULL, 'User Management', 'Manage users, roles, and authentication.', 'functional', 'in_progress', 1, 5, 'business', 'users', 'milen', NULL, 1, '2026-02-01 11:00:00'),
(2, 1, 1, 'User Registration', 'Allow visitors to register with username and password.', 'functional', 'done', 2, 5, 'client', 'register', 'milen', NULL, 1, '2026-02-01 11:10:00'),
(3, 1, 1, 'User Login', 'Authenticate users and create sessions.', 'functional', 'in_progress', 1, 5, 'business', 'auth', 'milen', NULL, 1, '2026-02-01 11:20:00'),
(4, 1, NULL, 'Project Management', 'Create, edit, and list projects.', 'functional', 'in_progress', 2, 4, 'business', 'projects', 'milen', NULL, 3, '2026-02-01 11:30:00'),
(5, 1, 4, 'Create Project', 'Provide UI and validation to create projects.', 'functional', 'done', 2, 4, 'client', 'projects', 'milen', NULL, 3, '2026-02-01 11:40:00'),
(6, 1, 4, 'Edit Project', 'Allow editing project details.', 'functional', 'not_started', 3, 4, 'client', 'projects', 'milen', NULL, 3, '2026-02-01 11:50:00'),
(7, 1, NULL, 'Requirements Catalog', 'Manage functional and non-functional requirements.', 'functional', 'in_progress', 1, 5, 'business', 'requirements', 'milen', NULL, 1, '2026-02-01 12:00:00'),
(8, 1, 7, 'Add Requirement', 'Add new requirement with priority and layer.', 'functional', 'done', 1, 5, 'client', 'requirements', 'milen', NULL, 1, '2026-02-01 12:10:00'),
(9, 1, 7, 'Edit Requirement', 'Edit existing requirement details.', 'functional', 'in_progress', 1, 5, 'client', 'requirements', 'milen', NULL, 1, '2026-02-01 12:20:00'),
(10, 1, NULL, 'Performance', 'System must respond within acceptable time.', 'nonfunctional', 'in_progress', 1, 5, 'business', 'performance', 'milen', NULL, 1, '2026-02-01 12:30:00'),
(11, 1, NULL, 'Security', 'Protect data and restrict access.', 'nonfunctional', 'not_started', 1, 5, 'business', 'security', 'milen', NULL, 1, '2026-02-01 12:40:00'),
(12, 2, NULL, 'Book Search', 'Search books by title, author, and ISBN.', 'functional', 'in_progress', 2, 4, 'client', 'search', 'milen', NULL, 3, '2026-02-01 13:00:00'),
(13, 2, 12, 'Advanced Filters', 'Filter by genre, year, and availability.', 'functional', 'not_started', 3, 3, 'client', 'search', 'milen', NULL, 3, '2026-02-01 13:10:00'),
(14, 2, NULL, 'Availability SLA', 'System uptime requirements for public portal.', 'nonfunctional', 'in_progress', 2, 4, 'install_test', 'sla', 'milen', NULL, 3, '2026-02-01 13:20:00');

INSERT INTO indicators (id, requirement_id, name, description, unit, value) VALUES
(1, 10, 'Response Time', 'Average response time for requirement listing.', 'ms', '<= 800'),
(2, 10, 'Peak Load', 'Requests per minute without degradation.', 'rpm', '>= 1200'),
(3, 11, 'Password Hashing', 'Use bcrypt for password storage.', 'security', 'bcrypt'),
(4, 14, 'Uptime', 'Monthly availability of the portal.', '%', '>= 99.5');

INSERT INTO tags (id, requirement_id, tag) VALUES
(1, 2, 'auth'),
(2, 3, 'auth'),
(3, 7, 'core'),
(4, 8, 'ui'),
(5, 9, 'ui'),
(6, 10, 'performance'),
(7, 11, 'security'),
(8, 12, 'search'),
(9, 13, 'filters'),
(10, 14, 'sla');
