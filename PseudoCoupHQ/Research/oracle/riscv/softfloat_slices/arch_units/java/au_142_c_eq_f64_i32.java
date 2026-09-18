// arch-unit 142  --  c  `a == b`  lhs=double rhs=int32_t
// symbol op_486   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.w fa5, a0                   float    emulation:i32_to_f64_rm0
//   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_142_c_eq_f64_i32 {
    public static long au_142_c_eq_f64_i32(long p0, long p1) {
    // fa0: operand `a` (double) arrives in fa0
        final long v1 = p0;
    // a0: operand `b` (int32_t) sign-extended to XLEN
        final long v2 = ((long)(int)(p1));
        final long v3 = i32_to_f64.i32_to_f64_rm0(((int)((((v2) & 0xffffffffL)) & 0xffffffffL)));
        final long v4 = (f64_eq.f64_eq_rm0(v1, v3) ? 1L : 0L);
        return v4;
    }
}
