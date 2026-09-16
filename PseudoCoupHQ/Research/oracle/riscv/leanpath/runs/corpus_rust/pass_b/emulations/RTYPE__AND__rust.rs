// probe 152 -- binary &
#[no_mangle]
pub fn op_152(a: u64, b: u64) -> <u64 as core::ops::BitAnd<u64>>::Output {
    a & b
}


#[no_mangle]
pub extern "C" fn emu_RTYPE__AND(a: u64, b: u64) -> u64 {
    ((op_152((a) as u64, (b) as u64)) as u64)
}
