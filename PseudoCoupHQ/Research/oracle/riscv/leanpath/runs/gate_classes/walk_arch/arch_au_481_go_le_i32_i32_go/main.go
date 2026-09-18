// probe 564 -- binary <=
package main

//go:noinline
func op_564(a int32, b int32) bool {
	return a <= b
}

var ga int32
var gb int32
var sink interface{}

func main() {
	sink = op_564(ga, gb)
	_ = sink
}
