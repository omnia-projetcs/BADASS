package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	v := strings.NewReplacer("&", "&amp;", "<", "&lt;", ">", "&gt;").Replace(os.Args[1])
	fmt.Print("<p>" + v + "</p>")
}
