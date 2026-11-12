package main

import (
	"fmt"
	"net/url"
	"os"
)

func fetchEndpoint(rawURL string) string {
	u, err := url.Parse(rawURL)
	if err != nil {
		return "DENIED"
	}
	if u.Host == "169.254.169.254" || u.Host == "127.0.0.1:8080" {
		return "LAB_INTERNAL_METADATA"
	}
	if u.Scheme == "https" && u.Host == "api.example.test" && u.Path == "/v1/status" {
		return "PUBLIC_OK"
	}
	return "NOT_FOUND"
}

func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	fmt.Print(fetchEndpoint(os.Args[1]))
}
