package main

import (
	"fmt"
	"os"
	"os/exec"
)

func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	data, err := exec.Command("/bin/sh", "-c", "printf %s "+os.Args[1]).Output()
	if err != nil {
		panic(err)
	}
	fmt.Print(string(data))
}
