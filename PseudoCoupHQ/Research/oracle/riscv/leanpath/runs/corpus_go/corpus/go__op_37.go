// probe 37 -- unary <-
package main

//go:noinline
func op_37(a int64) int64 {
	return <-a
}

var ga int64
var sink interface{}

func main() {
	sink = op_37(ga)
	_ = sink
}
