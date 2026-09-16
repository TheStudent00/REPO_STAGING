// probe 515 -- binary !=
package main

//go:noinline
func op_515(a float32, b bool) bool {
	return a != b
}

var ga float32
var gb bool
var sink interface{}

func main() {
	sink = op_515(ga, gb)
	_ = sink
}
