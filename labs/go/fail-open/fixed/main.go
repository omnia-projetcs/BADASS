package main

import (
	"errors"
	"fmt"
	"os"
)

func run(value string) string {
	lookup := func() (bool, error) {
		if value == "backend-down" {
			return false, errors.New("Authorization unavailable")
		}
		return value == "authorized", nil
	}
	authorized, err := lookup()
	if err != nil {
		return "DENIED"
	}
	if authorized {
		return "ALLOWED"
	}
	return "DENIED"
}
func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	fmt.Print(run(os.Args[1]))
}
