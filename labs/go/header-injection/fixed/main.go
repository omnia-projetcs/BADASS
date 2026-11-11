package main

import (
	"fmt"
	"os"
	"strings"
)

func run(value string) string {
	if strings.ContainsAny(value, "
") {
		return "DENIED"
	}
	return "X-User: " + value + "

BODY"
}
func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	fmt.Print(run(os.Args[1]))
}
