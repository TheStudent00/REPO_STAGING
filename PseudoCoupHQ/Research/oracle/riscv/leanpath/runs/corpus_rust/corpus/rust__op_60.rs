// probe 60 -- unary .await
#[no_mangle]
pub fn op_60(a: i32) -> i32 {
    a.await
}
