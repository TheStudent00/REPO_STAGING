// probe 247 -- binary &
package main

//go:noinline
func emu_and_gpr_gpr_64__primitive__go(a int64, b int64) int64 {
	return a & b
}

var ga int64
var gb int64
var sink interface{}

func main() {
	sink = emu_and_gpr_gpr_64__primitive__go(ga, gb)
	_ = sink
}
