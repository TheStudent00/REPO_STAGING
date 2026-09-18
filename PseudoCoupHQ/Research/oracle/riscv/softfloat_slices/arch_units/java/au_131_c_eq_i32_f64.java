// arch-unit 131  --  c  `a == b`  lhs=int32_t rhs=double
// symbol op_466   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.w fa5, a0                   float    emulation:i32_to_f64_rm0
//   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_131_c_eq_i32_f64 {
    public static long au_131_c_eq_i32_f64(long p0, long p1) {
    // a0: operand `a` (int32_t) sign-extended to XLEN
        final long v1 = ((long)(int)(p0));
    // fa0: operand `b` (double) arrives in fa0
        final long v2 = p1;
        final long v3 = i32_to_f64.i32_to_f64_rm0(((int)((((v1) & 0xffffffffL)) & 0xffffffffL)));
        final long v4 = (f64_eq.f64_eq_rm0(v2, v3) ? 1L : 0L);
        return v4;
    }
}
