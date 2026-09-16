// probe 215 -- binary ^
#[no_mangle]
pub fn op_215(a: i32, b: bool) -> <i32 as core::ops::BitXor<bool>>::Output {
    a ^ b
}
