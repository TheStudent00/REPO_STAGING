// probe 545 -- binary +
#[no_mangle]
pub fn op_545(a: i64, b: bool) -> <i64 as core::ops::Add<bool>>::Output {
    a + b
}
