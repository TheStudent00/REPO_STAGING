// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of or_gpr_gpr_32__flags__go__native_first.
//   Concat(Extract(31, 0, v0) | Extract(31, 0, v1), 0)
package main

//go:noinline
func emu_or_gpr_gpr_32__flags__go__native_first(a uint32, b uint32) uint64 {
	var v0 uint32 = uint32(b)
	var v1 uint32 = uint32(a)
	var v2 uint32 = (uint32((uint32(v1)) | (uint32(v0))))
	var v3 uint64 = (uint64(((uint64(v2)) << 32) | (uint64(uint32(0x0)))))
	return uint64(v3)
}

var g0 uint32
var g1 uint32
var sink interface{}

func main() {
	sink = emu_or_gpr_gpr_32__flags__go__native_first(g0, g1)
	_ = sink
}
