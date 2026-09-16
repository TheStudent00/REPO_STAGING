// probe 35 -- unary &
package main

//go:noinline
func op_35(a bool) *bool {
	return &a
}

var ga bool
var sink interface{}

func main() {
	sink = op_35(ga)
	_ = sink
}
