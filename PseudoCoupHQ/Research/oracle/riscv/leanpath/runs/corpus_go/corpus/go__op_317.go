// probe 317 -- binary +
package main

//go:noinline
func op_317(a int32, b bool) int32 {
	return a + b
}

var ga int32
var gb bool
var sink interface{}

func main() {
	sink = op_317(ga, gb)
	_ = sink
}
