// probe 535 -- binary <
package main

//go:noinline
func op_535(a int64, b int64) bool {
	return a < b
}

var ga int64
var gb int64
var sink interface{}

func main() {
	sink = op_535(ga, gb)
	_ = sink
}
