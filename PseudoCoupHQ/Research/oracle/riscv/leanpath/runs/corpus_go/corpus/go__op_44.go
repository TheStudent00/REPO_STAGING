// probe 44 -- unary ++
package main

//go:noinline
func op_44(a uint64) uint64 {
	return a++
}

var ga uint64
var sink interface{}

func main() {
	sink = op_44(ga)
	_ = sink
}
