// probe 325 -- binary <
#[no_mangle]
pub fn op_325(a: i64, b: i64) -> bool {
    a < b
}


#[no_mangle]
pub extern "C" fn emu_RTYPE__SLT(a: u64, b: u64) -> u64 {
    ((op_325((a) as i64, (b) as i64)) as u64)
}
