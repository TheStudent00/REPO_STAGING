// probe 235 -- binary ^
#[no_mangle]
pub fn op_235(a: f64, b: i64) -> <f64 as core::ops::BitXor<i64>>::Output {
    a ^ b
}
