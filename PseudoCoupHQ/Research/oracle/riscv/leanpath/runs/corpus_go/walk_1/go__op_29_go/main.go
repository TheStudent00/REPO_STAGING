// probe 29 -- unary *
package main

//go:noinline
func op_29(a bool) bool {
	return *a
}

var ga bool
var sink interface{}

func main() {
	sink = op_29(ga)
	_ = sink
}
