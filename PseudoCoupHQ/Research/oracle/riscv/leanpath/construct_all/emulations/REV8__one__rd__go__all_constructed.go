// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of REV8__one__rd__go__all_constructed.
//   
package main

//go:noinline
func emu_REV8__one__rd__go__all_constructed(a uint64) uint64 {
	var v0 uint32 = ((uint32((uint64(a)) >> 56)) & uint32(0xff))
	var v1 uint32 = ((uint32((uint64(a)) >> 48)) & uint32(0xff))
	var v2 uint32 = ((uint32((uint64(a)) >> 40)) & uint32(0xff))
	var v3 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0xff))
	var v4 uint32 = ((uint32((uint64(a)) >> 24)) & uint32(0xff))
	var v5 uint32 = ((uint32((uint64(a)) >> 16)) & uint32(0xff))
	var v6 uint32 = ((uint32((uint64(a)) >> 8)) & uint32(0xff))
	var v7 uint32 = ((uint32((uint64(a)) >> 0)) & uint32(0xff))
	var v8 uint32 = v0
	var v9 uint32 = v1
	var v10 uint32 = v2
	var v11 uint32 = v3
	var v12 uint32 = v4
	var v13 uint32 = v5
	var v14 uint32 = v6
	var v15 uint32 = v7
	var v16 uint32 = ((uint32(((uint32(v15)) << 8) | (uint32(v14)))) & uint32(0xffff))
	var v17 uint32 = ((uint32(((uint32(v16)) << 8) | (uint32(v13)))) & uint32(0xffffff))
	var v18 uint32 = (uint32(((uint32(v17)) << 8) | (uint32(v12))))
	var v19 uint64 = ((uint64(((uint64(v18)) << 8) | (uint64(v11)))) & uint64(0xffffffffff))
	var v20 uint64 = ((uint64(((uint64(v19)) << 8) | (uint64(v10)))) & uint64(0xffffffffffff))
	var v21 uint64 = ((uint64(((uint64(v20)) << 8) | (uint64(v9)))) & uint64(0xffffffffffffff))
	var v22 uint64 = (uint64(((uint64(v21)) << 8) | (uint64(v8))))
	return uint64(v22)
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_REV8__one__rd__go__all_constructed(g0)
	_ = sink
}
