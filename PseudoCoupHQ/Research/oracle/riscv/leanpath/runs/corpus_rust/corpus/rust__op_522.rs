// probe 522 -- binary >>
#[no_mangle]
pub fn op_522(a: f64, b: i32) -> <f64 as core::ops::Shr<i32>>::Output {
    a >> b
}
