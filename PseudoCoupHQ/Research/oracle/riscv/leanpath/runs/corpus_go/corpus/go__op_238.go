// probe 238 -- binary >>
package main

//go:noinline
func op_238(a bool, b float64) bool {
	return a >> b
}

var ga bool
var gb float64
var sink interface{}

func main() {
	sink = op_238(ga, gb)
	_ = sink
}
