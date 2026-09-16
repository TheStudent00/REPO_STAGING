// probe 601 -- binary -
#[no_mangle]
pub fn op_601(a: bool, b: i64) -> <bool as core::ops::Sub<i64>>::Output {
    a - b
}
