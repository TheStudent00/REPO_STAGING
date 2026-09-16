// probe 236 -- binary ^
#[no_mangle]
pub fn op_236(a: f64, b: u64) -> <f64 as core::ops::BitXor<u64>>::Output {
    a ^ b
}
