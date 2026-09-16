// probe 173 -- binary &
#[no_mangle]
pub fn op_173(a: bool, b: bool) -> <bool as core::ops::BitAnd<bool>>::Output {
    a & b
}
