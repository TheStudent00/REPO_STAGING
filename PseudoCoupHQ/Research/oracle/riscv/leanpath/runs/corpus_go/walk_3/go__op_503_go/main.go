// probe 503 -- binary !=
package main

//go:noinline
func op_503(a int64, b bool) bool {
	return a != b
}

var ga int64
var gb bool
var sink interface{}

func main() {
	sink = op_503(ga, gb)
	_ = sink
}
