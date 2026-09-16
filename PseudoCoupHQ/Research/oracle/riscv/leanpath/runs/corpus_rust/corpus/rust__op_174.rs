// probe 174 -- binary |
#[no_mangle]
pub fn op_174(a: i32, b: i32) -> <i32 as core::ops::BitOr<i32>>::Output {
    a | b
}
