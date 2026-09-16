// probe 194 -- binary |
#[no_mangle]
pub fn op_194(a: f32, b: u64) -> <f32 as core::ops::BitOr<u64>>::Output {
    a | b
}
