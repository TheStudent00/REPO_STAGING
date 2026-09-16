// probe 548 -- binary +
#[no_mangle]
pub fn op_548(a: u64, b: u64) -> <u64 as core::ops::Add<u64>>::Output {
    a + b
}


#[no_mangle]
pub extern "C" fn emu_RTYPE__ADD(a: u64, b: u64) -> u64 {
    ((op_548((a) as u64, (b) as u64)) as u64)
}
