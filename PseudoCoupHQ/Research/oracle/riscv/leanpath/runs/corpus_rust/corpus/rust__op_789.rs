// probe 789 -- binary ..=
#[no_mangle]
pub fn op_789(a: i32, b: f32) -> core::ops::RangeInclusive<i32> {
    a ..= b
}
