// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of div_gpr_one_8__reg_rax__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v0), Extract(7, 0, bvurem_i(Extract(15, 0, v0), Concat(0, Extract(7, 0, v1)))), Extract(7, 0, bvudiv_i(Extract(15, 0, v0), Concat(0, Extract(7, 0, v1)))))
@_cdecl("emu_div_gpr_one_8__reg_rax__swift")
public func emu_div_gpr_one_8__reg_rax__swift(_ a: UInt64, _ b: UInt8) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(a))) &>> 16)) & UInt64(0xffffffffffff)))) &<< 16) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt64(a))) &>> 0)) & UInt32(0xffff))))) % ((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: UInt32(0x0))) &<< 8) | (UInt32(truncatingIfNeeded: (UInt32(b)))))) & UInt32(0xffff))))))) & UInt32(0xffff)))) &>> 0)) & UInt32(0xff)))) &<< 8) | (UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt64(a))) &>> 0)) & UInt32(0xffff))))) / ((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: UInt32(0x0))) &<< 8) | (UInt32(truncatingIfNeeded: (UInt32(b)))))) & UInt32(0xffff))))))) & UInt32(0xffff)))) &>> 0)) & UInt32(0xff)))))))
}
