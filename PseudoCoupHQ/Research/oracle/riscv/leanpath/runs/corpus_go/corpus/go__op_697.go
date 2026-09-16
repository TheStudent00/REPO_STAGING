// probe 697 -- binary &&
package main

//go:noinline
func op_697(a float64, b int64) bool {
	return a && b
}

var ga float64
var gb int64
var sink interface{}

func main() {
	sink = op_697(ga, gb)
	_ = sink
}
