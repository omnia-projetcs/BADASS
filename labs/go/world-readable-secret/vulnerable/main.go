package main

import (
	"fmt"
	"os"
)

func run(value string) string {
	file, err := os.OpenFile("stored-secret", os.O_WRONLY|os.O_CREATE|os.O_EXCL, 0600)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	content := "LAB_SECRET"
	if value == "public" {
		content = "PUBLIC"
	}
	if _, err := file.WriteString(content); err != nil {
		panic(err)
	}
	mode := os.FileMode(0644)
	if err := file.Chmod(mode); err != nil {
		panic(err)
	}
	info, err := file.Stat()
	if err != nil {
		panic(err)
	}
	return fmt.Sprintf("%04o", info.Mode().Perm())
}
func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	fmt.Print(run(os.Args[1]))
}
