// probe 528 -- binary >>
#[no_mangle]
pub fn op_528(a: bool, b: i32) -> <bool as core::ops::Shr<i32>>::Output {
    a >> b
}
