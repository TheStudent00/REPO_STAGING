// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of shl_cl_gpr_32__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, v0) << Concat(0, Extract(4, 0, v1)))
@_cdecl("emu_shl_cl_gpr_32__reg_rdi__swift")
public func emu_shl_cl_gpr_32__reg_rdi__swift(_ a: UInt32, _ b: UInt8) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) | (UInt64(truncatingIfNeeded: (UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: (UInt32(a)))) &<< (UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: UInt32(0x0))) &<< 5) | (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(b))) &>> 0)) & UInt32(0x1f)))))))))))))))
}
