// probe 348 -- binary -
package main

//go:noinline
func emu_sub_gpr_gpr_32__primitive__go(a int32, b int32) int32 {
	return a - b
}

var ga int32
var gb int32
var sink interface{}

func main() {
	sink = emu_sub_gpr_gpr_32__primitive__go(ga, gb)
	_ = sink
}
