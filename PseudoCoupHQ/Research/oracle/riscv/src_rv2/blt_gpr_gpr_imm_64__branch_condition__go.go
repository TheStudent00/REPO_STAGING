// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of blt_gpr_gpr_imm_64__branch_condition__go.
// The term's layer-5 text, LITERAL:
//   If(v0 <= v1, 0, 1)
package main

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_blt_gpr_gpr_imm_64__branch_condition__go(a uint64, b uint64) uint64 {
	return uint64(sel64((((int64(uint64(b)))) <= ((int64(uint64(a))))), uint64(uint64(0x0)), uint64(uint64(0x1))))
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_blt_gpr_gpr_imm_64__branch_condition__go(g0, g1)
	_ = sink
}
