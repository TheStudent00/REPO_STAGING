// probe 510 -- binary >>
#[no_mangle]
pub fn op_510(a: u64, b: i32) -> <u64 as core::ops::Shr<i32>>::Output {
    a >> b
}
