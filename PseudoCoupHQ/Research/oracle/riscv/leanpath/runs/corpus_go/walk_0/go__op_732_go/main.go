// probe 732 -- binary ||
package main

//go:noinline
func op_732(a float64, b int32) bool {
	return a || b
}

var ga float64
var gb int32
var sink interface{}

func main() {
	sink = op_732(ga, gb)
	_ = sink
}
