// probe 6 -- unary -
package main

//go:noinline
func emu_neg_gpr_one_32__primitive__go(a int32) int32 {
	return -a
}

var ga int32
var sink interface{}

func main() {
	sink = emu_neg_gpr_one_32__primitive__go(ga)
	_ = sink
}
