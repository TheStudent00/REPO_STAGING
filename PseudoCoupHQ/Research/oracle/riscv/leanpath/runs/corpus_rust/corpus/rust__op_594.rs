// probe 594 -- binary -
#[no_mangle]
pub fn op_594(a: f64, b: i32) -> <f64 as core::ops::Sub<i32>>::Output {
    a - b
}
