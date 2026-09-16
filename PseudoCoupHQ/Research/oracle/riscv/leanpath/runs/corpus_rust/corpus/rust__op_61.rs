// probe 61 -- unary .await
#[no_mangle]
pub fn op_61(a: i64) -> i64 {
    a.await
}
