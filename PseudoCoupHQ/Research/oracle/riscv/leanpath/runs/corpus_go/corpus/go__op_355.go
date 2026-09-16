// probe 355 -- binary -
package main

//go:noinline
func op_355(a int64, b int64) int64 {
	return a - b
}

var ga int64
var gb int64
var sink interface{}

func main() {
	sink = op_355(ga, gb)
	_ = sink
}
