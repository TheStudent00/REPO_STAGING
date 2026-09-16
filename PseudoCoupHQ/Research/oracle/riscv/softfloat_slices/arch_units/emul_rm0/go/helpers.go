// Package emul holds the RISC-V float arch-opcodes as ordinary integer go.
//
// helpers.go is the eight LLVM intrinsics the flattened slices use, the three
// don't-care pins, and the 128-bit integer go does not have.
//
//	ctlz      BUILT-IN: math/bits.LeadingZeros32/64 return the bit width for
//	          0, which is exactly LLVM's ctlz with is_zero_poison=false, so
//	          the edge case matches and the built-in is used.
//	abs       WRITTEN OUT.  go has no integer abs; math.Abs is float64 and
//	          would round.  LLVM's llvm.abs wraps at INT_MIN, so this does.
//	usub.sat  WRITTEN OUT.  go has no saturating subtract.
//	fshl      WRITTEN OUT.  go has no funnel shift; bits.RotateLeft64 is only
//	          the a == b case.
//	udiv      WRITTEN OUT with a zero guard: go panics on divide by zero.
//
// Shifts in the emitted bodies are written `x << (n & (W-1))`, because go
// does NOT mask the shift amount - it yields 0 for an over-wide shift.  The
// mask pins the same rule c, c++ and rust use.
package emul

import "math/bits"

// ------------------------------------------------------------ intrinsics --

func sfCtlz32(x uint32) uint32 { return uint32(bits.LeadingZeros32(x)) }

func sfCtlz64(x uint64) uint64 { return uint64(bits.LeadingZeros64(x)) }

func sfCtlz16(x uint16) uint16 { return uint16(bits.LeadingZeros16(x)) }

func sfAbs16(x uint16) uint16 {
	if int16(x) < 0 {
		return uint16(0) - x
	}
	return x
}

func sfAbs32(x uint32) uint32 {
	if int32(x) < 0 {
		return uint32(0) - x
	}
	return x
}

func sfAbs64(x uint64) uint64 {
	if int64(x) < 0 {
		return uint64(0) - x
	}
	return x
}

func sfUsubsat8(a, b uint8) uint8 {
	if a > b {
		return a - b
	}
	return 0
}

func sfUsubsat16(a, b uint16) uint16 {
	if a > b {
		return a - b
	}
	return 0
}

func sfUsubsat32(a, b uint32) uint32 {
	if a > b {
		return a - b
	}
	return 0
}

func sfFshl64(a, b, c uint64) uint64 {
	s := c & 63
	if s == 0 {
		return a
	}
	return (a << s) | (b >> (64 - s))
}

func sfFshl32(a, b, c uint32) uint32 {
	s := c & 31
	if s == 0 {
		return a
	}
	return (a << s) | (b >> (32 - s))
}

// -------------------------------------------------------- pinned poison --

func sfUdiv32(a, b uint32) uint32 {
	if b == 0 {
		return 0
	}
	return a / b
}

func sfUdiv64(a, b uint64) uint64 {
	if b == 0 {
		return 0
	}
	return a / b
}

// ------------------------------------------------------------ i1 widening --

func sfB2u8(b bool) uint8 {
	if b {
		return 1
	}
	return 0
}

func sfB2u16(b bool) uint16 {
	if b {
		return 1
	}
	return 0
}

func sfB2u32(b bool) uint32 {
	if b {
		return 1
	}
	return 0
}

func sfB2u64(b bool) uint64 {
	if b {
		return 1
	}
	return 0
}

func sfSext1u8(b bool) uint8 {
	if b {
		return 0xFF
	}
	return 0
}

func sfSext1u16(b bool) uint16 {
	if b {
		return 0xFFFF
	}
	return 0
}

func sfSext1u32(b bool) uint32 {
	if b {
		return 0xFFFFFFFF
	}
	return 0
}

func sfSext1u64(b bool) uint64 {
	if b {
		return 0xFFFFFFFFFFFFFFFF
	}
	return 0
}

// ---------------------------------------------------------------- 128-bit --
//
// go is the one language of the four with no 128-bit integer, so i128 is a
// pair of 64-bit halves.  Only f64_mul and f64_mulAdd reach it, and only
// through zext64, mul, lshr-by-64, trunc-to-64 and a sign test; every
// operation the flattened corpus can produce is written out here anyway.

// U128 is a little-endian pair: Lo is bits 0..63, Hi is bits 64..127.
type U128 struct {
	Hi uint64
	Lo uint64
}

func u128And(a, b U128) U128 { return U128{a.Hi & b.Hi, a.Lo & b.Lo} }
func u128Or(a, b U128) U128  { return U128{a.Hi | b.Hi, a.Lo | b.Lo} }
func u128Xor(a, b U128) U128 { return U128{a.Hi ^ b.Hi, a.Lo ^ b.Lo} }

func u128Add(a, b U128) U128 {
	lo, carry := bits.Add64(a.Lo, b.Lo, 0)
	hi, _ := bits.Add64(a.Hi, b.Hi, carry)
	return U128{hi, lo}
}

func u128Sub(a, b U128) U128 {
	lo, borrow := bits.Sub64(a.Lo, b.Lo, 0)
	hi, _ := bits.Sub64(a.Hi, b.Hi, borrow)
	return U128{hi, lo}
}

// u128Mul is the low 128 bits of the 256-bit product.
func u128Mul(a, b U128) U128 {
	hi, lo := bits.Mul64(a.Lo, b.Lo)
	hi += a.Hi*b.Lo + a.Lo*b.Hi
	return U128{hi, lo}
}

func u128Shl(a, b U128) U128 {
	n := uint(b.Lo & 127)
	switch {
	case n == 0:
		return a
	case n < 64:
		return U128{(a.Hi << n) | (a.Lo >> (64 - n)), a.Lo << n}
	default:
		return U128{a.Lo << (n - 64), 0}
	}
}

func u128Lshr(a, b U128) U128 {
	n := uint(b.Lo & 127)
	switch {
	case n == 0:
		return a
	case n < 64:
		return U128{a.Hi >> n, (a.Lo >> n) | (a.Hi << (64 - n))}
	default:
		return U128{0, a.Hi >> (n - 64)}
	}
}

// u128Udiv is long division, only used if a mode needs it; f64_mul and
// f64_mulAdd do not.
func u128Udiv(a, b U128) U128 {
	if b.Hi == 0 && b.Lo == 0 {
		return U128{0, 0}
	}
	if b.Hi == 0 && a.Hi < b.Lo {
		q, _ := bits.Div64(a.Hi, a.Lo, b.Lo)
		return U128{0, q}
	}
	var q, r U128
	for i := 127; i >= 0; i-- {
		r = u128Shl(r, U128{0, 1})
		var bit uint64
		if i >= 64 {
			bit = (a.Hi >> uint(i-64)) & 1
		} else {
			bit = (a.Lo >> uint(i)) & 1
		}
		r.Lo |= bit
		if u128Ucmp(r, b) >= 0 {
			r = u128Sub(r, b)
			if i >= 64 {
				q.Hi |= 1 << uint(i-64)
			} else {
				q.Lo |= 1 << uint(i)
			}
		}
	}
	return q
}

func u128Lo64(a U128) uint64 { return a.Lo }
func u128Lo32(a U128) uint32 { return uint32(a.Lo) }
func u128Lo16(a U128) uint16 { return uint16(a.Lo) }
func u128Lo8(a U128) uint8   { return uint8(a.Lo) }
func u128Lo1(a U128) bool    { return a.Lo&1 != 0 }

func u128Sext1(b bool) U128 {
	if b {
		return U128{0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF}
	}
	return U128{0, 0}
}

func u128Sext64(x uint64) U128 {
	if int64(x) < 0 {
		return U128{0xFFFFFFFFFFFFFFFF, x}
	}
	return U128{0, x}
}

func u128Eq(a, b U128) bool { return a.Hi == b.Hi && a.Lo == b.Lo }

func u128Ucmp(a, b U128) int {
	if a.Hi != b.Hi {
		if a.Hi < b.Hi {
			return -1
		}
		return 1
	}
	if a.Lo != b.Lo {
		if a.Lo < b.Lo {
			return -1
		}
		return 1
	}
	return 0
}

func u128Scmp(a, b U128) int {
	x, y := int64(a.Hi), int64(b.Hi)
	if x != y {
		if x < y {
			return -1
		}
		return 1
	}
	if a.Lo != b.Lo {
		if a.Lo < b.Lo {
			return -1
		}
		return 1
	}
	return 0
}
