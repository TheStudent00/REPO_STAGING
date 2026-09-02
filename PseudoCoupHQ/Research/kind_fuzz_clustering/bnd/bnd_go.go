
package main

import (
	"fmt"
	"math"
	"math/big"
	"os"
	"reflect"
	"sort"
	"strings"
)

var EXACT = map[string]bool{"+": true, "-": true, "*": true, "<": true,
	"<=": true, ">": true, ">=": true, "==": true, "!=": true}

func wantv(op string, a, b *big.Int) interface{} {
	if !EXACT[op] {
		return nil
	}
	switch op {
	case "+":
		return new(big.Int).Add(a, b)
	case "-":
		return new(big.Int).Sub(a, b)
	case "*":
		return new(big.Int).Mul(a, b)
	case "<":
		return a.Cmp(b) < 0
	case "<=":
		return a.Cmp(b) <= 0
	case ">":
		return a.Cmp(b) > 0
	case ">=":
		return a.Cmp(b) >= 0
	case "==":
		return a.Cmp(b) == 0
	case "!=":
		return a.Cmp(b) != 0
	}
	return nil
}

func asint(r interface{}) interface{} {
	switch v := r.(type) {
	case bool:
		return v
	case int:
		return big.NewInt(int64(v))
	case int32:
		return big.NewInt(int64(v))
	case int64:
		return big.NewInt(v)
	case uint64:
		return new(big.Int).SetUint64(v)
	case float64:
		if math.IsNaN(v) || math.IsInf(v, 0) {
			return nil
		}
		if v != math.Trunc(v) {
			return "NONINT"
		}
		f := new(big.Float).SetFloat64(v)
		i, _ := f.Int(nil)
		return i
	case float32:
		return asint(float64(v))
	}
	return nil
}

func fidv(r interface{}, op string, a, b *big.Int) string {
	w := wantv(op, a, b)
	if w == nil {
		return "na"
	}
	g := asint(r)
	if g == nil {
		return "na"
	}
	if wb, ok := w.(bool); ok {
		gb, ok2 := g.(bool)
		if !ok2 {
			return "na"
		}
		if wb == gb {
			return "exact"
		}
		return "inexact"
	}
	if _, ok := g.(bool); ok {
		return "na"
	}
	if s, ok := g.(string); ok && s == "NONINT" {
		return "inexact"
	}
	if g.(*big.Int).Cmp(w.(*big.Int)) == 0 {
		return "exact"
	}
	return "inexact"
}

func sigv(fn func(*big.Int) interface{}, c *big.Int, op string,
	a, b *big.Int) (out string) {
	defer func() {
		if e := recover(); e != nil {
			out = fmt.Sprintf("raise|%v|na", e)
		}
	}()
	r := fn(c)
	tn := "null"
	if r != nil {
		tn = reflect.TypeOf(r).String()
	}
	return "answer|" + tn + "|" + fidv(r, op, a, b)
}

func bisect(tid int, fn func(*big.Int) interface{}, op string,
	lov, hiv, fixedv *big.Int, varyIsLhs bool) int {
	s := func(c *big.Int) string {
		a, b := c, fixedv
		if !varyIsLhs {
			a, b = fixedv, c
		}
		return sigv(fn, c, op, a, b)
	}
	lo := new(big.Int).Set(lov)
	hi := new(big.Int).Set(hiv)
	slo, shi := s(lo), s(hi)
	probes := 2
	if slo == shi {
		fmt.Printf("N|%d|%s|%s\n", tid, slo, shi)
		return probes
	}
	other := map[string]bool{}
	one := big.NewInt(1)
	for new(big.Int).Sub(hi, lo).Cmp(one) > 0 {
		mid := new(big.Int).Rsh(new(big.Int).Add(lo, hi), 1)
		sm := s(mid)
		probes++
		if sm == slo {
			lo = mid
		} else {
			if sm != shi {
				other[sm] = true
			}
			hi = mid
		}
	}
	keys := []string{}
	for k := range other {
		keys = append(keys, k)
	}
	sort.Strings(keys)
	fmt.Printf("B|%d|%s|%s|%s|%s|%d|%s\n", tid, lo.String(), hi.String(),
		slo, shi, probes, strings.Join(keys, ";"))
	return probes
}

var TARGETS []func() int

func mustBig(s string) *big.Int {
	v, _ := new(big.Int).SetString(s, 10)
	return v
}

func reg() {
	TARGETS = append(TARGETS, func() int { var f int64 = 42; return bisect(0, func(c *big.Int) interface{} { return ((c.Int64()) + (f)) }, "+", mustBig("9007199254740993"), mustBig("9223372036854775807"), mustBig("42"), true) })
	TARGETS = append(TARGETS, func() int { var f int64 = 42; return bisect(1, func(c *big.Int) interface{} { return ((c.Int64()) * (f)) }, "*", mustBig("9007199254740993"), mustBig("9223372036854775807"), mustBig("42"), true) })
	TARGETS = append(TARGETS, func() int { var f int64 = 9223372036854775807; return bisect(2, func(c *big.Int) interface{} { return ((c.Int64()) + (f)) }, "+", mustBig("0"), mustBig("42"), mustBig("9223372036854775807"), true) })
	TARGETS = append(TARGETS, func() int { var f int64 = 9223372036854775807; return bisect(3, func(c *big.Int) interface{} { return ((c.Int64()) * (f)) }, "*", mustBig("0"), mustBig("42"), mustBig("9223372036854775807"), true) })
	TARGETS = append(TARGETS, func() int { var f int64 = 9007199254740993; return bisect(4, func(c *big.Int) interface{} { return ((c.Int64()) + (f)) }, "+", mustBig("9007199254740993"), mustBig("9223372036854775807"), mustBig("9007199254740993"), true) })
	TARGETS = append(TARGETS, func() int { var f int64 = 9007199254740993; return bisect(5, func(c *big.Int) interface{} { return ((c.Int64()) * (f)) }, "*", mustBig("42"), mustBig("9007199254740993"), mustBig("9007199254740993"), true) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 42; return bisect(6, func(c *big.Int) interface{} { return ((c.Uint64()) + (f)) }, "+", mustBig("9223372036854775808"), mustBig("18446744073709551615"), mustBig("42"), true) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 42; return bisect(7, func(c *big.Int) interface{} { return ((c.Uint64()) - (f)) }, "-", mustBig("0"), mustBig("42"), mustBig("42"), true) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 42; return bisect(8, func(c *big.Int) interface{} { return ((c.Uint64()) * (f)) }, "*", mustBig("9007199254740993"), mustBig("9223372036854775807"), mustBig("42"), true) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9223372036854775807; return bisect(9, func(c *big.Int) interface{} { return ((c.Uint64()) + (f)) }, "+", mustBig("9223372036854775808"), mustBig("18446744073709551615"), mustBig("9223372036854775807"), true) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9223372036854775807; return bisect(10, func(c *big.Int) interface{} { return ((c.Uint64()) - (f)) }, "-", mustBig("9007199254740993"), mustBig("9223372036854775807"), mustBig("9223372036854775807"), true) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9223372036854775807; return bisect(11, func(c *big.Int) interface{} { return ((c.Uint64()) * (f)) }, "*", mustBig("0"), mustBig("42"), mustBig("9223372036854775807"), true) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9223372036854775808; return bisect(12, func(c *big.Int) interface{} { return ((c.Uint64()) * (f)) }, "*", mustBig("0"), mustBig("42"), mustBig("9223372036854775808"), true) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9007199254740993; return bisect(13, func(c *big.Int) interface{} { return ((c.Uint64()) + (f)) }, "+", mustBig("9223372036854775808"), mustBig("18446744073709551615"), mustBig("9007199254740993"), true) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9007199254740993; return bisect(14, func(c *big.Int) interface{} { return ((c.Uint64()) - (f)) }, "-", mustBig("42"), mustBig("9007199254740993"), mustBig("9007199254740993"), true) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9007199254740993; return bisect(15, func(c *big.Int) interface{} { return ((c.Uint64()) * (f)) }, "*", mustBig("42"), mustBig("9007199254740993"), mustBig("9007199254740993"), true) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 18446744073709551615; return bisect(16, func(c *big.Int) interface{} { return ((c.Uint64()) + (f)) }, "+", mustBig("0"), mustBig("42"), mustBig("18446744073709551615"), true) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 18446744073709551615; return bisect(17, func(c *big.Int) interface{} { return ((c.Uint64()) - (f)) }, "-", mustBig("9223372036854775808"), mustBig("18446744073709551615"), mustBig("18446744073709551615"), true) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 18446744073709551615; return bisect(18, func(c *big.Int) interface{} { return ((c.Uint64()) * (f)) }, "*", mustBig("0"), mustBig("42"), mustBig("18446744073709551615"), true) })
	TARGETS = append(TARGETS, func() int { var f int = 42; return bisect(19, func(c *big.Int) interface{} { return ((int(c.Int64())) + (f)) }, "+", mustBig("9007199254740993"), mustBig("9223372036854775807"), mustBig("42"), true) })
	TARGETS = append(TARGETS, func() int { var f int = 42; return bisect(20, func(c *big.Int) interface{} { return ((int(c.Int64())) * (f)) }, "*", mustBig("9007199254740993"), mustBig("9223372036854775807"), mustBig("42"), true) })
	TARGETS = append(TARGETS, func() int { var f int = 9223372036854775807; return bisect(21, func(c *big.Int) interface{} { return ((int(c.Int64())) + (f)) }, "+", mustBig("0"), mustBig("42"), mustBig("9223372036854775807"), true) })
	TARGETS = append(TARGETS, func() int { var f int = 9223372036854775807; return bisect(22, func(c *big.Int) interface{} { return ((int(c.Int64())) * (f)) }, "*", mustBig("0"), mustBig("42"), mustBig("9223372036854775807"), true) })
	TARGETS = append(TARGETS, func() int { var f int = 9007199254740993; return bisect(23, func(c *big.Int) interface{} { return ((int(c.Int64())) + (f)) }, "+", mustBig("9007199254740993"), mustBig("9223372036854775807"), mustBig("9007199254740993"), true) })
	TARGETS = append(TARGETS, func() int { var f int = 9007199254740993; return bisect(24, func(c *big.Int) interface{} { return ((int(c.Int64())) * (f)) }, "*", mustBig("42"), mustBig("9007199254740993"), mustBig("9007199254740993"), true) })
	TARGETS = append(TARGETS, func() int { var f int32 = 42; return bisect(25, func(c *big.Int) interface{} { return ((f) / (int32(c.Int64()))) }, "/", mustBig("0"), mustBig("42"), mustBig("42"), false) })
	TARGETS = append(TARGETS, func() int { var f int32 = 42; return bisect(26, func(c *big.Int) interface{} { return ((f) % (int32(c.Int64()))) }, "%", mustBig("0"), mustBig("42"), mustBig("42"), false) })
	TARGETS = append(TARGETS, func() int { var f int32 = 0; return bisect(27, func(c *big.Int) interface{} { return ((f) / (int32(c.Int64()))) }, "/", mustBig("0"), mustBig("42"), mustBig("0"), false) })
	TARGETS = append(TARGETS, func() int { var f int32 = 0; return bisect(28, func(c *big.Int) interface{} { return ((f) % (int32(c.Int64()))) }, "%", mustBig("0"), mustBig("42"), mustBig("0"), false) })
	TARGETS = append(TARGETS, func() int { var f int64 = 42; return bisect(29, func(c *big.Int) interface{} { return ((f) + (c.Int64())) }, "+", mustBig("9007199254740993"), mustBig("9223372036854775807"), mustBig("42"), false) })
	TARGETS = append(TARGETS, func() int { var f int64 = 42; return bisect(30, func(c *big.Int) interface{} { return ((f) * (c.Int64())) }, "*", mustBig("9007199254740993"), mustBig("9223372036854775807"), mustBig("42"), false) })
	TARGETS = append(TARGETS, func() int { var f int64 = 42; return bisect(31, func(c *big.Int) interface{} { return ((f) / (c.Int64())) }, "/", mustBig("0"), mustBig("42"), mustBig("42"), false) })
	TARGETS = append(TARGETS, func() int { var f int64 = 42; return bisect(32, func(c *big.Int) interface{} { return ((f) % (c.Int64())) }, "%", mustBig("0"), mustBig("42"), mustBig("42"), false) })
	TARGETS = append(TARGETS, func() int { var f int64 = 0; return bisect(33, func(c *big.Int) interface{} { return ((f) / (c.Int64())) }, "/", mustBig("0"), mustBig("42"), mustBig("0"), false) })
	TARGETS = append(TARGETS, func() int { var f int64 = 0; return bisect(34, func(c *big.Int) interface{} { return ((f) % (c.Int64())) }, "%", mustBig("0"), mustBig("42"), mustBig("0"), false) })
	TARGETS = append(TARGETS, func() int { var f int64 = 9223372036854775807; return bisect(35, func(c *big.Int) interface{} { return ((f) + (c.Int64())) }, "+", mustBig("0"), mustBig("42"), mustBig("9223372036854775807"), false) })
	TARGETS = append(TARGETS, func() int { var f int64 = 9223372036854775807; return bisect(36, func(c *big.Int) interface{} { return ((f) * (c.Int64())) }, "*", mustBig("0"), mustBig("42"), mustBig("9223372036854775807"), false) })
	TARGETS = append(TARGETS, func() int { var f int64 = 9223372036854775807; return bisect(37, func(c *big.Int) interface{} { return ((f) / (c.Int64())) }, "/", mustBig("0"), mustBig("42"), mustBig("9223372036854775807"), false) })
	TARGETS = append(TARGETS, func() int { var f int64 = 9223372036854775807; return bisect(38, func(c *big.Int) interface{} { return ((f) % (c.Int64())) }, "%", mustBig("0"), mustBig("42"), mustBig("9223372036854775807"), false) })
	TARGETS = append(TARGETS, func() int { var f int64 = 9007199254740993; return bisect(39, func(c *big.Int) interface{} { return ((f) + (c.Int64())) }, "+", mustBig("9007199254740993"), mustBig("9223372036854775807"), mustBig("9007199254740993"), false) })
	TARGETS = append(TARGETS, func() int { var f int64 = 9007199254740993; return bisect(40, func(c *big.Int) interface{} { return ((f) * (c.Int64())) }, "*", mustBig("42"), mustBig("9007199254740993"), mustBig("9007199254740993"), false) })
	TARGETS = append(TARGETS, func() int { var f int64 = 9007199254740993; return bisect(41, func(c *big.Int) interface{} { return ((f) / (c.Int64())) }, "/", mustBig("0"), mustBig("42"), mustBig("9007199254740993"), false) })
	TARGETS = append(TARGETS, func() int { var f int64 = 9007199254740993; return bisect(42, func(c *big.Int) interface{} { return ((f) % (c.Int64())) }, "%", mustBig("0"), mustBig("42"), mustBig("9007199254740993"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 42; return bisect(43, func(c *big.Int) interface{} { return ((f) + (c.Uint64())) }, "+", mustBig("9223372036854775808"), mustBig("18446744073709551615"), mustBig("42"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 42; return bisect(44, func(c *big.Int) interface{} { return ((f) - (c.Uint64())) }, "-", mustBig("42"), mustBig("9007199254740993"), mustBig("42"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 42; return bisect(45, func(c *big.Int) interface{} { return ((f) * (c.Uint64())) }, "*", mustBig("9007199254740993"), mustBig("9223372036854775807"), mustBig("42"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 42; return bisect(46, func(c *big.Int) interface{} { return ((f) / (c.Uint64())) }, "/", mustBig("0"), mustBig("42"), mustBig("42"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 42; return bisect(47, func(c *big.Int) interface{} { return ((f) % (c.Uint64())) }, "%", mustBig("0"), mustBig("42"), mustBig("42"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 0; return bisect(48, func(c *big.Int) interface{} { return ((f) - (c.Uint64())) }, "-", mustBig("0"), mustBig("42"), mustBig("0"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 0; return bisect(49, func(c *big.Int) interface{} { return ((f) / (c.Uint64())) }, "/", mustBig("0"), mustBig("42"), mustBig("0"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 0; return bisect(50, func(c *big.Int) interface{} { return ((f) % (c.Uint64())) }, "%", mustBig("0"), mustBig("42"), mustBig("0"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9223372036854775807; return bisect(51, func(c *big.Int) interface{} { return ((f) + (c.Uint64())) }, "+", mustBig("9223372036854775808"), mustBig("18446744073709551615"), mustBig("9223372036854775807"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9223372036854775807; return bisect(52, func(c *big.Int) interface{} { return ((f) * (c.Uint64())) }, "*", mustBig("0"), mustBig("42"), mustBig("9223372036854775807"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9223372036854775807; return bisect(53, func(c *big.Int) interface{} { return ((f) / (c.Uint64())) }, "/", mustBig("0"), mustBig("42"), mustBig("9223372036854775807"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9223372036854775807; return bisect(54, func(c *big.Int) interface{} { return ((f) % (c.Uint64())) }, "%", mustBig("0"), mustBig("42"), mustBig("9223372036854775807"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9223372036854775808; return bisect(55, func(c *big.Int) interface{} { return ((f) - (c.Uint64())) }, "-", mustBig("9223372036854775808"), mustBig("18446744073709551615"), mustBig("9223372036854775808"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9223372036854775808; return bisect(56, func(c *big.Int) interface{} { return ((f) * (c.Uint64())) }, "*", mustBig("0"), mustBig("42"), mustBig("9223372036854775808"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9223372036854775808; return bisect(57, func(c *big.Int) interface{} { return ((f) / (c.Uint64())) }, "/", mustBig("0"), mustBig("42"), mustBig("9223372036854775808"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9223372036854775808; return bisect(58, func(c *big.Int) interface{} { return ((f) % (c.Uint64())) }, "%", mustBig("0"), mustBig("42"), mustBig("9223372036854775808"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9007199254740993; return bisect(59, func(c *big.Int) interface{} { return ((f) + (c.Uint64())) }, "+", mustBig("9223372036854775808"), mustBig("18446744073709551615"), mustBig("9007199254740993"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9007199254740993; return bisect(60, func(c *big.Int) interface{} { return ((f) - (c.Uint64())) }, "-", mustBig("9007199254740993"), mustBig("9223372036854775807"), mustBig("9007199254740993"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9007199254740993; return bisect(61, func(c *big.Int) interface{} { return ((f) * (c.Uint64())) }, "*", mustBig("42"), mustBig("9007199254740993"), mustBig("9007199254740993"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9007199254740993; return bisect(62, func(c *big.Int) interface{} { return ((f) / (c.Uint64())) }, "/", mustBig("0"), mustBig("42"), mustBig("9007199254740993"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 9007199254740993; return bisect(63, func(c *big.Int) interface{} { return ((f) % (c.Uint64())) }, "%", mustBig("0"), mustBig("42"), mustBig("9007199254740993"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 18446744073709551615; return bisect(64, func(c *big.Int) interface{} { return ((f) + (c.Uint64())) }, "+", mustBig("0"), mustBig("42"), mustBig("18446744073709551615"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 18446744073709551615; return bisect(65, func(c *big.Int) interface{} { return ((f) * (c.Uint64())) }, "*", mustBig("0"), mustBig("42"), mustBig("18446744073709551615"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 18446744073709551615; return bisect(66, func(c *big.Int) interface{} { return ((f) / (c.Uint64())) }, "/", mustBig("0"), mustBig("42"), mustBig("18446744073709551615"), false) })
	TARGETS = append(TARGETS, func() int { var f uint64 = 18446744073709551615; return bisect(67, func(c *big.Int) interface{} { return ((f) % (c.Uint64())) }, "%", mustBig("0"), mustBig("42"), mustBig("18446744073709551615"), false) })
	TARGETS = append(TARGETS, func() int { var f int = 42; return bisect(68, func(c *big.Int) interface{} { return ((f) + (int(c.Int64()))) }, "+", mustBig("9007199254740993"), mustBig("9223372036854775807"), mustBig("42"), false) })
	TARGETS = append(TARGETS, func() int { var f int = 42; return bisect(69, func(c *big.Int) interface{} { return ((f) * (int(c.Int64()))) }, "*", mustBig("9007199254740993"), mustBig("9223372036854775807"), mustBig("42"), false) })
	TARGETS = append(TARGETS, func() int { var f int = 42; return bisect(70, func(c *big.Int) interface{} { return ((f) / (int(c.Int64()))) }, "/", mustBig("0"), mustBig("42"), mustBig("42"), false) })
	TARGETS = append(TARGETS, func() int { var f int = 42; return bisect(71, func(c *big.Int) interface{} { return ((f) % (int(c.Int64()))) }, "%", mustBig("0"), mustBig("42"), mustBig("42"), false) })
	TARGETS = append(TARGETS, func() int { var f int = 0; return bisect(72, func(c *big.Int) interface{} { return ((f) / (int(c.Int64()))) }, "/", mustBig("0"), mustBig("42"), mustBig("0"), false) })
	TARGETS = append(TARGETS, func() int { var f int = 0; return bisect(73, func(c *big.Int) interface{} { return ((f) % (int(c.Int64()))) }, "%", mustBig("0"), mustBig("42"), mustBig("0"), false) })
	TARGETS = append(TARGETS, func() int { var f int = 9223372036854775807; return bisect(74, func(c *big.Int) interface{} { return ((f) + (int(c.Int64()))) }, "+", mustBig("0"), mustBig("42"), mustBig("9223372036854775807"), false) })
	TARGETS = append(TARGETS, func() int { var f int = 9223372036854775807; return bisect(75, func(c *big.Int) interface{} { return ((f) * (int(c.Int64()))) }, "*", mustBig("0"), mustBig("42"), mustBig("9223372036854775807"), false) })
	TARGETS = append(TARGETS, func() int { var f int = 9223372036854775807; return bisect(76, func(c *big.Int) interface{} { return ((f) / (int(c.Int64()))) }, "/", mustBig("0"), mustBig("42"), mustBig("9223372036854775807"), false) })
	TARGETS = append(TARGETS, func() int { var f int = 9223372036854775807; return bisect(77, func(c *big.Int) interface{} { return ((f) % (int(c.Int64()))) }, "%", mustBig("0"), mustBig("42"), mustBig("9223372036854775807"), false) })
	TARGETS = append(TARGETS, func() int { var f int = 9007199254740993; return bisect(78, func(c *big.Int) interface{} { return ((f) + (int(c.Int64()))) }, "+", mustBig("9007199254740993"), mustBig("9223372036854775807"), mustBig("9007199254740993"), false) })
	TARGETS = append(TARGETS, func() int { var f int = 9007199254740993; return bisect(79, func(c *big.Int) interface{} { return ((f) * (int(c.Int64()))) }, "*", mustBig("42"), mustBig("9007199254740993"), mustBig("9007199254740993"), false) })
	TARGETS = append(TARGETS, func() int { var f int = 9007199254740993; return bisect(80, func(c *big.Int) interface{} { return ((f) / (int(c.Int64()))) }, "/", mustBig("0"), mustBig("42"), mustBig("9007199254740993"), false) })
	TARGETS = append(TARGETS, func() int { var f int = 9007199254740993; return bisect(81, func(c *big.Int) interface{} { return ((f) % (int(c.Int64()))) }, "%", mustBig("0"), mustBig("42"), mustBig("9007199254740993"), false) })
}

func main() {
	reg()
	total := 0
	n := len(TARGETS)
	for k := 0; k < n; k++ {
		total += TARGETS[k]()
		if (k+1)%25 == 0 || k+1 == n {
			fmt.Fprintf(os.Stderr, "progress %d/%d probes=%d\n", k+1, n, total)
		}
	}
	fmt.Fprintf(os.Stderr, "DONE targets=%d probes=%d\n", n, total)
}
