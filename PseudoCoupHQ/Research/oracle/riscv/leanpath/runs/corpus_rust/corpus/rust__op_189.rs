// probe 189 -- binary |
#[no_mangle]
pub fn op_189(a: u64, b: f32) -> <u64 as core::ops::BitOr<f32>>::Output {
    a | b
}
