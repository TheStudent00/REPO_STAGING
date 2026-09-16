// probe 670 -- binary >=
package main

//go:noinline
func op_670(a bool, b float64) bool {
	return a >= b
}

var ga bool
var gb float64
var sink interface{}

func main() {
	sink = op_670(ga, gb)
	_ = sink
}
