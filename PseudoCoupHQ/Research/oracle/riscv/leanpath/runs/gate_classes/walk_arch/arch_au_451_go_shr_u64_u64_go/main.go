// probe 218 -- binary >>
package main

//go:noinline
func op_218(a uint64, b uint64) uint64 {
	return a >> b
}

var ga uint64
var gb uint64
var sink interface{}

func main() {
	sink = op_218(ga, gb)
	_ = sink
}
