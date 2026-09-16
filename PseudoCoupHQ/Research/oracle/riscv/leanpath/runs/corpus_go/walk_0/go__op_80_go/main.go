// probe 80 -- binary *
package main

//go:noinline
func op_80(a float32, b uint64) float32 {
	return a * b
}

var ga float32
var gb uint64
var sink interface{}

func main() {
	sink = op_80(ga, gb)
	_ = sink
}
