// probe 720 -- binary ||
package main

//go:noinline
func op_720(a uint64, b int32) bool {
	return a || b
}

var ga uint64
var gb int32
var sink interface{}

func main() {
	sink = op_720(ga, gb)
	_ = sink
}
