// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of REM__is_unsigned_True__rd__go__native_first.
//   
package main

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_REM__is_unsigned_True__rd__go__native_first(a uint64, b uint64) uint64 {
	var v27467 bool = ((uint64(uint64(a))) == (uint64(uint64(0x0))))
	var v27468 uint64 = sel64(v27467, uint64(uint64(b)), uint64(v27466))
	return uint64(v27468)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_REM__is_unsigned_True__rd__go__native_first(g0, g1)
	_ = sink
}
