// arch-unit 237  --  c  `a--`  lhs=double rhs=None
// symbol op_100   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: double, 64 bits.  parameters are operand bit patterns.
public final class au_237_c_postdec_f64 {

    public static long au_237_c_postdec_f64(long p0) {
        // fa0: operand `a` (double) arrives in fa0 as a bit pattern
        final long v1 = p0;
        // the answer is double, 64 bits
        return v1;
    }
}
