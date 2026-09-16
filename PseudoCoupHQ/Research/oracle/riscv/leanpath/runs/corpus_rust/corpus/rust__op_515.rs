// probe 515 -- binary >>
#[no_mangle]
pub fn op_515(a: u64, b: bool) -> <u64 as core::ops::Shr<bool>>::Output {
    a >> b
}
