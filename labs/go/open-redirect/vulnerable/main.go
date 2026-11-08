package main

import (
	"fmt"
	"os"
)

func run(value string) string {
	return "Location: " + value
}
func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	fmt.Print(run(os.Args[1]))
}
