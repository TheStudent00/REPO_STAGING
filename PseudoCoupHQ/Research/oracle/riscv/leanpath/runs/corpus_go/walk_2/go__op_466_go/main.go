// probe 466 -- binary ==
package main

//go:noinline
func op_466(a int64, b float64) bool {
	return a == b
}

var ga int64
var gb float64
var sink interface{}

func main() {
	sink = op_466(ga, gb)
	_ = sink
}
