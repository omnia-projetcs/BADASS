package main
import ("fmt";"os")
func main(){
data, err := os.ReadFile("public/" + os.Args[1]); if err != nil {panic(err)}; fmt.Print(string(data))
}
