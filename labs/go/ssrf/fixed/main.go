package main

import (
	"fmt"
	"net/url"
	"os"
)

func fetchEndpoint(rawURL string) string {
	u, err := url.Parse(rawURL)
	if err != nil || u.Scheme != "https" || u.Host != "api.example.test" || u.Path != "/v1/status" || u.User != nil {
		return "DENIED"
	}
	return "PUBLIC_OK"
}

func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	fmt.Print(fetchEndpoint(os.Args[1]))
}
