// probe 731 -- binary ||
package main

//go:noinline
func op_731(a float32, b bool) bool {
	return a || b
}

var ga float32
var gb bool
var sink interface{}

func main() {
	sink = op_731(ga, gb)
	_ = sink
}
