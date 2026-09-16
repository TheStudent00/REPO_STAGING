// probe 352 -- binary -
package main

//go:noinline
func op_352(a int32, b float64) int32 {
	return a - b
}

var ga int32
var gb float64
var sink interface{}

func main() {
	sink = op_352(ga, gb)
	_ = sink
}
