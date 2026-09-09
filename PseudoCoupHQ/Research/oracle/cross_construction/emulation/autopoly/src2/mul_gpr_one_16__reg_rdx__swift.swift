// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of mul_gpr_one_16__reg_rdx__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v2), Extract(31, 16, Concat(0, Extract(15, 0, v0))*Concat(0, Extract(15, 0, v1))))
@_cdecl("emu_mul_gpr_one_16__reg_rdx__swift")
public func emu_mul_gpr_one_16__reg_rdx__swift(_ a: UInt16, _ b: UInt16, _ c: UInt64) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(c))) &>> 16)) & UInt64(0xffffffffffff)))) &<< 16) | (UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: UInt32(0x0))) &<< 16) | (UInt32(truncatingIfNeeded: (UInt32(a)))))))) &* (UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: UInt32(0x0))) &<< 16) | (UInt32(truncatingIfNeeded: (UInt32(b)))))))))))) &>> 16)) & UInt32(0xffff)))))))
}
