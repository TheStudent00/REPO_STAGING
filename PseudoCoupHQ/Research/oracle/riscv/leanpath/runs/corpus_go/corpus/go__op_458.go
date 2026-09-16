// probe 458 -- binary ==
package main

//go:noinline
func op_458(a int32, b uint64) bool {
	return a == b
}

var ga int32
var gb uint64
var sink interface{}

func main() {
	sink = op_458(ga, gb)
	_ = sink
}
