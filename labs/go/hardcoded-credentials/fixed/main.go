package main

import (
	"crypto/subtle"
	"fmt"
	"os"
)

func run(value string) string {
	expected := os.Getenv("BADASS_ADMIN_PASSWORD")
	if expected != "" && subtle.ConstantTimeCompare([]byte(value), []byte(expected)) == 1 {
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
