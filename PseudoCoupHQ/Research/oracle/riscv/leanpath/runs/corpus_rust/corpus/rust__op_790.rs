// probe 790 -- binary ..=
#[no_mangle]
pub fn op_790(a: i32, b: f64) -> core::ops::RangeInclusive<i32> {
    a ..= b
}
