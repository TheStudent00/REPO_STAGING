// probe 704 -- binary &&
package main

//go:noinline
func op_704(a bool, b uint64) bool {
	return a && b
}

var ga bool
var gb uint64
var sink interface{}

func main() {
	sink = op_704(ga, gb)
	_ = sink
}
