// probe 569 -- binary <=
package main

//go:noinline
func op_569(a int32, b bool) bool {
	return a <= b
}

var ga int32
var gb bool
var sink interface{}

func main() {
	sink = op_569(ga, gb)
	_ = sink
}
