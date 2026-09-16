// probe 397 -- binary |
package main

//go:noinline
func op_397(a uint64, b int64) uint64 {
	return a | b
}

var ga uint64
var gb int64
var sink interface{}

func main() {
	sink = op_397(ga, gb)
	_ = sink
}
