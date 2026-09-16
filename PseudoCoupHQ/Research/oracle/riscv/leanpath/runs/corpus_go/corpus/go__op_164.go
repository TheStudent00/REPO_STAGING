// probe 164 -- binary %
package main

//go:noinline
func op_164(a bool, b uint64) bool {
	return a % b
}

var ga bool
var gb uint64
var sink interface{}

func main() {
	sink = op_164(ga, gb)
	_ = sink
}
