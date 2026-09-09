// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of div_gpr_one_32__reg_rdx__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, bvurem_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(0, Extract(31, 0, v2)))))
@_cdecl("emu_div_gpr_one_32__reg_rdx__swift")
public func emu_div_gpr_one_32__reg_rdx__swift(_ a: UInt32, _ b: UInt32, _ c: UInt32) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) | (UInt64(truncatingIfNeeded: (UInt32(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: (UInt32(a)))) &<< 32) | (UInt64(truncatingIfNeeded: (UInt32(b))))))))) % ((UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) | (UInt64(truncatingIfNeeded: (UInt32(c))))))))))))) &>> 0)))))))
}
