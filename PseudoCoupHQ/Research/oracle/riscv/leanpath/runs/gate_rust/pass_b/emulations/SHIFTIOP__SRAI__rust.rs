// probe 506 -- binary >>
#[no_mangle]
pub fn op_506(a: i64, b: u64) -> <i64 as core::ops::Shr<u64>>::Output {
    a >> b
}


#[no_mangle]
pub extern "C" fn emu_SHIFTIOP__SRAI(a: u64, shamt: u64) -> u64 {
    ((op_506((a) as i64, (shamt) as u64)) as u64)
}
