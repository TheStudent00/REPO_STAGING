// probe 186 -- binary |
#[no_mangle]
pub fn op_186(a: u64, b: i32) -> <u64 as core::ops::BitOr<i32>>::Output {
    a | b
}
