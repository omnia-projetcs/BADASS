package main

import (
	"fmt"
	"os"
)

func run(value string) string {
	expected := os.Getenv("BADASS_ADMIN_PASSWORD")
	if expected != "" && value == expected {
		return "ADMIN"
	}
	return "DENIED"
}
func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	fmt.Print(run(os.Args[1]))
}
