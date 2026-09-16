// probe 137 -- binary %
package main

//go:noinline
func op_137(a int32, b bool) int32 {
	return a % b
}

var ga int32
var gb bool
var sink interface{}

func main() {
	sink = op_137(ga, gb)
	_ = sink
}
