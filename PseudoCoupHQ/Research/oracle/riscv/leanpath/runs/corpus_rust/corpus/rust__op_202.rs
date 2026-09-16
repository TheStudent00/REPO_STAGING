// probe 202 -- binary |
#[no_mangle]
pub fn op_202(a: f64, b: f64) -> <f64 as core::ops::BitOr<f64>>::Output {
    a | b
}
