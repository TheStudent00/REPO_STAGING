// probe 168 -- binary &
#[no_mangle]
pub fn op_168(a: bool, b: i32) -> <bool as core::ops::BitAnd<i32>>::Output {
    a & b
}
