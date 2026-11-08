package main

import (
	"fmt"
	"os"
	"strconv"
)

func run(value string) string {
	size, err := strconv.Atoi(value)
	if err != nil || size < 0 {
		panic("Invalid size")
	}
	if size > 100 {
		return "DENIED"
	}
	data := make([]byte, size)
	return strconv.Itoa(len(data))
}
func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	fmt.Print(run(os.Args[1]))
}
