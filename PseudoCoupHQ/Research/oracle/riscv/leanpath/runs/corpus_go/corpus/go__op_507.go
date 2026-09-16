// probe 507 -- binary !=
package main

//go:noinline
func op_507(a uint64, b float32) bool {
	return a != b
}

var ga uint64
var gb float32
var sink interface{}

func main() {
	sink = op_507(ga, gb)
	_ = sink
}
