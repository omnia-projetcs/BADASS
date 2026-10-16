package main

import (
	"fmt"
	"os"
)

func run(value string) string {
	records := map[string]string{"alice": "ALICE_DATA", "bob": "BOB_PRIVATE"}
	data, found := records[value]
	if !found {
		return "NOT_FOUND"
	}
	if value != "alice" {
		return "DENIED"
	}
	return data
}
func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	fmt.Print(run(os.Args[1]))
}
