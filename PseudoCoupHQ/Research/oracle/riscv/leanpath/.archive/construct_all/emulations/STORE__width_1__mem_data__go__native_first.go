// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of STORE__width_1__mem_data__go__native_first.
//   
package main

//go:noinline
func emu_STORE__width_1__mem_data__go__native_first(a uint8) uint8 {
	var v0 uint32 = uint32(a)
	return uint8(v0)
}

var g0 uint8
var sink interface{}

func main() {
	sink = emu_STORE__width_1__mem_data__go__native_first(g0)
	_ = sink
}
