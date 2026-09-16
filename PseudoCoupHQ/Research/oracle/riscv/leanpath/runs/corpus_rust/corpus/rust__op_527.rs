// probe 527 -- binary >>
#[no_mangle]
pub fn op_527(a: f64, b: bool) -> <f64 as core::ops::Shr<bool>>::Output {
    a >> b
}
