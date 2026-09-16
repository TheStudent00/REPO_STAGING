// probe 577 -- binary <=
package main

//go:noinline
func op_577(a uint64, b int64) bool {
	return a <= b
}

var ga uint64
var gb int64
var sink interface{}

func main() {
	sink = op_577(ga, gb)
	_ = sink
}
