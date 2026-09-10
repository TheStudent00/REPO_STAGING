// handful.go -- task hub1, the file Hub v1 lowers.
//
// Eight explicitly typed functions, each one or two operators, written for
// this task and kept here as the object of the oracle test: body A is what
// go's own build leaves for each of them, body B is what the Hub composes
// for a target out of AutoPoly's proved emulations.
//
// The eight cover the brief's list: `+` `-` `*` on int32 and on int64, `<<`
// and `>>` on uint64 with a count, `/` on int32, float64 `+` and `*`, one
// comparison feeding a select, and one two-operator expression `(a + b) * c`.
//
// The shape is the corpus's own probe shape (`//go:noinline`, package main,
// globals fed to the function from `main` so nothing is folded away), so
// that go's build of this file is carved exactly as every go unit of the
// corpus was carved.
package main

//go:noinline
func f1_i32_add_sub(a int32, b int32, c int32) int32 {
	return a + b - c
}

//go:noinline
func f2_i32_add_mul(a int32, b int32, c int32) int32 {
	return (a + b) * c
}

//go:noinline
func f3_i64_add_sub(a int64, b int64, c int64) int64 {
	return a + b - c
}

//go:noinline
func f4_i64_mul(a int64, b int64) int64 {
	return a * b
}

//go:noinline
func f5_u64_shift(a uint64, n uint64) uint64 {
	return (a << n) >> n
}

//go:noinline
func f6_i32_div(a int32, b int32) int32 {
	return a / b
}

//go:noinline
func f7_f64_add_mul(a float64, b float64, c float64) float64 {
	return (a + b) * c
}

//go:noinline
func f8_i32_select(a int32, b int32, c int32, d int32) int32 {
	if a != b {
		return c
	}
	return d
}

var gi32a int32
var gi32b int32
var gi32c int32
var gi32d int32
var gi64a int64
var gi64b int64
var gi64c int64
var gu64a uint64
var gu64n uint64
var gf64a float64
var gf64b float64
var gf64c float64
var sink interface{}

func main() {
	sink = f1_i32_add_sub(gi32a, gi32b, gi32c)
	sink = f2_i32_add_mul(gi32a, gi32b, gi32c)
	sink = f3_i64_add_sub(gi64a, gi64b, gi64c)
	sink = f4_i64_mul(gi64a, gi64b)
	sink = f5_u64_shift(gu64a, gu64n)
	sink = f6_i32_div(gi32a, gi32b)
	sink = f7_f64_add_mul(gf64a, gf64b, gf64c)
	sink = f8_i32_select(gi32a, gi32b, gi32c, gi32d)
	_ = sink
}
