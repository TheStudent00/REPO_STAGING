// probe 327 -- binary +
package main

//go:noinline
func op_327(a uint64, b float32) uint64 {
	return a + b
}

var ga uint64
var gb float32
var sink interface{}

func main() {
	sink = op_327(ga, gb)
	_ = sink
}
