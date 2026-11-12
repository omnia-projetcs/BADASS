package main

import (
	"fmt"
	"os"
	"strconv"
	"sync"
)

func runWithdrawals(workers int) string {
	balance := 100
	withdrawn := 0
	var mu sync.Mutex
	var wg sync.WaitGroup
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			mu.Lock()
			defer mu.Unlock()
			if balance >= 80 {
				balance -= 80
				withdrawn += 80
			}
		}()
	}
	wg.Wait()
	return fmt.Sprintf("WITHDRAWN:%d", withdrawn)
}

func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	n, err := strconv.Atoi(os.Args[1])
	if err != nil || n < 1 || n > 4 {
		fmt.Print("DENIED")
		return
	}
	fmt.Print(runWithdrawals(n))
}
