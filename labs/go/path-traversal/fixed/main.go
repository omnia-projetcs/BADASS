package main
import ("fmt";"os")
func main(){
if os.Args[1] != "welcome.txt" {fmt.Print("DENIED"); return}; data, err := os.ReadFile("public/welcome.txt"); if err != nil {panic(err)}; fmt.Print(string(data))
}
