// probe 344 -- binary +
package main

//go:noinline
func op_344(a bool, b uint64) bool {
	return a + b
}

var ga bool
var gb uint64
var sink interface{}

func main() {
	sink = op_344(ga, gb)
	_ = sink
}
