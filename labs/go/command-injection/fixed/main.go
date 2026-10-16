package main
import ("fmt";"os";"os/exec")
func main(){
data, err := exec.Command("/usr/bin/printf", "%s", os.Args[1]).Output(); if err != nil {panic(err)}; fmt.Print(string(data))
}
