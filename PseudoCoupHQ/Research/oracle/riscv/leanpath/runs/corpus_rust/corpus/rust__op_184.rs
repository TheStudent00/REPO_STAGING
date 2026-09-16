// probe 184 -- binary |
#[no_mangle]
pub fn op_184(a: i64, b: f64) -> <i64 as core::ops::BitOr<f64>>::Output {
    a | b
}
