package main

import (
	"database/sql"
	"fmt"
	_ "github.com/mattn/go-sqlite3"
	"os"
)

func lookup(value string) error {
	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		return err
	}
	defer db.Close()
	db.SetMaxOpenConns(1)
	_, err = db.Exec("CREATE TABLE users(name TEXT NOT NULL); INSERT INTO users VALUES ('alice'),('admin');")
	if err != nil {
		return err
	}
	rows, err := db.Query("SELECT name FROM users WHERE name = '" + value + "'")
	if err != nil {
		return err
	}
	defer rows.Close()
	for rows.Next() {
		var name string
		if err := rows.Scan(&name); err != nil {
			return err
		}
		fmt.Println(name)
	}
	return rows.Err()
}

func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	if err := lookup(os.Args[1]); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
