// probe 675 -- binary &&
package main

//go:noinline
func op_675(a int32, b float32) bool {
	return a && b
}

var ga int32
var gb float32
var sink interface{}

func main() {
	sink = op_675(ga, gb)
	_ = sink
}
