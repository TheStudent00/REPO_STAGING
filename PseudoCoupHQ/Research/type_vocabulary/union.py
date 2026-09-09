"""Union the twelve compilers' own type enumerations into one table.

Step A of the node `type_vocabulary`
(`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/
node_0_3_3_type_vocabulary/CORE_0_3_3_type_vocabulary.md`).

MEASUREMENT ONLY. Nothing here decides which entries become verified
instruments -- that is step B, and it is the owner's.

Input : raw/<language>.types.json, one per language, each holding that
        language's own enumeration verbatim with its source and its
        confidence.
Output: type_union.json  -- the union, machine-readable
        type_union.md    -- the same table in pipe form

Every union entry names the raw spellings it was built from, per
language, so no normalization is hidden. The three markers:

    x   the language's own enumeration contains this type
    ~   present but qualified -- the `raw` note says how
    .   absent from that language's own enumeration

Run:  python3 ~/Programming/PseudoCoupHQ/Research/type_vocabulary/union.py
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

LANGS = ["python", "typescript", "java", "csharp", "go", "rust",
         "ruby", "php", "kotlin", "cpp", "dart", "swift"]

ABBR = {"python": "py", "typescript": "ts", "java": "jv", "csharp": "cs",
        "go": "go", "rust": "rs", "ruby": "rb", "php": "ph",
        "kotlin": "kt", "cpp": "cp", "dart": "dt", "swift": "sw"}

# The six already verified by the harness at
# ~/Programming/PseudoCoupHQ/Research/dominant_intentions/.
VERIFIED_INSTRUMENTS = {"boolean", "integer", "float", "string", "list", "dict"}

# category "data"      -- a shape a running program holds values of
# category "machinery" -- a type the compiler manipulates but no program
#                         ever holds a value of (inference variables,
#                         wildcards, error placeholders)
ENTRIES = [
 {"key": "boolean", "label": "boolean", "category": "data",
  "note": "ruby spells it as two classes with one value each",
  "langs": {
   "python": ["x", "bool"],
   "typescript": ["x", "Boolean, BooleanLiteral"],
   "java": ["x", "BOOLEAN; descriptor Z"],
   "csharp": ["x", "ELEMENT_TYPE_BOOLEAN"],
   "go": ["x", "bool"],
   "rust": ["x", "Bool"],
   "ruby": ["x", "TrueClass, FalseClass"],
   "php": ["x", "boolean (gettype); IS_TRUE, IS_FALSE"],
   "kotlin": ["x", "BOOLEAN; kotlin.Boolean"],
   "cpp": ["x", "bool"],
   "dart": ["x", "class bool"],
   "swift": ["x", "struct Bool"]}},

 {"key": "integer", "label": "integer (fixed-width whole number)",
  "category": "data",
  "note": "python and ruby have no fixed-width integer at all; their whole"
          "-number type is arbitrary-precision and sits in the bigint row."
          " typescript has neither: `number` is the double.",
  "langs": {
   "java": ["x", "INT, BYTE, SHORT, LONG"],
   "csharp": ["x", "ELEMENT_TYPE_I1, I2, I4, I8"],
   "go": ["x", "int, int8, int16, int32, int64"],
   "rust": ["x", "Int(IntTy)"],
   "php": ["x", "integer (gettype); IS_LONG"],
   "kotlin": ["x", "BYTE, SHORT, INT, LONG"],
   "cpp": ["x", "signed char, short, int, long, long long"],
   "dart": ["x", "class int"],
   "swift": ["x", "struct Int, Int8, Int16, Int32, Int64, Int128"]}},

 {"key": "bigint", "label": "bigint (arbitrary-precision whole number)",
  "category": "data",
  "note": "swift's StaticBigInt only types a literal, it is not a value "
          "type a program computes with",
  "langs": {
   "python": ["x", "int"],
   "typescript": ["x", "BigInt, BigIntLiteral"],
   "ruby": ["x", "Integer"],
   "dart": ["x", "class BigInt"],
   "swift": ["~", "struct StaticBigInt (literal only)"]}},

 {"key": "unsigned_integer", "label": "unsigned integer", "category": "data",
  "note": "java has no unsigned type at all",
  "langs": {
   "csharp": ["x", "ELEMENT_TYPE_U1, U2, U4, U8"],
   "go": ["x", "uint, uint8, uint16, uint32, uint64"],
   "rust": ["x", "Uint(UintTy)"],
   "kotlin": ["x", "UByte, UShort, UInt, ULong"],
   "cpp": ["x", "unsigned char, unsigned short, unsigned int, "
                "unsigned long, unsigned long long"],
   "swift": ["x", "struct UInt, UInt8, UInt16, UInt32, UInt64, UInt128"]}},

 {"key": "word_integer", "label": "pointer-sized integer", "category": "data",
  "note": "the width follows the machine word rather than the source",
  "langs": {
   "csharp": ["x", "ELEMENT_TYPE_I, ELEMENT_TYPE_U"],
   "go": ["x", "uintptr"],
   "rust": ["x", "Int(IntTy)/Uint(UintTy) at isize/usize"],
   "cpp": ["~", "size_t is a typedef, not a fundamental type"],
   "swift": ["~", "struct Int is word-sized, but not a separate type"]}},

 {"key": "float", "label": "float (IEEE binary floating point)",
  "category": "data", "note": "",
  "langs": {
   "python": ["x", "float"],
   "typescript": ["x", "Number, NumberLiteral"],
   "java": ["x", "FLOAT, DOUBLE"],
   "csharp": ["x", "ELEMENT_TYPE_R4, ELEMENT_TYPE_R8"],
   "go": ["x", "float32, float64"],
   "rust": ["x", "Float(FloatTy)"],
   "ruby": ["x", "Float"],
   "php": ["x", "double (gettype); IS_DOUBLE"],
   "kotlin": ["x", "FLOAT, DOUBLE"],
   "cpp": ["x", "float, double, long double, _Float16, _Float32, "
                "_Float64, _Float128"],
   "dart": ["x", "class double"],
   "swift": ["x", "struct Double, Float, Float16, Float80"]}},

 {"key": "complex", "label": "complex number", "category": "data",
  "note": "named in the CORE's first-pass expectation; the measurement "
          "confirms it at 3 of 12",
  "langs": {
   "python": ["x", "complex"],
   "go": ["x", "complex64, complex128"],
   "ruby": ["x", "Complex"]}},

 {"key": "rational", "label": "rational number", "category": "data",
  "note": "exact fractions; only ruby ships one as a core class",
  "langs": {
   "ruby": ["x", "Rational"]}},

 {"key": "char", "label": "char / unicode scalar", "category": "data",
  "note": "python, typescript, ruby, php and dart have no character type; "
          "a one-element string stands in",
  "langs": {
   "java": ["x", "CHAR; descriptor C"],
   "csharp": ["x", "ELEMENT_TYPE_CHAR"],
   "go": ["~", "untyped rune in go/types; rune is an alias for int32, "
               "not a distinct reflect.Kind"],
   "rust": ["x", "Char"],
   "kotlin": ["x", "CHAR; kotlin.Char"],
   "cpp": ["x", "char, char8_t, char16_t, char32_t, wchar_t"],
   "swift": ["x", "struct Character; enum Unicode"]}},

 {"key": "string", "label": "string / text", "category": "data",
  "note": "java and cpp are the two whose compiler-level enumeration has "
          "no text type: java.lang.String is a DECLARED reference and "
          "std::string is a library class template",
  "langs": {
   "python": ["x", "str"],
   "typescript": ["x", "String, StringLiteral, TemplateLiteral"],
   "csharp": ["x", "ELEMENT_TYPE_STRING"],
   "go": ["x", "string"],
   "rust": ["x", "Str"],
   "ruby": ["x", "String"],
   "php": ["x", "string (gettype); IS_STRING"],
   "kotlin": ["x", "kotlin.String, kotlin.CharSequence"],
   "dart": ["x", "class String"],
   "swift": ["x", "struct String, Substring, StaticString"]}},

 {"key": "byte_buffer", "label": "byte buffer / raw bytes", "category": "data",
  "note": "three languages have byte-oriented strings instead of a "
          "separate buffer type",
  "langs": {
   "python": ["x", "bytes, bytearray, memoryview"],
   "go": ["~", "[]byte is a slice of uint8, not a distinct kind"],
   "ruby": ["~", "String is byte-oriented"],
   "php": ["~", "string is a byte string"]}},

 {"key": "list", "label": "list (growable ordered sequence)",
  "category": "data",
  "note": "java's ArrayList, csharp's List<T>, cpp's std::vector and "
          "rust's Vec are library types; none appears in those four "
          "compilers' own type enumerations",
  "langs": {
   "python": ["x", "list"],
   "typescript": ["~", "ObjectFlags ArrayLiteral, EvolvingArray; Array "
                       "itself is a lib.d.ts interface"],
   "go": ["x", "slice"],
   "rust": ["~", "Slice is a borrowed view; Vec is a library type, "
                 "absent from TyKind"],
   "ruby": ["x", "Array"],
   "php": ["x", "array (gettype)"],
   "kotlin": ["x", "kotlin.collections.List, MutableList"],
   "dart": ["x", "class List"],
   "swift": ["x", "struct Array, ContiguousArray"]}},

 {"key": "fixed_array", "label": "fixed-size array", "category": "data",
  "note": "length is part of the type",
  "langs": {
   "java": ["x", "ARRAY; descriptor ["],
   "csharp": ["x", "ELEMENT_TYPE_ARRAY, ELEMENT_TYPE_SZARRAY"],
   "go": ["x", "array"],
   "rust": ["x", "Array"],
   "kotlin": ["x", "kotlin.Array; IntArray, ByteArray, CharArray, ..."],
   "cpp": ["x", "is_array"]}},

 {"key": "slice_view", "label": "slice / view into a sequence",
  "category": "data",
  "note": "borrows storage it does not own",
  "langs": {
   "python": ["x", "memoryview"],
   "go": ["~", "a go slice is both the view and the growable list"],
   "rust": ["x", "Slice"],
   "swift": ["x", "struct ArraySlice, Slice, Substring, "
                  "UnsafeBufferPointer"]}},

 {"key": "dict", "label": "dict (key-to-value map)", "category": "data",
  "note": "a verified instrument, yet only 6 of 12 compilers enumerate "
          "it; elsewhere it is a library class",
  "langs": {
   "python": ["x", "dict, MappingProxyType"],
   "go": ["x", "map"],
   "ruby": ["x", "Hash"],
   "php": ["~", "array (gettype) -- php's one array type IS the hash map"],
   "kotlin": ["x", "kotlin.collections.Map, MutableMap, Map.Entry"],
   "dart": ["x", "class Map, class MapEntry"],
   "swift": ["x", "struct Dictionary, KeyValuePairs"]}},

 {"key": "set", "label": "set", "category": "data",
  "note": "the CORE flags this as a candidate derivation from dict",
  "langs": {
   "python": ["x", "set, frozenset"],
   "ruby": ["x", "Set"],
   "kotlin": ["x", "kotlin.collections.Set, MutableSet"],
   "dart": ["x", "class Set"],
   "swift": ["x", "struct Set; protocol SetAlgebra"]}},

 {"key": "tuple", "label": "tuple (fixed-arity heterogeneous product)",
  "category": "data", "note": "",
  "langs": {
   "python": ["x", "tuple"],
   "typescript": ["x", "ObjectFlags Tuple"],
   "go": ["~", "go/types Tuple exists only for call signatures, never as "
               "a value type"],
   "rust": ["x", "Tuple"],
   "kotlin": ["~", "Pair, Triple are stdlib types, not a language form"],
   "dart": ["x", "class Record"],
   "swift": ["x", "Mirror.DisplayStyle tuple"]}},

 {"key": "struct", "label": "struct / record (named product, no identity)",
  "category": "data", "note": "",
  "langs": {
   "python": ["~", "SimpleNamespace; no struct form in the type table"],
   "csharp": ["x", "ELEMENT_TYPE_VALUETYPE"],
   "go": ["x", "struct"],
   "rust": ["x", "Adt"],
   "ruby": ["x", "Struct, Data"],
   "cpp": ["x", "is_class, is_union"],
   "swift": ["x", "Mirror.DisplayStyle struct"]}},

 {"key": "class_object", "label": "class / object with identity",
  "category": "data",
  "note": "go and rust have no class form at all",
  "langs": {
   "python": ["x", "object, type"],
   "typescript": ["x", "ObjectFlags Class"],
   "java": ["x", "DECLARED; classfile REFERENCE"],
   "csharp": ["x", "ELEMENT_TYPE_CLASS, ELEMENT_TYPE_OBJECT"],
   "ruby": ["x", "Object, BasicObject, Class"],
   "php": ["x", "object (gettype); IS_OBJECT"],
   "kotlin": ["x", "kotlin.Any"],
   "cpp": ["x", "is_class"],
   "dart": ["x", "class Object"],
   "swift": ["x", "Mirror.DisplayStyle class"]}},

 {"key": "enum_variant", "label": "enum / tagged variant",
  "category": "data",
  "note": "java's TypeKind has no enum entry (an enum is a DECLARED "
          "class) and csharp's CorElementType has none either (an enum "
          "is a VALUETYPE)",
  "langs": {
   "typescript": ["x", "Enum, EnumLiteral"],
   "rust": ["x", "Adt"],
   "php": ["~", "UnitEnum, BackedEnum -- enums are objects with "
                "marker interfaces"],
   "kotlin": ["x", "kotlin.Enum"],
   "cpp": ["x", "is_enum"],
   "dart": ["x", "class Enum"],
   "swift": ["x", "Mirror.DisplayStyle enum"]}},

 {"key": "range", "label": "range / interval", "category": "data",
  "note": "",
  "langs": {
   "python": ["x", "range"],
   "ruby": ["x", "Range"],
   "kotlin": ["x", "kotlin.ranges.IntRange, kotlin.ranges.LongRange"],
   "swift": ["x", "struct Range, ClosedRange, PartialRangeFrom, "
                  "PartialRangeThrough, PartialRangeUpTo"]}},

 {"key": "iterator", "label": "iterator / sequence", "category": "data",
  "note": "swift's ~40 lazy and adapter sequence types fold here",
  "langs": {
   "python": ["x", "GeneratorType, enumerate, filter, map, reversed, zip"],
   "ruby": ["x", "Enumerator, Enumerable"],
   "php": ["x", "Iterator, Traversable, IteratorAggregate"],
   "kotlin": ["x", "kotlin.collections.Iterator, Iterable, ListIterator"],
   "dart": ["x", "class Iterator, class Iterable"],
   "swift": ["x", "protocol Sequence, IteratorProtocol; struct "
                  "AnyIterator, AnySequence, LazySequence"]}},

 {"key": "function", "label": "function (a callable value)",
  "category": "data", "note": "",
  "langs": {
   "python": ["x", "FunctionType, LambdaType, BuiltinFunctionType, "
                   "MethodType"],
   "typescript": ["~", "no TypeFlags entry; function types are Object "
                       "types carrying call signatures"],
   "java": ["x", "EXECUTABLE"],
   "csharp": ["x", "ELEMENT_TYPE_FNPTR"],
   "go": ["x", "func; go/types Signature"],
   "rust": ["x", "FnDef, FnPtr"],
   "ruby": ["x", "Proc, Method, UnboundMethod"],
   "php": ["~", "Closure is a class; `callable` is a declaration-position "
                "type name"],
   "kotlin": ["x", "kotlin.Function"],
   "cpp": ["x", "is_function"],
   "dart": ["x", "class Function"],
   "swift": ["~", "function types are structural; the stdlib has no "
                  "nominal function type"]}},

 {"key": "closure_coroutine",
  "label": "closure / coroutine / generator (callable carrying state)",
  "category": "data",
  "note": "rustc gives these four TyKind variants of their own, which is "
          "why they earn a row separate from function",
  "langs": {
   "python": ["x", "CoroutineType, GeneratorType, AsyncGeneratorType, "
                   "CellType"],
   "rust": ["x", "Closure, Coroutine, CoroutineClosure, "
                 "CoroutineWitness"],
   "ruby": ["x", "Proc, Fiber, Enumerator"],
   "php": ["x", "Closure, Generator, Fiber"]}},

 {"key": "pointer", "label": "pointer (raw machine address)",
  "category": "data", "note": "",
  "langs": {
   "csharp": ["x", "ELEMENT_TYPE_PTR"],
   "go": ["x", "ptr, unsafe.Pointer"],
   "rust": ["x", "RawPtr"],
   "cpp": ["x", "is_pointer, is_member_object_pointer, "
                "is_member_function_pointer"],
   "swift": ["x", "struct UnsafePointer, UnsafeMutablePointer, "
                  "OpaquePointer"]}},

 {"key": "reference", "label": "reference (alias for another's storage)",
  "category": "data", "note": "",
  "langs": {
   "csharp": ["x", "ELEMENT_TYPE_BYREF, ELEMENT_TYPE_TYPEDBYREF"],
   "rust": ["x", "Ref"],
   "php": ["~", "IS_REFERENCE is a zval tag, not a declarable type"],
   "cpp": ["x", "is_lvalue_reference, is_rvalue_reference"]}},

 {"key": "weak_reference", "label": "weak reference", "category": "data",
  "note": "php's WeakReference/WeakMap are core classes, but this "
          "measurement does not read presence off php's class list "
          "(decision 6), so php is marked qualified",
  "langs": {
   "python": ["~", "weakref is a stdlib module, not a builtin type"],
   "php": ["~", "WeakReference, WeakMap (class list, not used for "
                "presence)"],
   "dart": ["x", "final class WeakReference, class Expando, "
                 "abstract final class Finalizer"]}},

 {"key": "channel", "label": "channel (typed queue between tasks)",
  "category": "data",
  "note": "the CORE's own example of a single-language type that stays in",
  "langs": {
   "go": ["x", "chan; go/types Chan"],
   "ruby": ["~", "Queue, SizedQueue are core classes, but thread queues "
                 "rather than a type form"]}},

 {"key": "symbol", "label": "symbol / interned name", "category": "data",
  "note": "",
  "langs": {
   "typescript": ["x", "ESSymbol, UniqueESSymbol"],
   "ruby": ["x", "Symbol"],
   "dart": ["x", "abstract class Symbol"]}},

 {"key": "regexp", "label": "regular expression", "category": "data",
  "note": "",
  "langs": {
   "ruby": ["x", "Regexp, MatchData"],
   "dart": ["x", "class RegExp, RegExpMatch, Pattern, Match"]}},

 {"key": "datetime", "label": "date-time / duration", "category": "data",
  "note": "",
  "langs": {
   "ruby": ["x", "Time"],
   "dart": ["x", "class DateTime, class Duration"],
   "swift": ["x", "struct Duration; protocol InstantProtocol"]}},

 {"key": "optional", "label": "optional wrapper (adds absence to a type)",
  "category": "data",
  "note": "rust's Option is a library enum with no TyKind of its own; "
          "three languages spell optionality as a modifier rather than "
          "a type",
  "langs": {
   "typescript": ["~", "modelled as a union with Undefined"],
   "rust": ["~", "Option is a library enum, absent from TyKind"],
   "kotlin": ["~", "T? is a modifier the compiler tracks, not a builtin "
                   "classifier"],
   "dart": ["~", "T? is a modifier"],
   "swift": ["x", "enum Optional"]}},

 {"key": "null_type", "label": "the absent value's own type (null/nil/None)",
  "category": "data",
  "note": "csharp, rust, kotlin and swift give the absent value no type "
          "of its own",
  "langs": {
   "python": ["x", "NoneType"],
   "typescript": ["x", "Null and Undefined -- two of them"],
   "java": ["x", "NULL"],
   "go": ["x", "untyped nil"],
   "ruby": ["x", "NilClass"],
   "php": ["x", "NULL (gettype); IS_NULL"],
   "cpp": ["x", "is_null_pointer"],
   "dart": ["x", "final class Null"]}},

 {"key": "void_unit", "label": "void / unit (no meaningful value)",
  "category": "data",
  "note": "half the set has a real type here and half fakes it with the "
          "absent value or with no return at all",
  "langs": {
   "python": ["~", "None doubles as the unit value"],
   "typescript": ["x", "Void"],
   "java": ["x", "VOID; descriptor V"],
   "csharp": ["x", "ELEMENT_TYPE_VOID"],
   "go": ["~", "a function may return nothing; there is no unit type"],
   "rust": ["~", "the empty Tuple is the unit"],
   "ruby": ["~", "nil doubles as unit"],
   "php": ["~", "void is a declaration-position type name"],
   "kotlin": ["x", "kotlin.Unit"],
   "cpp": ["x", "is_void"],
   "dart": ["~", "void is a language keyword, not a dart:core "
                 "declaration"],
   "swift": ["x", "typealias Void"]}},

 {"key": "never", "label": "never / bottom (the type with no values)",
  "category": "data", "note": "",
  "langs": {
   "typescript": ["x", "Never"],
   "rust": ["x", "Never"],
   "php": ["~", "never is a declaration-position return type"],
   "kotlin": ["x", "kotlin.Nothing"],
   "dart": ["~", "Never is in dart's type system but is not declared in "
                 "dart:core"],
   "swift": ["x", "enum Never"]}},

 {"key": "any_top", "label": "any / top (every value belongs to it)",
  "category": "data", "note": "",
  "langs": {
   "python": ["x", "object"],
   "typescript": ["x", "Any and Unknown -- two of them"],
   "java": ["~", "java.lang.Object is a DECLARED reference, not a "
                 "TypeKind"],
   "csharp": ["x", "ELEMENT_TYPE_OBJECT"],
   "go": ["~", "the empty interface"],
   "ruby": ["x", "BasicObject, Object"],
   "php": ["~", "mixed is a declaration-position type name"],
   "kotlin": ["x", "kotlin.Any"],
   "dart": ["x", "class Object"],
   "swift": ["x", "typealias AnyObject"]}},

 {"key": "interface", "label": "interface / protocol (dispatch, no storage)",
  "category": "data", "note": "",
  "langs": {
   "typescript": ["x", "ObjectFlags Interface"],
   "java": ["~", "DECLARED covers classes and interfaces alike"],
   "csharp": ["~", "ELEMENT_TYPE_CLASS covers both"],
   "go": ["x", "interface; go/types Interface"],
   "rust": ["x", "Dynamic"],
   "ruby": ["~", "Module"],
   "php": ["~", "Traversable, Stringable, Countable, ArrayAccess"],
   "swift": ["x", "protocol Equatable, Hashable, Comparable, Sequence"]}},

 {"key": "type_object", "label": "runtime type object (a value denoting a type)",
  "category": "data", "note": "",
  "langs": {
   "python": ["x", "type"],
   "ruby": ["x", "Class, Module"],
   "kotlin": ["x", "kotlin.reflect.KClass, kotlin.reflect.KType"],
   "dart": ["x", "abstract interface class Type"],
   "swift": ["~", "metatypes T.Type are a language form with no stdlib "
                  "nominal type"]}},

 {"key": "error_type", "label": "error / exception type", "category": "data",
  "note": "rust's TyKind::Error is NOT this -- it is the compiler's "
          "marker for a type it could not compute, and it is filed under "
          "the compiler-placeholder row instead",
  "langs": {
   "python": ["x", "BaseException"],
   "java": ["~", "Throwable is a DECLARED class"],
   "go": ["~", "error is a universe-scope interface, not a BasicKind"],
   "ruby": ["x", "Exception"],
   "php": ["x", "Throwable"],
   "kotlin": ["x", "kotlin.Throwable"],
   "dart": ["x", "class Error, abstract interface class Exception"],
   "swift": ["x", "protocol Error; enum DecodingError, EncodingError"]}},

 {"key": "result_either", "label": "result / either", "category": "data",
  "note": "",
  "langs": {
   "rust": ["~", "Result is a library enum, absent from TyKind"],
   "kotlin": ["x", "Result"],
   "swift": ["x", "enum Result"]}},

 {"key": "lazy", "label": "lazy value (computed on first read)",
  "category": "data", "note": "",
  "langs": {
   "kotlin": ["x", "Lazy, LazyThreadSafetyMode"]}},

 {"key": "atomic", "label": "atomic cell", "category": "data", "note": "",
  "langs": {
   "kotlin": ["x", "kotlin.concurrent.atomics.AtomicInt, AtomicLong, "
                   "AtomicBoolean, AtomicReference, AtomicArray"]}},

 {"key": "simd", "label": "SIMD vector", "category": "data", "note": "",
  "langs": {
   "swift": ["x", "struct SIMD2, SIMD3, SIMD4, SIMD8, SIMD16, SIMD32, "
                  "SIMD64, SIMDMask; protocol SIMD, SIMDScalar"]}},

 {"key": "key_path", "label": "key path / property reference",
  "category": "data", "note": "",
  "langs": {
   "python": ["~", "property is a descriptor object"],
   "kotlin": ["x", "kotlin.reflect.KProperty0, KProperty1, KProperty2, "
                   "KMutableProperty0"],
   "swift": ["x", "class KeyPath, WritableKeyPath, "
                  "ReferenceWritableKeyPath, PartialKeyPath, "
                  "AnyKeyPath"]}},

 {"key": "module_type", "label": "module / package as a type",
  "category": "data", "note": "",
  "langs": {
   "python": ["x", "ModuleType"],
   "java": ["x", "PACKAGE, MODULE"],
   "ruby": ["~", "Module doubles as the mixin form"]}},

 {"key": "uri", "label": "uri", "category": "data",
  "note": "the weakest data entry: parsed text that only dart puts in "
          "its core",
  "langs": {
   "dart": ["x", "abstract interface class Uri, final class UriData"]}},

 {"key": "text_builder", "label": "text builder (mutable text accumulator)",
  "category": "data",
  "note": "java's StringBuilder and python's io.StringIO are library "
          "types; only dart's core declares one",
  "langs": {
   "dart": ["x", "class StringBuffer, abstract interface class "
                 "StringSink"]}},

 # ---------------------------------------------------------------- machinery

 {"key": "union_type", "label": "union type (a value is one of several)",
  "category": "machinery",
  "note": "cpp's is_union is overlapping storage, a different thing from "
          "a type-level union",
  "langs": {
   "python": ["x", "UnionType"],
   "typescript": ["x", "Union, UnionOrIntersection"],
   "java": ["x", "UNION"],
   "go": ["x", "go/types Union"],
   "php": ["~", "union type declarations (A|B); "
                "ReflectionUnionType"],
   "cpp": ["~", "is_union is overlapping storage, not a type-level "
                "union"]}},

 {"key": "intersection_type", "label": "intersection type",
  "category": "machinery", "note": "",
  "langs": {
   "typescript": ["x", "Intersection"],
   "java": ["x", "INTERSECTION"],
   "php": ["~", "intersection type declarations (A&B); "
                "ReflectionIntersectionType"]}},

 {"key": "type_parameter", "label": "type parameter / generic variable",
  "category": "machinery", "note": "",
  "langs": {
   "typescript": ["x", "TypeParameter, TypeVariable"],
   "java": ["x", "TYPEVAR"],
   "csharp": ["x", "ELEMENT_TYPE_VAR, ELEMENT_TYPE_MVAR"],
   "go": ["x", "go/types TypeParam"],
   "rust": ["x", "Param, Bound, Placeholder"]}},

 {"key": "wildcard", "label": "wildcard (bounded unknown type argument)",
  "category": "machinery",
  "note": "java alone gives this a type kind",
  "langs": {
   "java": ["x", "WILDCARD"]}},

 {"key": "applied_generic",
  "label": "applied generic (a generic with its arguments filled in)",
  "category": "machinery", "note": "",
  "langs": {
   "typescript": ["x", "ObjectFlags Reference, Instantiated"],
   "csharp": ["x", "ELEMENT_TYPE_GENERICINST"],
   "go": ["~", "go/types Named"],
   "rust": ["~", "Adt carries GenericArgs"]}},

 {"key": "type_alias", "label": "type alias", "category": "machinery",
  "note": "",
  "langs": {
   "go": ["x", "go/types Alias"],
   "rust": ["x", "Alias; AliasTyKind Projection, Inherent, Opaque, Free"],
   "swift": ["x", "typealias Void, AnyObject, Codable, Float32"]}},

 {"key": "literal_type", "label": "literal type / untyped constant",
  "category": "machinery",
  "note": "two compilers carry a whole level between the literal and "
          "its eventual type",
  "langs": {
   "typescript": ["x", "StringLiteral, NumberLiteral, BooleanLiteral, "
                       "BigIntLiteral, TemplateLiteral"],
   "go": ["x", "untyped bool, untyped int, untyped rune, untyped float, "
               "untyped complex, untyped string"],
   "rust": ["~", "InferTy IntVar and FloatVar hold an undecided literal "
                 "type"]}},

 {"key": "type_operator",
  "label": "type operator (conditional, keyof, indexed access, mapped)",
  "category": "machinery",
  "note": "typescript alone computes types from other types",
  "langs": {
   "typescript": ["x", "Conditional, Index, IndexedAccess, StringMapping; "
                       "ObjectFlags Mapped, ReverseMapped"]}},

 {"key": "opaque_foreign",
  "label": "opaque / foreign type (layout unknown to the language)",
  "category": "machinery", "note": "",
  "langs": {
   "csharp": ["~", "ELEMENT_TYPE_INTERNAL"],
   "rust": ["x", "Foreign; AliasTyKind Opaque"],
   "swift": ["~", "struct OpaquePointer is a pointer, not an opaque "
                  "type"]}},

 {"key": "unsafe_binder", "label": "unsafe binder (lifetime-erased type)",
  "category": "machinery",
  "note": "rust alone",
  "langs": {
   "rust": ["x", "UnsafeBinder"]}},

 {"key": "pattern_type",
  "label": "pattern-restricted type (values narrowed by a pattern)",
  "category": "machinery",
  "note": "rust alone",
  "langs": {
   "rust": ["x", "Pat"]}},

 {"key": "compiler_placeholder",
  "label": "compiler-internal placeholder (inference var, error, sentinel)",
  "category": "machinery",
  "note": "no program ever holds one of these; they exist so the "
          "compiler can keep going",
  "langs": {
   "typescript": ["x", "Substitution, Reserved1, Reserved2"],
   "java": ["x", "ERROR, NONE, OTHER"],
   "csharp": ["x", "ELEMENT_TYPE_END, ELEMENT_TYPE_INTERNAL, "
                   "ELEMENT_TYPE_MAX, ELEMENT_TYPE_MODIFIER, "
                   "ELEMENT_TYPE_SENTINEL, ELEMENT_TYPE_PINNED, "
                   "ELEMENT_TYPE_CMOD_REQD, ELEMENT_TYPE_CMOD_OPT"],
   "go": ["x", "invalid; invalid type"],
   "rust": ["x", "Infer, Error; InferTy TyVar, FreshTy"],
   "php": ["~", "IS_UNDEF"]}},
]


def load_raw():
    """Return {language: the whole raw file's names joined into one string}."""
    blobs = {}
    for lang in LANGS:
        path = os.path.join(RAW, lang + ".types.json")
        with open(path) as handle:
            doc = json.load(handle)
        names = []
        for group in doc["enumerations"]:
            names.extend(group["names"])
        blobs[lang] = "\n".join(names)
    return blobs


def check_citations(blobs):
    """Warn where a cited raw spelling is nowhere in that language's raw file.

    This is the guard on the one place hand work enters: the `raw` string
    in each cell. A cell passes if at least one of its identifier-shaped
    tokens appears in the language's own enumeration.
    """
    strict, loose = [], []
    for entry in ENTRIES:
        for lang, (marker, raw) in entry["langs"].items():
            tokens = [t for t in re.findall(r"[A-Za-z_][A-Za-z0-9_.]{2,}", raw)]
            if not tokens:
                continue
            if not any(t in blobs[lang] for t in tokens):
                (strict if marker == "x" else loose).append(
                    (entry["key"], lang, marker, raw))
    return strict, loose


def build():
    blobs = load_raw()
    strict, loose = check_citations(blobs)

    rows = []
    for entry in ENTRIES:
        present = {}
        for lang in LANGS:
            marker, raw = entry["langs"].get(lang, [".", ""])
            present[lang] = {"marker": marker, "raw": raw}
        hard = [l for l in LANGS if present[l]["marker"] == "x"]
        soft = [l for l in LANGS if present[l]["marker"] == "~"]
        rows.append({
            "key": entry["key"],
            "label": entry["label"],
            "category": entry["category"],
            "already_verified_instrument": entry["key"] in VERIFIED_INSTRUMENTS,
            "languages_present": hard,
            "languages_qualified": soft,
            "count_present": len(hard),
            "count_with_qualified": len(hard) + len(soft),
            "reach": ("single-language" if len(hard) <= 1 else "shared"),
            "note": entry["note"],
            "per_language": present,
        })

    single = [r for r in rows if r["reach"] == "single-language"]
    doc = {
        "what": "the union of the twelve target compilers' own type "
                "enumerations, step A of the node type_vocabulary",
        "measured": "2026-08-16",
        "languages": LANGS,
        "markers": {"x": "present in that language's own enumeration",
                    "~": "present but qualified; the raw field says how",
                    ".": "absent from that language's own enumeration"},
        "totals": {
            "union_size": len(rows),
            "data_entries": len([r for r in rows if r["category"] == "data"]),
            "machinery_entries":
                len([r for r in rows if r["category"] == "machinery"]),
            "already_verified_instruments":
                len([r for r in rows if r["already_verified_instrument"]]),
            "new_entries":
                len(rows) - len([r for r in rows
                                 if r["already_verified_instrument"]]),
            "single_language_entries": len(single),
        },
        "citation_check": {
            "present_cells_with_no_matching_raw_name": [
                {"entry": k, "language": l, "marker": m, "raw": r}
                for (k, l, m, r) in strict],
            "qualified_cells_whose_note_is_prose": [
                {"entry": k, "language": l, "marker": m, "raw": r}
                for (k, l, m, r) in loose],
        },
        "entries": rows,
    }

    with open(os.path.join(HERE, "type_union.json"), "w") as handle:
        json.dump(doc, handle, indent=2)
        handle.write("\n")

    with open(os.path.join(HERE, "type_union.md"), "w") as handle:
        handle.write(markdown_table(rows))

    return doc, strict, loose


def markdown_table(rows):
    head = "| type entry | " + " | ".join(ABBR[l] for l in LANGS) + \
           " | n | instrument | notes |"
    rule = "|---|" + "---|" * len(LANGS) + "---|---|---|"
    out = [head, rule]
    for r in rows:
        cells = [r["per_language"][l]["marker"] for l in LANGS]
        note = r["note"].replace("\n", " ")
        if r["category"] == "machinery":
            note = ("MACHINERY. " + note) if note else "MACHINERY."
        out.append("| " + r["label"] + " | " + " | ".join(cells) + " | " +
                   str(r["count_present"]) + " | " +
                   ("yes" if r["already_verified_instrument"] else "no") +
                   " | " + note + " |")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    doc, strict, loose = build()
    t = doc["totals"]
    print("union size            :", t["union_size"])
    print("  data entries        :", t["data_entries"])
    print("  machinery entries   :", t["machinery_entries"])
    print("already instruments   :", t["already_verified_instruments"])
    print("new entries           :", t["new_entries"])
    print("single-language       :", t["single_language_entries"])
    print("x-cells with no matching raw name:", len(strict))
    for m in strict:
        print("   UNBACKED", m)
    print("~-cells whose note is prose      :", len(loose))
    print("")
    print("single-language entries:")
    for r in doc["entries"]:
        if r["reach"] == "single-language":
            who = r["languages_present"] or ["(qualified only)"]
            print("   %-58s %s" % (r["label"], ",".join(who)))
