// probe 226 -- binary >>
package main

//go:noinline
func op_226(a float32, b float64) float32 {
	return a >> b
}

var ga float32
var gb float64
var sink interface{}

func main() {
	sink = op_226(ga, gb)
	_ = sink
}
