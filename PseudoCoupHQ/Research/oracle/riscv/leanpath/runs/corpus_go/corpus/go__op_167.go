// probe 167 -- binary %
package main

//go:noinline
func op_167(a bool, b bool) bool {
	return a % b
}

var ga bool
var gb bool
var sink interface{}

func main() {
	sink = op_167(ga, gb)
	_ = sink
}
