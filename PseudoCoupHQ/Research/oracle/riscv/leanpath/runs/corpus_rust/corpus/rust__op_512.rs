// probe 512 -- binary >>
#[no_mangle]
pub fn op_512(a: u64, b: u64) -> <u64 as core::ops::Shr<u64>>::Output {
    a >> b
}
