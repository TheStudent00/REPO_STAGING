// probe 199 -- binary |
#[no_mangle]
pub fn op_199(a: f64, b: i64) -> <f64 as core::ops::BitOr<i64>>::Output {
    a | b
}
