package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	data, err := os.ReadFile("public/" + os.Args[1])
	if err != nil {
		panic(err)
	}
	fmt.Print(string(data))
}
