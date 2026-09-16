// probe 620 -- binary >
package main

//go:noinline
func op_620(a float32, b uint64) bool {
	return a > b
}

var ga float32
var gb uint64
var sink interface{}

func main() {
	sink = op_620(ga, gb)
	_ = sink
}
