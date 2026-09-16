// probe 148 -- binary %
package main

//go:noinline
func op_148(a uint64, b float64) uint64 {
	return a % b
}

var ga uint64
var gb float64
var sink interface{}

func main() {
	sink = op_148(ga, gb)
	_ = sink
}
