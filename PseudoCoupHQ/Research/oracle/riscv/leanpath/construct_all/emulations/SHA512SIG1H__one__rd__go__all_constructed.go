// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of SHA512SIG1H__one__rd__go__all_constructed.
//   
package main

//go:noinline
func emu_SHA512SIG1H__one__rd__go__all_constructed(a uint64, b uint64) uint64 {
	var v0 uint32 = ((uint32((uint64(a)) >> 6)) & uint32(0x7))
	var v1 uint32 = ((uint32((uint64(b)) >> 29)) & uint32(0x7))
	var v2 uint32 = ((uint32((uint64(a)) >> 19)) & uint32(0x7))
	var v3 uint32 = ((uint32((uint32(v2)) ^ (uint32(v1)))) & uint32(0x7))
	var v4 uint32 = ((uint32((uint32(v3)) ^ (uint32(v0)))) & uint32(0x7))
	var v5 uint32 = ((uint32((uint64(a)) >> 0)) & uint32(0x3ff))
	var v6 uint32 = ((uint32((uint64(b)) >> 32)) & uint32(0x3ff))
	var v7 uint32 = ((uint32((uint64(a)) >> 22)) & uint32(0x3ff))
	var v8 uint32 = ((uint32((uint64(a)) >> 9)) & uint32(0x3ff))
	var v9 uint32 = ((uint32((uint32(v8)) ^ (uint32(v7)))) & uint32(0x3ff))
	var v10 uint32 = ((uint32((uint32(v9)) ^ (uint32(v6)))) & uint32(0x3ff))
	var v11 uint32 = ((uint32((uint32(v10)) ^ (uint32(v5)))) & uint32(0x3ff))
	var v12 uint32 = ((uint32((uint64(b)) >> 42)) & uint32(0x3fffff))
	var v13 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x3fffff))
	var v14 uint32 = ((uint32((uint64(a)) >> 19)) & uint32(0x3fffff))
	var v15 uint32 = ((uint32((uint64(a)) >> 10)) & uint32(0x3fffff))
	var v16 uint32 = ((uint32((uint64(b)) >> 0)) & uint32(0x3fffff))
	var v17 uint32 = ((uint32((uint32(v16)) ^ (uint32(v15)))) & uint32(0x3fffff))
	var v18 uint32 = ((uint32((uint32(v17)) ^ (uint32(v14)))) & uint32(0x3fffff))
	var v19 uint32 = ((uint32((uint32(v18)) ^ (uint32(v13)))) & uint32(0x3fffff))
	var v20 uint32 = ((uint32((uint32(v19)) ^ (uint32(v12)))) & uint32(0x3fffff))
	var v21 uint32 = ((uint32((uint64(a)) >> 54)) & uint32(0x3ff))
	var v22 uint32 = ((uint32((uint64(a)) >> 41)) & uint32(0x3ff))
	var v23 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x3ff))
	var v24 uint32 = ((uint32((uint64(b)) >> 22)) & uint32(0x3ff))
	var v25 uint32 = ((uint32((uint32(v24)) ^ (uint32(v23)))) & uint32(0x3ff))
	var v26 uint32 = ((uint32((uint32(v25)) ^ (uint32(v22)))) & uint32(0x3ff))
	var v27 uint32 = ((uint32((uint32(v26)) ^ (uint32(v21)))) & uint32(0x3ff))
	var v28 uint32 = ((uint32((uint64(a)) >> 51)) & uint32(0x1fff))
	var v29 uint32 = ((uint32((uint64(a)) >> 42)) & uint32(0x1fff))
	var v30 uint32 = ((uint32((uint64(b)) >> 32)) & uint32(0x1fff))
	var v31 uint32 = ((uint32((uint32(v30)) ^ (uint32(v29)))) & uint32(0x1fff))
	var v32 uint32 = ((uint32((uint32(v31)) ^ (uint32(v28)))) & uint32(0x1fff))
	var v33 uint32 = ((uint32((uint64(a)) >> 55)) & uint32(0x3f))
	var v34 uint32 = ((uint32((uint64(b)) >> 45)) & uint32(0x3f))
	var v35 uint32 = ((uint32((uint32(v34)) ^ (uint32(v33)))) & uint32(0x3f))
	var v36 uint32 = v4
	var v37 uint32 = v11
	var v38 uint32 = v20
	var v39 uint32 = v27
	var v40 uint32 = v32
	var v41 uint32 = v35
	var v42 uint32 = ((uint32(((uint32(v41)) << 13) | (uint32(v40)))) & uint32(0x7ffff))
	var v43 uint32 = ((uint32(((uint32(v42)) << 10) | (uint32(v39)))) & uint32(0x1fffffff))
	var v44 uint64 = ((uint64(((uint64(v43)) << 22) | (uint64(v38)))) & uint64(0x7ffffffffffff))
	var v45 uint64 = ((uint64(((uint64(v44)) << 10) | (uint64(v37)))) & uint64(0x1fffffffffffffff))
	var v46 uint64 = (uint64(((uint64(v45)) << 3) | (uint64(v36))))
	return uint64(v46)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_SHA512SIG1H__one__rd__go__all_constructed(g0, g1)
	_ = sink
}
