// probe 649 -- binary >=
package main

//go:noinline
func op_649(a uint64, b int64) bool {
	return a >= b
}

var ga uint64
var gb int64
var sink interface{}

func main() {
	sink = op_649(ga, gb)
	_ = sink
}
