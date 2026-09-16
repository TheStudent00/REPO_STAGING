// probe 502 -- binary >>
#[no_mangle]
pub fn op_502(a: i32, b: f64) -> <i32 as core::ops::Shr<f64>>::Output {
    a >> b
}
