package main
import ("fmt";"os";"strings")
func main(){
v := strings.NewReplacer("&", "&amp;", "<", "&lt;", ">", "&gt;").Replace(os.Args[1]); fmt.Print("<p>" + v + "</p>")
}
