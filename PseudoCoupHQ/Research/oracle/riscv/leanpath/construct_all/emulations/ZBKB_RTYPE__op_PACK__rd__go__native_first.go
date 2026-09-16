// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ZBKB_RTYPE__op_PACK__rd__go__native_first.
//   
package main

//go:noinline
func emu_ZBKB_RTYPE__op_PACK__rd__go__native_first(a uint32, b uint32) uint64 {
	var v0 uint32 = uint32(b)
	var v1 uint32 = uint32(a)
	var v2 uint64 = (uint64(((uint64(v1)) << 32) | (uint64(v0))))
	return uint64(v2)
}

var g0 uint32
var g1 uint32
var sink interface{}

func main() {
	sink = emu_ZBKB_RTYPE__op_PACK__rd__go__native_first(g0, g1)
	_ = sink
}
