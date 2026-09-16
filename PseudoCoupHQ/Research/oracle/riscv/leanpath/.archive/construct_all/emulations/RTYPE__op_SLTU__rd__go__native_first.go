// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of RTYPE__op_SLTU__rd__go__native_first.
//   
package main

func sel32(c bool, x uint32, y uint32) uint32 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_RTYPE__op_SLTU__rd__go__native_first(a uint64, b uint64) uint64 {
	var v0 bool = (((uint64(uint64(b)))) <= ((uint64(uint64(a)))))
	var v1 uint32 = sel32(v0, uint32(uint32(0x0)), uint32(uint32(0x1)))
	var v2 uint64 = (uint64(((uint64(uint64(0x0))) << 1) | (uint64(v1))))
	return uint64(v2)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_RTYPE__op_SLTU__rd__go__native_first(g0, g1)
	_ = sink
}
