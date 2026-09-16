// probe 715 -- binary ||
package main

//go:noinline
func op_715(a int64, b int64) bool {
	return a || b
}

var ga int64
var gb int64
var sink interface{}

func main() {
	sink = op_715(ga, gb)
	_ = sink
}
