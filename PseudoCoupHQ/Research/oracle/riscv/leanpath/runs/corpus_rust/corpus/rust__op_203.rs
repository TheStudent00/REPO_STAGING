// probe 203 -- binary |
#[no_mangle]
pub fn op_203(a: f64, b: bool) -> <f64 as core::ops::BitOr<bool>>::Output {
    a | b
}
