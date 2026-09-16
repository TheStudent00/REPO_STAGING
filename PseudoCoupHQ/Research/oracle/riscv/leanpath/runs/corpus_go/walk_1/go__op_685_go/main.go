// probe 685 -- binary &&
package main

//go:noinline
func op_685(a uint64, b int64) bool {
	return a && b
}

var ga uint64
var gb int64
var sink interface{}

func main() {
	sink = op_685(ga, gb)
	_ = sink
}
