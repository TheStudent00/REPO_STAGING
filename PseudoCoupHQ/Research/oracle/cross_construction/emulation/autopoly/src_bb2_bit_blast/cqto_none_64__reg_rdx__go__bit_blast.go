// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of cqto_none_64__reg_rdx__go__bit_blast.
//   v0 >> 63
package main

//go:noinline
func emu_cqto_none_64__reg_rdx__go__bit_blast(a uint64) uint64 {
	var x0_63 uint64 = (uint64(a) >> 63) & 1
	var w0 uint64 = (x0_63 << 0)
	var w1 uint64 = w0 | (x0_63 << 1)
	var w2 uint64 = w1 | (x0_63 << 2)
	var w3 uint64 = w2 | (x0_63 << 3)
	var w4 uint64 = w3 | (x0_63 << 4)
	var w5 uint64 = w4 | (x0_63 << 5)
	var w6 uint64 = w5 | (x0_63 << 6)
	var w7 uint64 = w6 | (x0_63 << 7)
	var w8 uint64 = w7 | (x0_63 << 8)
	var w9 uint64 = w8 | (x0_63 << 9)
	var w10 uint64 = w9 | (x0_63 << 10)
	var w11 uint64 = w10 | (x0_63 << 11)
	var w12 uint64 = w11 | (x0_63 << 12)
	var w13 uint64 = w12 | (x0_63 << 13)
	var w14 uint64 = w13 | (x0_63 << 14)
	var w15 uint64 = w14 | (x0_63 << 15)
	var w16 uint64 = w15 | (x0_63 << 16)
	var w17 uint64 = w16 | (x0_63 << 17)
	var w18 uint64 = w17 | (x0_63 << 18)
	var w19 uint64 = w18 | (x0_63 << 19)
	var w20 uint64 = w19 | (x0_63 << 20)
	var w21 uint64 = w20 | (x0_63 << 21)
	var w22 uint64 = w21 | (x0_63 << 22)
	var w23 uint64 = w22 | (x0_63 << 23)
	var w24 uint64 = w23 | (x0_63 << 24)
	var w25 uint64 = w24 | (x0_63 << 25)
	var w26 uint64 = w25 | (x0_63 << 26)
	var w27 uint64 = w26 | (x0_63 << 27)
	var w28 uint64 = w27 | (x0_63 << 28)
	var w29 uint64 = w28 | (x0_63 << 29)
	var w30 uint64 = w29 | (x0_63 << 30)
	var w31 uint64 = w30 | (x0_63 << 31)
	var w32 uint64 = w31 | (x0_63 << 32)
	var w33 uint64 = w32 | (x0_63 << 33)
	var w34 uint64 = w33 | (x0_63 << 34)
	var w35 uint64 = w34 | (x0_63 << 35)
	var w36 uint64 = w35 | (x0_63 << 36)
	var w37 uint64 = w36 | (x0_63 << 37)
	var w38 uint64 = w37 | (x0_63 << 38)
	var w39 uint64 = w38 | (x0_63 << 39)
	var w40 uint64 = w39 | (x0_63 << 40)
	var w41 uint64 = w40 | (x0_63 << 41)
	var w42 uint64 = w41 | (x0_63 << 42)
	var w43 uint64 = w42 | (x0_63 << 43)
	var w44 uint64 = w43 | (x0_63 << 44)
	var w45 uint64 = w44 | (x0_63 << 45)
	var w46 uint64 = w45 | (x0_63 << 46)
	var w47 uint64 = w46 | (x0_63 << 47)
	var w48 uint64 = w47 | (x0_63 << 48)
	var w49 uint64 = w48 | (x0_63 << 49)
	var w50 uint64 = w49 | (x0_63 << 50)
	var w51 uint64 = w50 | (x0_63 << 51)
	var w52 uint64 = w51 | (x0_63 << 52)
	var w53 uint64 = w52 | (x0_63 << 53)
	var w54 uint64 = w53 | (x0_63 << 54)
	var w55 uint64 = w54 | (x0_63 << 55)
	var w56 uint64 = w55 | (x0_63 << 56)
	var w57 uint64 = w56 | (x0_63 << 57)
	var w58 uint64 = w57 | (x0_63 << 58)
	var w59 uint64 = w58 | (x0_63 << 59)
	var w60 uint64 = w59 | (x0_63 << 60)
	var w61 uint64 = w60 | (x0_63 << 61)
	var w62 uint64 = w61 | (x0_63 << 62)
	var w63 uint64 = w62 | (x0_63 << 63)
	return uint64(w63)
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_cqto_none_64__reg_rdx__go__bit_blast(g0)
	_ = sink
}
