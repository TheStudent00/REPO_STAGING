// probe 198 -- binary <<
package main

//go:noinline
func op_198(a bool, b int32) bool {
	return a << b
}

var ga bool
var gb int32
var sink interface{}

func main() {
	sink = op_198(ga, gb)
	_ = sink
}
