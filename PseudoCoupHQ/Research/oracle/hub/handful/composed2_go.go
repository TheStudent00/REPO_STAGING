package main

import "math"

//go:noinline
func emu_add_gpr_gpr_32__primitive__go(a int32, b int32) int32 {
	return a + b
}

//go:noinline
func emu_sub_gpr_gpr_32__primitive__go(a int32, b int32) int32 {
	return a - b
}

//go:noinline
func emu_imul_gpr_gpr_32__primitive__go(a int32, b int32) int32 {
	return a * b
}

//go:noinline
func emu_add_gpr_gpr_64__primitive__go(a int64, b int64) int64 {
	return a + b
}

//go:noinline
func emu_sub_gpr_gpr_64__primitive__go(a int64, b int64) int64 {
	return a - b
}

//go:noinline
func emu_imul_gpr_gpr_64__primitive__go(a int64, b int64) int64 {
	return a * b
}

//go:noinline
func emu_addsd_xmm_xmm_64__reg_xmm0__go(a float64, b float64) float64 {
	return math.Float64frombits(uint64(uint64(math.Float64bits(((a) + (b))))))
}

//go:noinline
func emu_mulsd_xmm_xmm_64__reg_xmm0__go(a float64, b float64) float64 {
	return math.Float64frombits(uint64(uint64(math.Float64bits(((a) * (b))))))
}

//go:noinline
func f1_i32_add_sub(a int32, b int32, c int32) int32 {
	hub_t0 := int32(uint32(emu_add_gpr_gpr_32__primitive__go(int32(a), int32(b))))
	hub_t1 := int32(uint32(emu_sub_gpr_gpr_32__primitive__go(int32(hub_t0), int32(c))))
	return hub_t1
}

//go:noinline
func f2_i32_add_mul(a int32, b int32, c int32) int32 {
	hub_t0 := int32(uint32(emu_add_gpr_gpr_32__primitive__go(int32(a), int32(b))))
	hub_t1 := int32(uint32(emu_imul_gpr_gpr_32__primitive__go(int32(hub_t0), int32(c))))
	return hub_t1
}

//go:noinline
func f3_i64_add_sub(a int64, b int64, c int64) int64 {
	hub_t0 := int64(uint64(emu_add_gpr_gpr_64__primitive__go(int64(a), int64(b))))
	hub_t1 := int64(uint64(emu_sub_gpr_gpr_64__primitive__go(int64(hub_t0), int64(c))))
	return hub_t1
}

//go:noinline
func f4_i64_mul(a int64, b int64) int64 {
	hub_t0 := int64(uint64(emu_imul_gpr_gpr_64__primitive__go(int64(a), int64(b))))
	return hub_t0
}

//go:noinline
func f7_f64_add_mul(a float64, b float64, c float64) float64 {
	hub_t0 := float64(emu_addsd_xmm_xmm_64__reg_xmm0__go(float64(a), float64(b)))
	hub_t1 := float64(emu_mulsd_xmm_xmm_64__reg_xmm0__go(float64(hub_t0), float64(c)))
	return hub_t1
}

var hub_g0 int32
var hub_g1 int32
var hub_g2 int32
var hub_g3 int32
var hub_g4 int32
var hub_g5 int32
var hub_g6 int64
var hub_g7 int64
var hub_g8 int64
var hub_g9 int64
var hub_g10 int64
var hub_g11 float64
var hub_g12 float64
var hub_g13 float64
var hub_sink interface{}

func main() {
	hub_sink = f1_i32_add_sub(hub_g0, hub_g1, hub_g2)
	hub_sink = f2_i32_add_mul(hub_g3, hub_g4, hub_g5)
	hub_sink = f3_i64_add_sub(hub_g6, hub_g7, hub_g8)
	hub_sink = f4_i64_mul(hub_g9, hub_g10)
	hub_sink = f7_f64_add_mul(hub_g11, hub_g12, hub_g13)
	_ = hub_sink
}
