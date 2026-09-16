// probe 575 -- binary <=
package main

//go:noinline
func op_575(a int64, b bool) bool {
	return a <= b
}

var ga int64
var gb bool
var sink interface{}

func main() {
	sink = op_575(ga, gb)
	_ = sink
}
