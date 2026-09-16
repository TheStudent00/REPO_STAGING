// probe 481 -- binary ==
package main

//go:noinline
func op_481(a float64, b int64) bool {
	return a == b
}

var ga float64
var gb int64
var sink interface{}

func main() {
	sink = op_481(ga, gb)
	_ = sink
}
