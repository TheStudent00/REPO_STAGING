// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ZBB_RTYPE__op_ORN__rd__go__all_constructed.
//   
package main

//go:noinline
func emu_ZBB_RTYPE__op_ORN__rd__go__all_constructed(a uint64, b uint64) uint64 {
	var v0 uint64 = (uint64(^(uint64(uint64(b)))))
	var v1 uint64 = (uint64((uint64(v0)) | (uint64(uint64(a)))))
	return uint64(v1)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_ZBB_RTYPE__op_ORN__rd__go__all_constructed(g0, g1)
	_ = sink
}
