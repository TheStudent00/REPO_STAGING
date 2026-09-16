// probe 222 -- binary >>
package main

//go:noinline
func op_222(a float32, b int32) float32 {
	return a >> b
}

var ga float32
var gb int32
var sink interface{}

func main() {
	sink = op_222(ga, gb)
	_ = sink
}
