// probe 329 -- binary +
package main

//go:noinline
func op_329(a uint64, b bool) uint64 {
	return a + b
}

var ga uint64
var gb bool
var sink interface{}

func main() {
	sink = op_329(ga, gb)
	_ = sink
}
