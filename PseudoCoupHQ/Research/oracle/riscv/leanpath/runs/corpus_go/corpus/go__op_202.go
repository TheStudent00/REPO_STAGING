// probe 202 -- binary <<
package main

//go:noinline
func op_202(a bool, b float64) bool {
	return a << b
}

var ga bool
var gb float64
var sink interface{}

func main() {
	sink = op_202(ga, gb)
	_ = sink
}
