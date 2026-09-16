// probe 403 -- binary |
package main

//go:noinline
func op_403(a float32, b int64) float32 {
	return a | b
}

var ga float32
var gb int64
var sink interface{}

func main() {
	sink = op_403(ga, gb)
	_ = sink
}
