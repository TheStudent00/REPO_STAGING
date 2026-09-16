// probe 314 -- binary +
package main

//go:noinline
func op_314(a int32, b uint64) int32 {
	return a + b
}

var ga int32
var gb uint64
var sink interface{}

func main() {
	sink = op_314(ga, gb)
	_ = sink
}
