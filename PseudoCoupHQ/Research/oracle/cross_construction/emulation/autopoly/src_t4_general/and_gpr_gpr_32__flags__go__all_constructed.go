// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of and_gpr_gpr_32__flags__go__all_constructed.
//   Concat(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)), 0)
package main

//go:noinline
func emu_and_gpr_gpr_32__flags__go__all_constructed(a uint32, b uint32) uint64 {
	var v0 uint32 = uint32(b)
	var v1 uint32 = (uint32(^(uint32(v0))))
	var v2 uint32 = uint32(a)
	var v3 uint32 = (uint32(^(uint32(v2))))
	var v4 uint32 = (uint32((uint32(v3)) | (uint32(v1))))
	var v5 uint32 = (uint32(^(uint32(v4))))
	var v6 uint32 = uint32(0x0)
	var v7 uint32 = v5
	var v8 uint64 = (uint64(((uint64(v7)) << 32) | (uint64(v6))))
	return uint64(v8)
}

var g0 uint32
var g1 uint32
var sink interface{}

func main() {
	sink = emu_and_gpr_gpr_32__flags__go__all_constructed(g0, g1)
	_ = sink
}
