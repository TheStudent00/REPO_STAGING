// probe 695 -- binary &&
package main

//go:noinline
func op_695(a float32, b bool) bool {
	return a && b
}

var ga float32
var gb bool
var sink interface{}

func main() {
	sink = op_695(ga, gb)
	_ = sink
}
