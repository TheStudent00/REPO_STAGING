// probe 529 -- binary >>
#[no_mangle]
pub fn op_529(a: bool, b: i64) -> <bool as core::ops::Shr<i64>>::Output {
    a >> b
}
