// probe 301 -- binary &^
package main

//go:noinline
func op_301(a float64, b int64) float64 {
	return a &^ b
}

var ga float64
var gb int64
var sink interface{}

func main() {
	sink = op_301(ga, gb)
	_ = sink
}
