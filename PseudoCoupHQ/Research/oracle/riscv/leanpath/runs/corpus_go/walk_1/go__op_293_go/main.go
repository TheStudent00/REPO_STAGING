// probe 293 -- binary &^
package main

//go:noinline
func op_293(a uint64, b bool) uint64 {
	return a &^ b
}

var ga uint64
var gb bool
var sink interface{}

func main() {
	sink = op_293(ga, gb)
	_ = sink
}
