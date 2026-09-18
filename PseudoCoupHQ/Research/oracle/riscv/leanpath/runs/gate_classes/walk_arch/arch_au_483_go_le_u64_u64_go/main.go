// probe 578 -- binary <=
package main

//go:noinline
func op_578(a uint64, b uint64) bool {
	return a <= b
}

var ga uint64
var gb uint64
var sink interface{}

func main() {
	sink = op_578(ga, gb)
	_ = sink
}
