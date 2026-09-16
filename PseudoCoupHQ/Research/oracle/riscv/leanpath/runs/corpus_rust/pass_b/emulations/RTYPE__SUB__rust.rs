// probe 584 -- binary -
#[no_mangle]
pub fn op_584(a: u64, b: u64) -> <u64 as core::ops::Sub<u64>>::Output {
    a - b
}


#[no_mangle]
pub extern "C" fn emu_RTYPE__SUB(a: u64, b: u64) -> u64 {
    ((op_584((a) as u64, (b) as u64)) as u64)
}
