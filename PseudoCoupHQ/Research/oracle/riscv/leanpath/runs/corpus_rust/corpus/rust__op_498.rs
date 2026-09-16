// probe 498 -- binary >>
#[no_mangle]
pub fn op_498(a: i32, b: i32) -> <i32 as core::ops::Shr<i32>>::Output {
    a >> b
}
