// probe 672 -- binary &&
package main

//go:noinline
func op_672(a int32, b int32) bool {
	return a && b
}

var ga int32
var gb int32
var sink interface{}

func main() {
	sink = op_672(ga, gb)
	_ = sink
}
