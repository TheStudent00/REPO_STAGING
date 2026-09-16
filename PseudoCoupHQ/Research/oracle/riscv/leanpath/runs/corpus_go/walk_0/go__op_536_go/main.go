// probe 536 -- binary <
package main

//go:noinline
func op_536(a int64, b uint64) bool {
	return a < b
}

var ga int64
var gb uint64
var sink interface{}

func main() {
	sink = op_536(ga, gb)
	_ = sink
}
