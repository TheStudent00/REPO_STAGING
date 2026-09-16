// probe 176 -- binary |
#[no_mangle]
pub fn op_176(a: i32, b: u64) -> <i32 as core::ops::BitOr<u64>>::Output {
    a | b
}
