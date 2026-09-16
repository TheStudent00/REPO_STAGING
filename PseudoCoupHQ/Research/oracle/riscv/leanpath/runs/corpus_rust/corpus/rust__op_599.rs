// probe 599 -- binary -
#[no_mangle]
pub fn op_599(a: f64, b: bool) -> <f64 as core::ops::Sub<bool>>::Output {
    a - b
}
