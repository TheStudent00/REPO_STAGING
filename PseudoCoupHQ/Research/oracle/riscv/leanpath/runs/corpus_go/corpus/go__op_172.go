// probe 172 -- binary <<
package main

//go:noinline
func op_172(a int32, b float64) int32 {
	return a << b
}

var ga int32
var gb float64
var sink interface{}

func main() {
	sink = op_172(ga, gb)
	_ = sink
}
