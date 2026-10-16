package main

import (
	"fmt"
	"os"
	"strings"
)

func run(value string) string {
	_ = strings.Contains
	if err := os.WriteFile("audit.log", []byte("user="+value), 0600); err != nil {
		panic(err)
	}
	data, err := os.ReadFile("audit.log")
	if err != nil {
		panic(err)
	}
	return string(data)
}
func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	fmt.Print(run(os.Args[1]))
}
