// probe 73 -- binary *
package main

//go:noinline
func op_73(a uint64, b int64) uint64 {
	return a * b
}

var ga uint64
var gb int64
var sink interface{}

func main() {
	sink = op_73(ga, gb)
	_ = sink
}
