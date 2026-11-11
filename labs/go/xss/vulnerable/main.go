package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	fmt.Print("<p>" + os.Args[1] + "</p>")
}
