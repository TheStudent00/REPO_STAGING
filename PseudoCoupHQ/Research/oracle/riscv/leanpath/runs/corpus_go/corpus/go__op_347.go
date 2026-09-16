// probe 347 -- binary +
package main

//go:noinline
func op_347(a bool, b bool) bool {
	return a + b
}

var ga bool
var gb bool
var sink interface{}

func main() {
	sink = op_347(ga, gb)
	_ = sink
}
