// probe 476 -- binary <<
#[no_mangle]
pub fn op_476(a: u64, b: u64) -> <u64 as core::ops::Shl<u64>>::Output {
    a << b
}


#[no_mangle]
pub extern "C" fn emu_RTYPE__SLL(a: u64, b: u64) -> u64 {
    ((op_476((a) as u64, (b) as u64)) as u64)
}
