// probe 693 -- binary &&
package main

//go:noinline
func op_693(a float32, b float32) bool {
	return a && b
}

var ga float32
var gb float32
var sink interface{}

func main() {
	sink = op_693(ga, gb)
	_ = sink
}
