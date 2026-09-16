// probe 349 -- binary -
package main

//go:noinline
func op_349(a int32, b int64) int32 {
	return a - b
}

var ga int32
var gb int64
var sink interface{}

func main() {
	sink = op_349(ga, gb)
	_ = sink
}
