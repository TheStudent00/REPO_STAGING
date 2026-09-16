// probe 574 -- binary <=
package main

//go:noinline
func op_574(a int64, b float64) bool {
	return a <= b
}

var ga int64
var gb float64
var sink interface{}

func main() {
	sink = op_574(ga, gb)
	_ = sink
}
