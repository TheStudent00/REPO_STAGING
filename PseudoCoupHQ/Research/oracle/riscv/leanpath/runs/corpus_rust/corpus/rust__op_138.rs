// probe 138 -- binary &
#[no_mangle]
pub fn op_138(a: i32, b: i32) -> <i32 as core::ops::BitAnd<i32>>::Output {
    a & b
}
