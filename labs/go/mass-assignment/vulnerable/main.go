package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type Account struct {
	Name string `json:"name"`
	Role string `json:"role"`
}

func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	acc := Account{Name: "Alice", Role: "user"}
	_ = json.Unmarshal([]byte(os.Args[1]), &acc)
	fmt.Printf("%s:%s", acc.Name, acc.Role)
}
