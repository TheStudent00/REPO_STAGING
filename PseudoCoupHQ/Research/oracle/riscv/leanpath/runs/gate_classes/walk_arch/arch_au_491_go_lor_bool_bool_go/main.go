// probe 743 -- binary ||
package main

//go:noinline
func op_743(a bool, b bool) bool {
	return a || b
}

var ga bool
var gb bool
var sink interface{}

func main() {
	sink = op_743(ga, gb)
	_ = sink
}
