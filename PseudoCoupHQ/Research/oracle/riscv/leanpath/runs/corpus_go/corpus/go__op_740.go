// probe 740 -- binary ||
package main

//go:noinline
func op_740(a bool, b uint64) bool {
	return a || b
}

var ga bool
var gb uint64
var sink interface{}

func main() {
	sink = op_740(ga, gb)
	_ = sink
}
