// probe 322 -- binary +
package main

//go:noinline
func op_322(a int64, b float64) int64 {
	return a + b
}

var ga int64
var gb float64
var sink interface{}

func main() {
	sink = op_322(ga, gb)
	_ = sink
}
