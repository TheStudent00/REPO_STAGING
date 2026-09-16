// probe 162 -- binary %
package main

//go:noinline
func op_162(a bool, b int32) bool {
	return a % b
}

var ga bool
var gb int32
var sink interface{}

func main() {
	sink = op_162(ga, gb)
	_ = sink
}
