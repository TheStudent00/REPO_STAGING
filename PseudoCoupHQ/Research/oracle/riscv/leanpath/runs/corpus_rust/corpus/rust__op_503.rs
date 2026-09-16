// probe 503 -- binary >>
#[no_mangle]
pub fn op_503(a: i32, b: bool) -> <i32 as core::ops::Shr<bool>>::Output {
    a >> b
}
