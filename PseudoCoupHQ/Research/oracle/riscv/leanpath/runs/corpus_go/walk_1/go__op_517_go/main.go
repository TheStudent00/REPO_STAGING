// probe 517 -- binary !=
package main

//go:noinline
func op_517(a float64, b int64) bool {
	return a != b
}

var ga float64
var gb int64
var sink interface{}

func main() {
	sink = op_517(ga, gb)
	_ = sink
}
