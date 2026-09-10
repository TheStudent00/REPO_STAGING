// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of add_gpr_gpr_64__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   v0 + v1
@_cdecl("emu_add_gpr_gpr_64__reg_rdi__swift")
public func emu_add_gpr_gpr_64__reg_rdi__swift(_ a: UInt64, _ b: UInt64) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(a)))) &+ (UInt64(truncatingIfNeeded: (UInt64(b)))))))
}
