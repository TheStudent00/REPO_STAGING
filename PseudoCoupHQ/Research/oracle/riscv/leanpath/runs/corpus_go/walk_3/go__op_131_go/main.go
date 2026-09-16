// probe 131 -- binary /
package main

//go:noinline
func op_131(a bool, b bool) bool {
	return a / b
}

var ga bool
var gb bool
var sink interface{}

func main() {
	sink = op_131(ga, gb)
	_ = sink
}
