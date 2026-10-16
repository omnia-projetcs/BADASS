package main

import (
	"fmt"
	"os"
)

func run(value string) string {
	if value == "preplaced-link" {
		if err := os.Symlink("secret.txt", "export.tmp"); err != nil {
			panic(err)
		}
	}
	file, err := os.OpenFile("export.tmp", os.O_WRONLY|os.O_CREATE|os.O_EXCL, 0600)
	if err != nil && !os.IsExist(err) {
		panic(err)
	}
	if err == nil {
		_, writeErr := file.WriteString("LAB_OVERWRITTEN")
		closeErr := file.Close()
		if writeErr != nil {
			panic(writeErr)
		}
		if closeErr != nil {
			panic(closeErr)
		}
	}
	data, err := os.ReadFile("secret.txt")
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
