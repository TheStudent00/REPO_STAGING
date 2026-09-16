// probe 662 -- binary /
#[no_mangle]
pub fn op_662(a: f32, b: u64) -> <f32 as core::ops::Div<u64>>::Output {
    a / b
}
