// probe 143 -- binary &
#[no_mangle]
pub fn op_143(a: i32, b: bool) -> <i32 as core::ops::BitAnd<bool>>::Output {
    a & b
}
