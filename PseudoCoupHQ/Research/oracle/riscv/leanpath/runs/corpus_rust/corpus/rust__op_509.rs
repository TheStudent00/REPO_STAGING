// probe 509 -- binary >>
#[no_mangle]
pub fn op_509(a: i64, b: bool) -> <i64 as core::ops::Shr<bool>>::Output {
    a >> b
}
