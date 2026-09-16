// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ZBS_RTYPE__op_BEXT__rd__go__native_first.
//   
package main

func sel32(c bool, x uint32, y uint32) uint32 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_ZBS_RTYPE__op_BEXT__rd__go__native_first(a uint64, b uint8) uint64 {
	var v0 uint64 = (uint64(^(uint64(uint64(a)))))
	var v1 uint32 = ((uint32((uint32(b)) >> 0)) & uint32(0x3f))
	var v2 uint64 = (uint64(((uint64(uint64(0x0))) << 6) | (uint64(v1))))
	var v3 uint64 = (uint64((uint64(uint64(0x1))) << ((uint64(v2)) & uint64(0x3f))))
	var v4 uint64 = (uint64(^(uint64(v3))))
	var v5 uint64 = (uint64((uint64(v4)) | (uint64(v0))))
	var v6 uint64 = (uint64(^(uint64(v5))))
	var v7 bool = ((uint64(v6)) == (uint64(uint64(0x0))))
	var v8 uint32 = sel32(v7, uint32(uint32(0x0)), uint32(uint32(0x1)))
	var v9 uint64 = (uint64(((uint64(uint64(0x0))) << 1) | (uint64(v8))))
	return uint64(v9)
}

var g0 uint64
var g1 uint8
var sink interface{}

func main() {
	sink = emu_ZBS_RTYPE__op_BEXT__rd__go__native_first(g0, g1)
	_ = sink
}
