// probe 728 -- binary ||
package main

//go:noinline
func op_728(a float32, b uint64) bool {
	return a || b
}

var ga float32
var gb uint64
var sink interface{}

func main() {
	sink = op_728(ga, gb)
	_ = sink
}
