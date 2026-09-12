// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of punpckldq_mem_xmm_128__reg_xmm0_high__go__bit_blast.
//   Concat(Extract(63, 32, v0), Extract(63, 32, v1))
package main

import "math"

//go:noinline
func emu_punpckldq_mem_xmm_128__reg_xmm0_high__go__bit_blast(a uint64, b float64) float64 {
	var x1_32 uint64 = (uint64(b) >> 32) & 1
	var x1_33 uint64 = (uint64(b) >> 33) & 1
	var x1_34 uint64 = (uint64(b) >> 34) & 1
	var x1_35 uint64 = (uint64(b) >> 35) & 1
	var x1_36 uint64 = (uint64(b) >> 36) & 1
	var x1_37 uint64 = (uint64(b) >> 37) & 1
	var x1_38 uint64 = (uint64(b) >> 38) & 1
	var x1_39 uint64 = (uint64(b) >> 39) & 1
	var x1_40 uint64 = (uint64(b) >> 40) & 1
	var x1_41 uint64 = (uint64(b) >> 41) & 1
	var x1_42 uint64 = (uint64(b) >> 42) & 1
	var x1_43 uint64 = (uint64(b) >> 43) & 1
	var x1_44 uint64 = (uint64(b) >> 44) & 1
	var x1_45 uint64 = (uint64(b) >> 45) & 1
	var x1_46 uint64 = (uint64(b) >> 46) & 1
	var x1_47 uint64 = (uint64(b) >> 47) & 1
	var x1_48 uint64 = (uint64(b) >> 48) & 1
	var x1_49 uint64 = (uint64(b) >> 49) & 1
	var x1_50 uint64 = (uint64(b) >> 50) & 1
	var x1_51 uint64 = (uint64(b) >> 51) & 1
	var x1_52 uint64 = (uint64(b) >> 52) & 1
	var x1_53 uint64 = (uint64(b) >> 53) & 1
	var x1_54 uint64 = (uint64(b) >> 54) & 1
	var x1_55 uint64 = (uint64(b) >> 55) & 1
	var x1_56 uint64 = (uint64(b) >> 56) & 1
	var x1_57 uint64 = (uint64(b) >> 57) & 1
	var x1_58 uint64 = (uint64(b) >> 58) & 1
	var x1_59 uint64 = (uint64(b) >> 59) & 1
	var x1_60 uint64 = (uint64(b) >> 60) & 1
	var x1_61 uint64 = (uint64(b) >> 61) & 1
	var x1_62 uint64 = (uint64(b) >> 62) & 1
	var x1_63 uint64 = (uint64(b) >> 63) & 1
	var x0_32 uint64 = (uint64(a) >> 32) & 1
	var x0_33 uint64 = (uint64(a) >> 33) & 1
	var x0_34 uint64 = (uint64(a) >> 34) & 1
	var x0_35 uint64 = (uint64(a) >> 35) & 1
	var x0_36 uint64 = (uint64(a) >> 36) & 1
	var x0_37 uint64 = (uint64(a) >> 37) & 1
	var x0_38 uint64 = (uint64(a) >> 38) & 1
	var x0_39 uint64 = (uint64(a) >> 39) & 1
	var x0_40 uint64 = (uint64(a) >> 40) & 1
	var x0_41 uint64 = (uint64(a) >> 41) & 1
	var x0_42 uint64 = (uint64(a) >> 42) & 1
	var x0_43 uint64 = (uint64(a) >> 43) & 1
	var x0_44 uint64 = (uint64(a) >> 44) & 1
	var x0_45 uint64 = (uint64(a) >> 45) & 1
	var x0_46 uint64 = (uint64(a) >> 46) & 1
	var x0_47 uint64 = (uint64(a) >> 47) & 1
	var x0_48 uint64 = (uint64(a) >> 48) & 1
	var x0_49 uint64 = (uint64(a) >> 49) & 1
	var x0_50 uint64 = (uint64(a) >> 50) & 1
	var x0_51 uint64 = (uint64(a) >> 51) & 1
	var x0_52 uint64 = (uint64(a) >> 52) & 1
	var x0_53 uint64 = (uint64(a) >> 53) & 1
	var x0_54 uint64 = (uint64(a) >> 54) & 1
	var x0_55 uint64 = (uint64(a) >> 55) & 1
	var x0_56 uint64 = (uint64(a) >> 56) & 1
	var x0_57 uint64 = (uint64(a) >> 57) & 1
	var x0_58 uint64 = (uint64(a) >> 58) & 1
	var x0_59 uint64 = (uint64(a) >> 59) & 1
	var x0_60 uint64 = (uint64(a) >> 60) & 1
	var x0_61 uint64 = (uint64(a) >> 61) & 1
	var x0_62 uint64 = (uint64(a) >> 62) & 1
	var x0_63 uint64 = (uint64(a) >> 63) & 1
	var w0 uint64 = (x1_32 << 0)
	var w1 uint64 = w0 | (x1_33 << 1)
	var w2 uint64 = w1 | (x1_34 << 2)
	var w3 uint64 = w2 | (x1_35 << 3)
	var w4 uint64 = w3 | (x1_36 << 4)
	var w5 uint64 = w4 | (x1_37 << 5)
	var w6 uint64 = w5 | (x1_38 << 6)
	var w7 uint64 = w6 | (x1_39 << 7)
	var w8 uint64 = w7 | (x1_40 << 8)
	var w9 uint64 = w8 | (x1_41 << 9)
	var w10 uint64 = w9 | (x1_42 << 10)
	var w11 uint64 = w10 | (x1_43 << 11)
	var w12 uint64 = w11 | (x1_44 << 12)
	var w13 uint64 = w12 | (x1_45 << 13)
	var w14 uint64 = w13 | (x1_46 << 14)
	var w15 uint64 = w14 | (x1_47 << 15)
	var w16 uint64 = w15 | (x1_48 << 16)
	var w17 uint64 = w16 | (x1_49 << 17)
	var w18 uint64 = w17 | (x1_50 << 18)
	var w19 uint64 = w18 | (x1_51 << 19)
	var w20 uint64 = w19 | (x1_52 << 20)
	var w21 uint64 = w20 | (x1_53 << 21)
	var w22 uint64 = w21 | (x1_54 << 22)
	var w23 uint64 = w22 | (x1_55 << 23)
	var w24 uint64 = w23 | (x1_56 << 24)
	var w25 uint64 = w24 | (x1_57 << 25)
	var w26 uint64 = w25 | (x1_58 << 26)
	var w27 uint64 = w26 | (x1_59 << 27)
	var w28 uint64 = w27 | (x1_60 << 28)
	var w29 uint64 = w28 | (x1_61 << 29)
	var w30 uint64 = w29 | (x1_62 << 30)
	var w31 uint64 = w30 | (x1_63 << 31)
	var w32 uint64 = w31 | (x0_32 << 32)
	var w33 uint64 = w32 | (x0_33 << 33)
	var w34 uint64 = w33 | (x0_34 << 34)
	var w35 uint64 = w34 | (x0_35 << 35)
	var w36 uint64 = w35 | (x0_36 << 36)
	var w37 uint64 = w36 | (x0_37 << 37)
	var w38 uint64 = w37 | (x0_38 << 38)
	var w39 uint64 = w38 | (x0_39 << 39)
	var w40 uint64 = w39 | (x0_40 << 40)
	var w41 uint64 = w40 | (x0_41 << 41)
	var w42 uint64 = w41 | (x0_42 << 42)
	var w43 uint64 = w42 | (x0_43 << 43)
	var w44 uint64 = w43 | (x0_44 << 44)
	var w45 uint64 = w44 | (x0_45 << 45)
	var w46 uint64 = w45 | (x0_46 << 46)
	var w47 uint64 = w46 | (x0_47 << 47)
	var w48 uint64 = w47 | (x0_48 << 48)
	var w49 uint64 = w48 | (x0_49 << 49)
	var w50 uint64 = w49 | (x0_50 << 50)
	var w51 uint64 = w50 | (x0_51 << 51)
	var w52 uint64 = w51 | (x0_52 << 52)
	var w53 uint64 = w52 | (x0_53 << 53)
	var w54 uint64 = w53 | (x0_54 << 54)
	var w55 uint64 = w54 | (x0_55 << 55)
	var w56 uint64 = w55 | (x0_56 << 56)
	var w57 uint64 = w56 | (x0_57 << 57)
	var w58 uint64 = w57 | (x0_58 << 58)
	var w59 uint64 = w58 | (x0_59 << 59)
	var w60 uint64 = w59 | (x0_60 << 60)
	var w61 uint64 = w60 | (x0_61 << 61)
	var w62 uint64 = w61 | (x0_62 << 62)
	var w63 uint64 = w62 | (x0_63 << 63)
	return math.Float64frombits(uint64(w63))
}

var g0 uint64
var g1 float64
var sink interface{}

func main() {
	sink = emu_punpckldq_mem_xmm_128__reg_xmm0_high__go__bit_blast(g0, g1)
	_ = sink
}
