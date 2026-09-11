// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of cmp_imm_gpr_64__flags_high__go.
// The term's layer-5 text, LITERAL:
//   v0
package main

//go:noinline
func emu_cmp_imm_gpr_64__flags_high__go(a uint64) uint64 {
	return uint64(uint64(a))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_cmp_imm_gpr_64__flags_high__go(g0)
	_ = sink
}
