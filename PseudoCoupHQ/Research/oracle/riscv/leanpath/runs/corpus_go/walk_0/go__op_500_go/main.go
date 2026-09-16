// probe 500 -- binary !=
package main

//go:noinline
func op_500(a int64, b uint64) bool {
	return a != b
}

var ga int64
var gb uint64
var sink interface{}

func main() {
	sink = op_500(ga, gb)
	_ = sink
}
