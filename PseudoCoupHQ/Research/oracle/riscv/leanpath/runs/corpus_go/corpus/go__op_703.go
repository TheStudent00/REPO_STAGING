// probe 703 -- binary &&
package main

//go:noinline
func op_703(a bool, b int64) bool {
	return a && b
}

var ga bool
var gb int64
var sink interface{}

func main() {
	sink = op_703(ga, gb)
	_ = sink
}
