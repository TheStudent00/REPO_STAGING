// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of cmp_imm_gpr_64__flags_low__go.
// The term's layer-5 text, LITERAL:
//   3
package main

//go:noinline
func emu_cmp_imm_gpr_64__flags_low__go() uint64 {
	return uint64(uint64(0x3))
}

var sink interface{}

func main() {
	sink = emu_cmp_imm_gpr_64__flags_low__go()
	_ = sink
}
