// probe 143 -- binary %
package main

//go:noinline
func op_143(a int64, b bool) int64 {
	return a % b
}

var ga int64
var gb bool
var sink interface{}

func main() {
	sink = op_143(ga, gb)
	_ = sink
}
