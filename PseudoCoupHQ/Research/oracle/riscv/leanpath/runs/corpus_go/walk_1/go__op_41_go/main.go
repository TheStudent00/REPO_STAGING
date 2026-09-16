// probe 41 -- unary <-
package main

//go:noinline
func op_41(a bool) bool {
	return <-a
}

var ga bool
var sink interface{}

func main() {
	sink = op_41(ga)
	_ = sink
}
