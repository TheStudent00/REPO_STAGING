// probe 767 -- binary ...
#[no_mangle]
pub fn op_767(a: u64, b: bool) -> u64 {
    a ... b
}
