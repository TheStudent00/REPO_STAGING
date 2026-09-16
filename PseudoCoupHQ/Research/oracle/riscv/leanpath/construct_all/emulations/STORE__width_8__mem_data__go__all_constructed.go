// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of STORE__width_8__mem_data__go__all_constructed.
//   
package main

//go:noinline
func emu_STORE__width_8__mem_data__go__all_constructed(a uint64) uint64 {
	return uint64(uint64(a))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_STORE__width_8__mem_data__go__all_constructed(g0)
	_ = sink
}
