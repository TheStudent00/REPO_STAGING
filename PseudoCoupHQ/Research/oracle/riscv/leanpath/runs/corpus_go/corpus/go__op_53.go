// probe 53 -- unary --
package main

//go:noinline
func op_53(a bool) bool {
	return a--
}

var ga bool
var sink interface{}

func main() {
	sink = op_53(ga)
	_ = sink
}
