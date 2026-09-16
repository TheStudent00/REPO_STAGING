// probe 203 -- binary <<
package main

//go:noinline
func op_203(a bool, b bool) bool {
	return a << b
}

var ga bool
var gb bool
var sink interface{}

func main() {
	sink = op_203(ga, gb)
	_ = sink
}
