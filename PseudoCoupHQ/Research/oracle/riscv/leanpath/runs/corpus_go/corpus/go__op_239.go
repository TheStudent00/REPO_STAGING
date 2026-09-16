// probe 239 -- binary >>
package main

//go:noinline
func op_239(a bool, b bool) bool {
	return a >> b
}

var ga bool
var gb bool
var sink interface{}

func main() {
	sink = op_239(ga, gb)
	_ = sink
}
