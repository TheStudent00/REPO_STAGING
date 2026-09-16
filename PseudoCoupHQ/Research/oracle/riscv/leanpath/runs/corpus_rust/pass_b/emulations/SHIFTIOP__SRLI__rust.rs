// probe 512 -- binary >>
#[no_mangle]
pub fn op_512(a: u64, b: u64) -> <u64 as core::ops::Shr<u64>>::Output {
    a >> b
}


#[no_mangle]
pub extern "C" fn emu_SHIFTIOP__SRLI(a: u64, shamt: u64) -> u64 {
    ((op_512((a) as u64, (shamt) as u64)) as u64)
}
