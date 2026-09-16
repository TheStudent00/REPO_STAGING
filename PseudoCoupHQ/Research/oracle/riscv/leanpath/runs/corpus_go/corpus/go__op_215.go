// probe 215 -- binary >>
package main

//go:noinline
func op_215(a int64, b bool) int64 {
	return a >> b
}

var ga int64
var gb bool
var sink interface{}

func main() {
	sink = op_215(ga, gb)
	_ = sink
}
