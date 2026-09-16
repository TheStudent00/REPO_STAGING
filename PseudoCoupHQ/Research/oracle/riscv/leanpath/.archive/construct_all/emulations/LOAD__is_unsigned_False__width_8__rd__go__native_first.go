// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of LOAD__is_unsigned_False__width_8__rd__go__native_first.
//   
package main

//go:noinline
func emu_LOAD__is_unsigned_False__width_8__rd__go__native_first(a uint64) uint64 {
	return uint64(uint64(a))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_LOAD__is_unsigned_False__width_8__rd__go__native_first(g0)
	_ = sink
}
