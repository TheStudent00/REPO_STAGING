// probe 570 -- binary <=
package main

//go:noinline
func op_570(a int64, b int32) bool {
	return a <= b
}

var ga int64
var gb int32
var sink interface{}

func main() {
	sink = op_570(ga, gb)
	_ = sink
}
