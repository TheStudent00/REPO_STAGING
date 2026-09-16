// probe 241 -- binary &
package main

//go:noinline
func op_241(a int32, b int64) int32 {
	return a & b
}

var ga int32
var gb int64
var sink interface{}

func main() {
	sink = op_241(ga, gb)
	_ = sink
}
