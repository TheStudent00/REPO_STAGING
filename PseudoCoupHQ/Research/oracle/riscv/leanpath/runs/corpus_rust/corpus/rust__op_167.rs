// probe 167 -- binary &
#[no_mangle]
pub fn op_167(a: f64, b: bool) -> <f64 as core::ops::BitAnd<bool>>::Output {
    a & b
}
