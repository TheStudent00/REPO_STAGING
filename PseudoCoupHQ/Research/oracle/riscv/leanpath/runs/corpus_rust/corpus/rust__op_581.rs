// probe 581 -- binary -
#[no_mangle]
pub fn op_581(a: i64, b: bool) -> <i64 as core::ops::Sub<bool>>::Output {
    a - b
}
