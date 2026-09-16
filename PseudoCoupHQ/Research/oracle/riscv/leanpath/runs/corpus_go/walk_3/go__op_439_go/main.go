// probe 439 -- binary ^
package main

//go:noinline
func op_439(a float32, b int64) float32 {
	return a ^ b
}

var ga float32
var gb int64
var sink interface{}

func main() {
	sink = op_439(ga, gb)
	_ = sink
}
