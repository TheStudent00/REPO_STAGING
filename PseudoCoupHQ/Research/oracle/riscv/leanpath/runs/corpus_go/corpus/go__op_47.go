// probe 47 -- unary ++
package main

//go:noinline
func op_47(a bool) bool {
	return a++
}

var ga bool
var sink interface{}

func main() {
	sink = op_47(ga)
	_ = sink
}
