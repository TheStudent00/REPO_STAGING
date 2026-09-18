// arch-unit 29  --  c  `a + b`  lhs=bool rhs=double
// symbol op_136   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.wu fa5, a0                  float    emulation:ui32_to_f64_rm0
//   fadd.d fa0, fa0, fa5, dyn          float    emulation:f64_add_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
public final class au_029_c_add_bool_f64 {
    public static long au_029_c_add_bool_f64(long p0, long p1) {
    // a0: operand `a` (bool) zero-extended
        final long v1 = ((p0) & 0x1L);
    // fa0: operand `b` (double) arrives in fa0
        final long v2 = p1;
        final long v3 = ui32_to_f64.ui32_to_f64_rm0(((int)((((v1) & 0xffffffffL)) & 0xffffffffL)));
        final long v4 = f64_add.f64_add_rm0(v2, v3);
        return v4;
    }
}
