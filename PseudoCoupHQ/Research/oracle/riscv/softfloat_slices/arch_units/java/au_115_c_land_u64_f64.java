// arch-unit 115  --  c  `a && b`  lhs=uint64_t rhs=double
// symbol op_334   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, zero, a0                  integer  operator:<
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
//   xori a1, a1, 0x1                   integer  operator:^
//   c.and a0, a1                       integer  operator:&
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_115_c_land_u64_f64 {
    public static long au_115_c_land_u64_f64(long p0, long p1) {
    // a0: operand `a` (uint64_t) arrives in a0
        final long v1 = p0;
    // fa0: operand `b` (double) arrives in fa0
        final long v2 = p1;
        final long v3 = (Long.compareUnsigned(0x0L, v1) < 0 ? 1L : 0L);
        final long v4 = 0x0L;
        final long v5 = (f64_eq.f64_eq_rm0(v2, v4) ? 1L : 0L);
        final long v6 = ((v5) ^ 0x1L);
        final long v7 = ((v3) & (v6));
        return v7;
    }
}
