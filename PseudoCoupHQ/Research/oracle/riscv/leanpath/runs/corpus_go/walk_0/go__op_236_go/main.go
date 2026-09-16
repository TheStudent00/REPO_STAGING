// probe 236 -- binary >>
package main

//go:noinline
func op_236(a bool, b uint64) bool {
	return a >> b
}

var ga bool
var gb uint64
var sink interface{}

func main() {
	sink = op_236(ga, gb)
	_ = sink
}
