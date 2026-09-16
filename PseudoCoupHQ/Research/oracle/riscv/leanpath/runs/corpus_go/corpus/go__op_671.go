// probe 671 -- binary >=
package main

//go:noinline
func op_671(a bool, b bool) bool {
	return a >= b
}

var ga bool
var gb bool
var sink interface{}

func main() {
	sink = op_671(ga, gb)
	_ = sink
}
