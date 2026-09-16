// probe 446 -- binary ^
package main

//go:noinline
func op_446(a float64, b uint64) float64 {
	return a ^ b
}

var ga float64
var gb uint64
var sink interface{}

func main() {
	sink = op_446(ga, gb)
	_ = sink
}
