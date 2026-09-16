// probe 577 -- binary -
#[no_mangle]
pub fn op_577(a: i64, b: i64) -> <i64 as core::ops::Sub<i64>>::Output {
    a - b
}
