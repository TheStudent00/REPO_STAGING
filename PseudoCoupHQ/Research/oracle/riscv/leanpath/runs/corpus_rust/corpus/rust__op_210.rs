// probe 210 -- binary ^
#[no_mangle]
pub fn op_210(a: i32, b: i32) -> <i32 as core::ops::BitXor<i32>>::Output {
    a ^ b
}
