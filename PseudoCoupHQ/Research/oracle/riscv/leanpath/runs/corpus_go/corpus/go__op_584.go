// probe 584 -- binary <=
package main

//go:noinline
func op_584(a float32, b uint64) bool {
	return a <= b
}

var ga float32
var gb uint64
var sink interface{}

func main() {
	sink = op_584(ga, gb)
	_ = sink
}
