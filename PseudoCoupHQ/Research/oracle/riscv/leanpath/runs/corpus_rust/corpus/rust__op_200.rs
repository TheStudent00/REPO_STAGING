// probe 200 -- binary |
#[no_mangle]
pub fn op_200(a: f64, b: u64) -> <f64 as core::ops::BitOr<u64>>::Output {
    a | b
}
