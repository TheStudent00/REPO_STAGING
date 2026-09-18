// arch-unit 212  --  c  `__alignof a`  lhs=float rhs=None
// symbol op_63   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x4                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
public final class au_212_c_alignof_gnu_f32 {

    public static long au_212_c_alignof_gnu_f32(long p0) {
        // fa0: operand `a` (float) arrives in fa0 as a bit pattern
        final long v1 = ((p0) & 0xffffffffL);
        final long v2 = 0x4L;
        // the answer is uint64_t, 64 bits
        return v2;
    }
}
