// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of cmovl_gpr_gpr_64__reg_rdi__swift__constructed.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   If(Extract(63, 63, v0 + 18446744073709551613) == If(Extract(63, 63, Concat(Extract(63, 63, v0), v0) + 36893488147419103229) == Extract(64, 64, Concat(Extract(63, 63, v0), v0) + 36893488147419103229), 1, 0), v1, v2)
@_cdecl("emu_cmovl_gpr_gpr_64__reg_rdi__swift__constructed")
public func emu_cmovl_gpr_gpr_64__reg_rdi__swift__constructed(_ a: UInt64, _ b: UInt64, _ c: UInt64) -> UInt64
{
    return UInt64(truncatingIfNeeded: ((((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(a)))) &+ (UInt64(truncatingIfNeeded: UInt64(0xfffffffffffffffd))))))) &>> 63)) & UInt32(0x1)))) == (UInt32(truncatingIfNeeded: ((((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt64(a))) &>> 63)) & UInt32(0x1)))) &+ (UInt32(truncatingIfNeeded: ((((((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt64(a))) &>> 0)) & UInt32(0x3)))) == (UInt32(truncatingIfNeeded: UInt32(0x3))))) || ((!(((UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(a))) &>> 2)) & UInt64(0x3fffffffffffffff)))) == (UInt64(truncatingIfNeeded: UInt64(0x0))))))))) ? (UInt32(0x0)) : (UInt32(0x1))))))) & UInt32(0x1)))) == (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(a)))) &+ (UInt64(truncatingIfNeeded: UInt64(0xfffffffffffffffd))))))) &>> 63)) & UInt32(0x1)))))) ? (UInt32(0x1)) : (UInt32(0x0))))))) ? ((UInt64(b))) : ((UInt64(c)))))
}
