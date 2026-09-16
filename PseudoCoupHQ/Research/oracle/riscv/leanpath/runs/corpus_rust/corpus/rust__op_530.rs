// probe 530 -- binary >>
#[no_mangle]
pub fn op_530(a: bool, b: u64) -> <bool as core::ops::Shr<u64>>::Output {
    a >> b
}
