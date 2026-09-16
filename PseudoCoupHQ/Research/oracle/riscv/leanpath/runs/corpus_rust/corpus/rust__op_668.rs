// probe 668 -- binary /
#[no_mangle]
pub fn op_668(a: f64, b: u64) -> <f64 as core::ops::Div<u64>>::Output {
    a / b
}
