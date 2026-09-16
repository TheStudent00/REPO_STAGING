// probe 155 -- binary %
package main

//go:noinline
func op_155(a float32, b bool) float32 {
	return a % b
}

var ga float32
var gb bool
var sink interface{}

func main() {
	sink = op_155(ga, gb)
	_ = sink
}
