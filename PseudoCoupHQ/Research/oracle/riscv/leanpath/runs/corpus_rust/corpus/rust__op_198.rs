// probe 198 -- binary |
#[no_mangle]
pub fn op_198(a: f64, b: i32) -> <f64 as core::ops::BitOr<i32>>::Output {
    a | b
}
