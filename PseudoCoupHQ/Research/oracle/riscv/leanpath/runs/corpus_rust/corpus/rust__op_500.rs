// probe 500 -- binary >>
#[no_mangle]
pub fn op_500(a: i32, b: u64) -> <i32 as core::ops::Shr<u64>>::Output {
    a >> b
}
