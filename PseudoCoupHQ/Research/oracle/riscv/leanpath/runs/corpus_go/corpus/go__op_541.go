// probe 541 -- binary <
package main

//go:noinline
func op_541(a uint64, b int64) bool {
	return a < b
}

var ga uint64
var gb int64
var sink interface{}

func main() {
	sink = op_541(ga, gb)
	_ = sink
}
