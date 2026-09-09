// probe 17 -- unary !
package main

//go:noinline
func emu_xor_imm_gpr_32__primitive__go(a bool) bool {
	return !a
}

var ga bool
var sink interface{}

func main() {
	sink = emu_xor_imm_gpr_32__primitive__go(ga)
	_ = sink
}
