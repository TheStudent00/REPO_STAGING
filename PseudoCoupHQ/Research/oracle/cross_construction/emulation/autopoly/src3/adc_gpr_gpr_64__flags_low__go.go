// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of adc_gpr_gpr_64__flags_low__go.
// The term's layer-5 text, LITERAL:
//   v0
package main

//go:noinline
func emu_adc_gpr_gpr_64__flags_low__go(a uint64) uint64 {
	return uint64(uint64(a))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_adc_gpr_gpr_64__flags_low__go(g0)
	_ = sink
}
