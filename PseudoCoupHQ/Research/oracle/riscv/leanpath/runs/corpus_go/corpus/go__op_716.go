// probe 716 -- binary ||
package main

//go:noinline
func op_716(a int64, b uint64) bool {
	return a || b
}

var ga int64
var gb uint64
var sink interface{}

func main() {
	sink = op_716(ga, gb)
	_ = sink
}
