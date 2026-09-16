// probe 539 -- binary <
package main

//go:noinline
func op_539(a int64, b bool) bool {
	return a < b
}

var ga int64
var gb bool
var sink interface{}

func main() {
	sink = op_539(ga, gb)
	_ = sink
}
