// probe 39 -- unary <-
package main

//go:noinline
func op_39(a float32) float32 {
	return <-a
}

var ga float32
var sink interface{}

func main() {
	sink = op_39(ga)
	_ = sink
}
