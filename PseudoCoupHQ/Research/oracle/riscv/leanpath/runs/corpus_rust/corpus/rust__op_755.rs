// probe 755 -- binary ...
#[no_mangle]
pub fn op_755(a: i32, b: bool) -> i32 {
    a ... b
}
