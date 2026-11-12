package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type ProfileUpdateRequest struct {
	Name string `json:"name"`
}

func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	var req ProfileUpdateRequest
	if err := json.Unmarshal([]byte(os.Args[1]), &req); err != nil {
		fmt.Print("DENIED")
		return
	}
	name := "Alice"
	if req.Name != "" {
		name = req.Name
	}
	fmt.Printf("%s:user", name)
}
