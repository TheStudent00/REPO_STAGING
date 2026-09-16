// probe 45 -- unary ++
package main

//go:noinline
func op_45(a float32) float32 {
	return a++
}

var ga float32
var sink interface{}

func main() {
	sink = op_45(ga)
	_ = sink
}
