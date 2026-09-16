// probe 558 -- binary +
#[no_mangle]
pub fn op_558(a: f64, b: i32) -> <f64 as core::ops::Add<i32>>::Output {
    a + b
}
