// probe 798 -- binary ..=
#[no_mangle]
pub fn op_798(a: u64, b: i32) -> core::ops::RangeInclusive<u64> {
    a ..= b
}
