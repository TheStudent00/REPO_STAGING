// probe 174 -- binary <<
package main

//go:noinline
func op_174(a int64, b int32) int64 {
	return a << b
}

var ga int64
var gb int32
var sink interface{}

func main() {
	sink = op_174(ga, gb)
	_ = sink
}
