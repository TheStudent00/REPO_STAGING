// probe 265 -- binary &
package main

//go:noinline
func op_265(a float64, b int64) float64 {
	return a & b
}

var ga float64
var gb int64
var sink interface{}

func main() {
	sink = op_265(ga, gb)
	_ = sink
}
