// probe 653 -- binary >=
package main

//go:noinline
func op_653(a uint64, b bool) bool {
	return a >= b
}

var ga uint64
var gb bool
var sink interface{}

func main() {
	sink = op_653(ga, gb)
	_ = sink
}
