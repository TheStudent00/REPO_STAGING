// probe 36 -- unary <-
package main

//go:noinline
func op_36(a int32) int32 {
	return <-a
}

var ga int32
var sink interface{}

func main() {
	sink = op_36(ga)
	_ = sink
}
