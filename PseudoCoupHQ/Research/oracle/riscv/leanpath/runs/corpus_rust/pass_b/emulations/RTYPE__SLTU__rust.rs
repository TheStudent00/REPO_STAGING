// probe 332 -- binary <
#[no_mangle]
pub fn op_332(a: u64, b: u64) -> bool {
    a < b
}


#[no_mangle]
pub extern "C" fn emu_RTYPE__SLTU(a: u64, b: u64) -> u64 {
    ((op_332((a) as u64, (b) as u64)) as u64)
}
