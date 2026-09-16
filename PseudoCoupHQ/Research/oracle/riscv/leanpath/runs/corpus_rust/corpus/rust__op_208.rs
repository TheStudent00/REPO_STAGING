// probe 208 -- binary |
#[no_mangle]
pub fn op_208(a: bool, b: f64) -> <bool as core::ops::BitOr<f64>>::Output {
    a | b
}
