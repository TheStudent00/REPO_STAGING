// probe 388 -- binary |
package main

//go:noinline
func op_388(a int32, b float64) int32 {
	return a | b
}

var ga int32
var gb float64
var sink interface{}

func main() {
	sink = op_388(ga, gb)
	_ = sink
}
