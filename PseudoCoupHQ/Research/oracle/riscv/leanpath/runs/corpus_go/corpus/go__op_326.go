// probe 326 -- binary +
package main

//go:noinline
func op_326(a uint64, b uint64) uint64 {
	return a + b
}

var ga uint64
var gb uint64
var sink interface{}

func main() {
	sink = op_326(ga, gb)
	_ = sink
}
