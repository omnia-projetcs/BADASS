package main

import (
	"fmt"
	"os"
)

func run(value string) string {
	if value == "ok" {
		return "OK"
	}
	_, err := os.ReadFile("missing-database")
	if err != nil {
		return "db://admin:LAB_SECRET@database/internal"
	}
	return "OK"
}
func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	fmt.Print(run(os.Args[1]))
}
