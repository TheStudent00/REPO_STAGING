// probe 162 -- binary &
#[no_mangle]
pub fn op_162(a: f64, b: i32) -> <f64 as core::ops::BitAnd<i32>>::Output {
    a & b
}
