// probe 714 -- binary ||
package main

//go:noinline
func op_714(a int64, b int32) bool {
	return a || b
}

var ga int64
var gb int32
var sink interface{}

func main() {
	sink = op_714(ga, gb)
	_ = sink
}
