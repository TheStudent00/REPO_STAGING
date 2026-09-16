// probe 220 -- binary ^
#[no_mangle]
pub fn op_220(a: i64, b: f64) -> <i64 as core::ops::BitXor<f64>>::Output {
    a ^ b
}
