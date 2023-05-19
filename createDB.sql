DROP DATABASE IF EXISTS chat;
CREATE DATABASE IF NOT EXISTS chat;

USE chat;

DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT UNIQUE,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    status VARCHAR(255) default 'Offline',
    salt VARCHAR(255) default "",
    publicKey VARCHAR(255) default "",
    privateKey VARCHAR(255) default "",
    PRIMARY KEY (id)
);

INSERT INTO users (username, password, salt) VALUES ("klaviam", "d54b67f8282f0105d16dd318c42a8758062c4f7cb1325e5d36f68847778d7ba9dfcaed4e44026faa627a221ca28290e99ea406f132668e68ec02f4a18749a8c4", "1353c9e922154806984fea20b08de222");
INSERT INTO users (username, password, salt) VALUES ("boxer", "72279d6985c106e6d47114da1850fbd3245f7835ddf4269a16bae8dea25e61a14d37d51dda0c4fb8ee0f147629a5c35d94cc7b8ea33bb77a5f42791397482a80", "c4877cf34c8944ebb76a3a47eb8a37a9");
INSERT INTO users (username, password, salt) VALUES ("adam", "46538e879207be291b22f4d0018bd3471ae7c98436d46a6fb270dabc4e819f2b41d2913f9089779d7bf2f60b8699e3d4cd5efc2249fafc89d5c75c785ae312c5", "2e5710a4c40b493e8a89fdaf74c3a471");
INSERT INTO users (username, password, salt) VALUES ("dog", "77dbb6eef5b4ca7fd9d2094446d7cff61652a565b17858dd2f0d29daea97f002200b722c229439e3154911500e9ab10f79c7982a5aae0cde90f679f304a79cb5", "9bb6e678ed9549309889a37ebd4ca995");
