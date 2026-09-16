// probe 240 -- binary ^
#[no_mangle]
pub fn op_240(a: bool, b: i32) -> <bool as core::ops::BitXor<i32>>::Output {
    a ^ b
}
