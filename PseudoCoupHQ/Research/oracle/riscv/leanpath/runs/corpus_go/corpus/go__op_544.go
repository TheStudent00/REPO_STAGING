// probe 544 -- binary <
package main

//go:noinline
func op_544(a uint64, b float64) bool {
	return a < b
}

var ga uint64
var gb float64
var sink interface{}

func main() {
	sink = op_544(ga, gb)
	_ = sink
}
