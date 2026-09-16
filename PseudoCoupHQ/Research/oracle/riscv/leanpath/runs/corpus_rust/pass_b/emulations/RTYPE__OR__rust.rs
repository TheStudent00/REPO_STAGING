// probe 188 -- binary |
#[no_mangle]
pub fn op_188(a: u64, b: u64) -> <u64 as core::ops::BitOr<u64>>::Output {
    a | b
}


#[no_mangle]
pub extern "C" fn emu_RTYPE__OR(a: u64, b: u64) -> u64 {
    ((op_188((a) as u64, (b) as u64)) as u64)
}
