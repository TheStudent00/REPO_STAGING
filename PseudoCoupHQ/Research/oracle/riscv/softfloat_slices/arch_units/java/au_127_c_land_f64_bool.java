// arch-unit 127  --  c  `a && b`  lhs=double rhs=bool
// symbol op_347   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
//   andn a0, a0, a1                    integer  operator:& ~
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_127_c_land_f64_bool {
    public static long au_127_c_land_f64_bool(long p0, long p1) {
    // fa0: operand `a` (double) arrives in fa0
        final long v1 = p0;
    // a0: operand `b` (bool) zero-extended
        final long v2 = ((p1) & 0x1L);
        final long v3 = 0x0L;
        final long v4 = (f64_eq.f64_eq_rm0(v1, v3) ? 1L : 0L);
        final long v5 = ((v2) & (~(v4)));
        return v5;
    }
}
