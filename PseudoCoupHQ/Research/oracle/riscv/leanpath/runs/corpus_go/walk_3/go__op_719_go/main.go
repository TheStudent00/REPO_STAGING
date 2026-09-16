// probe 719 -- binary ||
package main

//go:noinline
func op_719(a int64, b bool) bool {
	return a || b
}

var ga int64
var gb bool
var sink interface{}

func main() {
	sink = op_719(ga, gb)
	_ = sink
}
