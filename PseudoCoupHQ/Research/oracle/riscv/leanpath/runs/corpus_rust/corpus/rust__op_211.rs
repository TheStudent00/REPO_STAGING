// probe 211 -- binary ^
#[no_mangle]
pub fn op_211(a: i32, b: i64) -> <i32 as core::ops::BitXor<i64>>::Output {
    a ^ b
}
