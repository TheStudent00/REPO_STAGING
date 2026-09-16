// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of LOAD__is_unsigned_True__width_1__rd__go__native_first.
//   
package main

//go:noinline
func emu_LOAD__is_unsigned_True__width_1__rd__go__native_first(a uint8) uint64 {
	var v0 uint32 = uint32(a)
	var v1 uint64 = (uint64(((uint64(uint64(0x0))) << 8) | (uint64(v0))))
	return uint64(v1)
}

var g0 uint8
var sink interface{}

func main() {
	sink = emu_LOAD__is_unsigned_True__width_1__rd__go__native_first(g0)
	_ = sink
}
