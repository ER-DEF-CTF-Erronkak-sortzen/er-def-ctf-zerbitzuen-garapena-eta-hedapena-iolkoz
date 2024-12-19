CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    secret_key TEXT NOT NULL
);

INSERT INTO users (username, password, role, secret_key) VALUES
("admin", "5f4dcc3b5aa765d61d8327deb882cf99", "admin", "supersecretkey"),
("user", "ee11cbb19052e40b07aac0ca060c23ee", "normal", "userkey");
