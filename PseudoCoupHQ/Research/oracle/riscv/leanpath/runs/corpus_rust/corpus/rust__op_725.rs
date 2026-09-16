// probe 725 -- binary ..
#[no_mangle]
pub fn op_725(a: i64, b: bool) -> core::ops::Range<i64> {
    a .. b
}
