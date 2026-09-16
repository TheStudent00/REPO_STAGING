// probe 178 -- binary |
#[no_mangle]
pub fn op_178(a: i32, b: f64) -> <i32 as core::ops::BitOr<f64>>::Output {
    a | b
}
