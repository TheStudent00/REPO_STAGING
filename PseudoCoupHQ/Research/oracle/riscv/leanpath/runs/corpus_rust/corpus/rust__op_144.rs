// probe 144 -- binary &
#[no_mangle]
pub fn op_144(a: i64, b: i32) -> <i64 as core::ops::BitAnd<i32>>::Output {
    a & b
}
