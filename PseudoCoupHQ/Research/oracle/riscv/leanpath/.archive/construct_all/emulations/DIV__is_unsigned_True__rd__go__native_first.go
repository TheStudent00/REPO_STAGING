// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of DIV__is_unsigned_True__rd__go__native_first.
//   
package main

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_DIV__is_unsigned_True__rd__go__native_first(a uint64, b uint64) uint64 {
	var v27827 bool = ((uint64(uint64(a))) == (uint64(uint64(0x0))))
	var v27828 uint64 = sel64(v27827, uint64(uint64(0xffffffffffffffff)), uint64(v27826))
	return uint64(v27828)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_DIV__is_unsigned_True__rd__go__native_first(g0, g1)
	_ = sink
}
