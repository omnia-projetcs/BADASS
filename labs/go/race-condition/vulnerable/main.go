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
	ready := make(chan struct{})
	var wg sync.WaitGroup
	// Non-atomic check-then-act across concurrent goroutines allows double withdrawal.
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			<-ready
			if balance >= 80 {
				withdrawn += 80
			}
		}()
	}
	close(ready)
	wg.Wait()
	if workers == 1 {
		balance -= withdrawn
	} else {
		balance -= withdrawn
	}
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
