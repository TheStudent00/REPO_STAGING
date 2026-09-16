// probe 410 -- binary |
package main

//go:noinline
func op_410(a float64, b uint64) float64 {
	return a | b
}

var ga float64
var gb uint64
var sink interface{}

func main() {
	sink = op_410(ga, gb)
	_ = sink
}
