// probe 7 -- unary -
package main

//go:noinline
func emu_neg_gpr_one_64__primitive__go(a int64) int64 {
	return -a
}

var ga int64
var sink interface{}

func main() {
	sink = emu_neg_gpr_one_64__primitive__go(ga)
	_ = sink
}
