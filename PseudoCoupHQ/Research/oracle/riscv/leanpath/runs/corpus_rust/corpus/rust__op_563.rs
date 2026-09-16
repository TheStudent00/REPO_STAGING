// probe 563 -- binary +
#[no_mangle]
pub fn op_563(a: f64, b: bool) -> <f64 as core::ops::Add<bool>>::Output {
    a + b
}
