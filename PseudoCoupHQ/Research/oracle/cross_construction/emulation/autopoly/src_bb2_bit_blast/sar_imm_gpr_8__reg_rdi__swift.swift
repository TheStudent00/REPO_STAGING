// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of sar_imm_gpr_8__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v0), Extract(7, 0, v0) >> 3)
@_cdecl("emu_sar_imm_gpr_8__reg_rdi__swift")
public func emu_sar_imm_gpr_8__reg_rdi__swift(_ a: UInt64) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(a))) &>> 8)) & UInt64(0xffffffffffffff)))) &<< 8) | (UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: UInt32(bitPattern: ((((Int32(bitPattern: ((UInt32(truncatingIfNeeded: ((UInt64(a))) &>> 0)) & UInt32(0xff)))) &<< 24) &>> 24)) &>> (UInt32(truncatingIfNeeded: UInt32(0x3)))))) & UInt32(0xff)))))))
}
