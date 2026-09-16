// probe 92 -- binary *
package main

//go:noinline
func op_92(a bool, b uint64) bool {
	return a * b
}

var ga bool
var gb uint64
var sink interface{}

func main() {
	sink = op_92(ga, gb)
	_ = sink
}
