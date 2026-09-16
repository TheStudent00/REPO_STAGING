// probe 38 -- unary <-
package main

//go:noinline
func op_38(a uint64) uint64 {
	return <-a
}

var ga uint64
var sink interface{}

func main() {
	sink = op_38(ga)
	_ = sink
}
