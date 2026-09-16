// probe 672 -- binary /
#[no_mangle]
pub fn op_672(a: bool, b: i32) -> <bool as core::ops::Div<i32>>::Output {
    a / b
}
