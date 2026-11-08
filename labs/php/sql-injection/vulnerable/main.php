<?php
$db = new PDO('sqlite::memory:');
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$db->exec("CREATE TABLE users(name TEXT NOT NULL); INSERT INTO users VALUES ('alice'),('admin');");
$value = $argv[1];
$statement = $db->query("SELECT name FROM users WHERE name = '" . $value . "'");
foreach ($statement->fetchAll(PDO::FETCH_COLUMN) as $name) {
    echo $name, "\n";
}
