// probe 686 -- binary &&
package main

//go:noinline
func op_686(a uint64, b uint64) bool {
	return a && b
}

var ga uint64
var gb uint64
var sink interface{}

func main() {
	sink = op_686(ga, gb)
	_ = sink
}
