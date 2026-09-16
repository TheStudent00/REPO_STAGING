// probe 234 -- binary ^
#[no_mangle]
pub fn op_234(a: f64, b: i32) -> <f64 as core::ops::BitXor<i32>>::Output {
    a ^ b
}
