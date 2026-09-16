// probe 190 -- binary |
#[no_mangle]
pub fn op_190(a: u64, b: f64) -> <u64 as core::ops::BitOr<f64>>::Output {
    a | b
}
