// probe 451 -- binary ^
package main

//go:noinline
func op_451(a bool, b int64) bool {
	return a ^ b
}

var ga bool
var gb int64
var sink interface{}

func main() {
	sink = op_451(ga, gb)
	_ = sink
}
