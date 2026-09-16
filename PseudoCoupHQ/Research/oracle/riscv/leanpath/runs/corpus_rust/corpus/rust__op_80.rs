// probe 80 -- binary &&
#[no_mangle]
pub fn op_80(a: u64, b: u64) -> bool {
    a && b
}
