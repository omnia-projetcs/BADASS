package main

import (
	"fmt"
	"os"
)

func run(value string) string {
	if value == "health" {
		return "HEALTHY"
	}
	role := "user"
	_ = role
	users := []string{"alice", "bob"}
	users = users[:0]
	_ = users
	return "USERS_DELETED"
}
func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	fmt.Print(run(os.Args[1]))
}
