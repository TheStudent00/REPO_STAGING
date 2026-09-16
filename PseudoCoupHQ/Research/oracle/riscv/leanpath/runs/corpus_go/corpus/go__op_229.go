// probe 229 -- binary >>
package main

//go:noinline
func op_229(a float64, b int64) float64 {
	return a >> b
}

var ga float64
var gb int64
var sink interface{}

func main() {
	sink = op_229(ga, gb)
	_ = sink
}
