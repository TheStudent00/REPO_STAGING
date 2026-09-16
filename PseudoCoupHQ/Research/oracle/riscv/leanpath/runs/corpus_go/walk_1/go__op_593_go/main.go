// probe 593 -- binary <=
package main

//go:noinline
func op_593(a float64, b bool) bool {
	return a <= b
}

var ga float64
var gb bool
var sink interface{}

func main() {
	sink = op_593(ga, gb)
	_ = sink
}
