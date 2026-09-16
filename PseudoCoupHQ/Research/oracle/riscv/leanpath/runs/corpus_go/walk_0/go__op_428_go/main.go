// probe 428 -- binary ^
package main

//go:noinline
func op_428(a int64, b uint64) int64 {
	return a ^ b
}

var ga int64
var gb uint64
var sink interface{}

func main() {
	sink = op_428(ga, gb)
	_ = sink
}
