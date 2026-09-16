// probe 79 -- binary *
package main

//go:noinline
func op_79(a float32, b int64) float32 {
	return a * b
}

var ga float32
var gb int64
var sink interface{}

func main() {
	sink = op_79(ga, gb)
	_ = sink
}
