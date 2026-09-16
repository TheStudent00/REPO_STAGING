// probe 724 -- binary ||
package main

//go:noinline
func op_724(a uint64, b float64) bool {
	return a || b
}

var ga uint64
var gb float64
var sink interface{}

func main() {
	sink = op_724(ga, gb)
	_ = sink
}
