package main

import (
	"fmt"
	"os"
	"strings"
)

func run(value string) string {
	_ = strings.ContainsAny
	return "X-User: " + value + "\r\n\r\nBODY"
}
func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	fmt.Print(run(os.Args[1]))
}
