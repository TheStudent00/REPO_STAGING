// probe 620 -- binary *
#[no_mangle]
pub fn op_620(a: u64, b: u64) -> <u64 as core::ops::Mul<u64>>::Output {
    a * b
}


#[no_mangle]
pub extern "C" fn emu_MUL__Low_Signed_Signed(a: u64, b: u64) -> u64 {
    ((op_620((a) as u64, (b) as u64)) as u64)
}
