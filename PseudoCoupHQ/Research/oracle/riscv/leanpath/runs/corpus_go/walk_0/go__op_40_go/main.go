// probe 40 -- unary <-
package main

//go:noinline
func op_40(a float64) float64 {
	return <-a
}

var ga float64
var sink interface{}

func main() {
	sink = op_40(ga)
	_ = sink
}
