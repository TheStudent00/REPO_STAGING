// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of SHIFTIOP__op_SRLI__rd__go__native_first.
//   
package main

//go:noinline
func emu_SHIFTIOP__op_SRLI__rd__go__native_first(a uint64, b uint8) uint64 {
	var v0 uint32 = ((uint32((uint32(b)) >> 0)) & uint32(0x3f))
	var v1 uint64 = (uint64(((uint64(uint64(0x0))) << 6) | (uint64(v0))))
	var v2 uint64 = (uint64((uint64(uint64(a))) >> ((uint64(v1)) & uint64(0x3f))))
	return uint64(v2)
}

var g0 uint64
var g1 uint8
var sink interface{}

func main() {
	sink = emu_SHIFTIOP__op_SRLI__rd__go__native_first(g0, g1)
	_ = sink
}
