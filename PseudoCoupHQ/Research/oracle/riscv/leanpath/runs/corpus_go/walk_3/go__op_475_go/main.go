// probe 475 -- binary ==
package main

//go:noinline
func op_475(a float32, b int64) bool {
	return a == b
}

var ga float32
var gb int64
var sink interface{}

func main() {
	sink = op_475(ga, gb)
	_ = sink
}
