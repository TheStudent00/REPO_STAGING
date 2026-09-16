// probe 646 -- binary >=
package main

//go:noinline
func op_646(a int64, b float64) bool {
	return a >= b
}

var ga int64
var gb float64
var sink interface{}

func main() {
	sink = op_646(ga, gb)
	_ = sink
}
