// probe 632 -- binary >
package main

//go:noinline
func op_632(a bool, b uint64) bool {
	return a > b
}

var ga bool
var gb uint64
var sink interface{}

func main() {
	sink = op_632(ga, gb)
	_ = sink
}
