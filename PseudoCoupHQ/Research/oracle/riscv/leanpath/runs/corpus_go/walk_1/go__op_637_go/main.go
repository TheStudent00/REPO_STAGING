// probe 637 -- binary >=
package main

//go:noinline
func op_637(a int32, b int64) bool {
	return a >= b
}

var ga int32
var gb int64
var sink interface{}

func main() {
	sink = op_637(ga, gb)
	_ = sink
}
