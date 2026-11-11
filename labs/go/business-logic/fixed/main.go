package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func run(value string) string {
	if strings.HasPrefix(value, "-0") || strings.HasPrefix(value, "+") {
		return "DENIED"
	}
	quantity, err := strconv.Atoi(value)
	if err != nil || quantity < 1 || quantity > 100 {
		return "DENIED"
	}
	return strconv.Itoa(1000 - quantity*10)
}
func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	fmt.Print(run(os.Args[1]))
}
