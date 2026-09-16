// probe 696 -- binary &&
package main

//go:noinline
func op_696(a float64, b int32) bool {
	return a && b
}

var ga float64
var gb int32
var sink interface{}

func main() {
	sink = op_696(ga, gb)
	_ = sink
}
