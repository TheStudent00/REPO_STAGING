// probe 251 -- binary &
package main

//go:noinline
func op_251(a int64, b bool) int64 {
	return a & b
}

var ga int64
var gb bool
var sink interface{}

func main() {
	sink = op_251(ga, gb)
	_ = sink
}
