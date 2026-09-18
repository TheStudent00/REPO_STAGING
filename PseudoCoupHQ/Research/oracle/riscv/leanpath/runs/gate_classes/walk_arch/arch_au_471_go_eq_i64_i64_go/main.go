// probe 463 -- binary ==
package main

//go:noinline
func op_463(a int64, b int64) bool {
	return a == b
}

var ga int64
var gb int64
var sink interface{}

func main() {
	sink = op_463(ga, gb)
	_ = sink
}
