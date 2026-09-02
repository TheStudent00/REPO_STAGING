# dominant_table4 -- classes after the third candidate rule

- classes: 1025 (was 1113)
- classes of size 1: 578 (was 737)
- rows that are a merge of two or more table-3 classes: 88
- weakest evidence: {'byte': 327, 'canon-byte': 57, 'sem': 32, 'z3': 29, 'core-text': 2, 'None': 578}

## the rows that merged

| class | merged from | operand types | result | languages | members | weakest evidence |
|---|---|---|---|---|---|---|
| K0035 | K0035, K0957 | bool,None | bool | c, cpp, go, rust, swift | c `--`; cpp `not`; cpp `!`; go `!`; rust `!`; swift `!` | z3 |
| K0036 | K0036, K0993 | bool,bool | bool | cpp, go, rust, swift | cpp `not_eq`; cpp `!=`; go `!=`; rust `^`; rust `!=`; swift `!=` | z3 |
| K0062 | K0062, K0988 | i32,i32 | bool | cpp, go, rust, swift | cpp `!=`; cpp `not_eq`; go `!=`; rust `!=`; swift `!=` | z3 |
| K0063 | K0063, K0989 | i64,i64 | bool | cpp, go, rust, swift | cpp `!=`; cpp `not_eq`; go `!=`; rust `!=`; swift `!=` | z3 |
| K0064 | K0064, K0990 | u64,u64 | bool | cpp, go, rust, swift | cpp `!=`; cpp `not_eq`; go `!=`; rust `!=`; swift `!=` | z3 |
| K0124 | K0124, K0994 | i32,i32 | bool | cpp, go, rust, swift | cpp `<`; go `<`; rust `<`; swift `<` | z3 |
| K0125 | K0125, K0995 | i64,i64 | bool | cpp, go, rust, swift | cpp `<`; go `<`; rust `<`; swift `<` | z3 |
| K0126 | K0126, K0996 | u64,u64 | bool | cpp, go, rust, swift | cpp `<`; go `<`; rust `<`; swift `<` | z3 |
| K0127 | K0127, K0997 | i32,i32 | bool | cpp, go, rust, swift | cpp `>=`; go `>=`; rust `>=`; swift `>=` | z3 |
| K0128 | K0128, K0998 | i64,i64 | bool | cpp, go, rust, swift | cpp `>=`; go `>=`; rust `>=`; swift `>=` | z3 |
| K0129 | K0129, K0999 | u64,u64 | bool | cpp, go, rust, swift | cpp `>=`; go `>=`; rust `>=`; swift `>=` | z3 |
| K0130 | K0130, K0982 | i32,i32 | bool | cpp, go, rust, swift | cpp `==`; go `==`; rust `==`; swift `==` | z3 |
| K0131 | K0131, K0983 | i64,i64 | bool | cpp, go, rust, swift | cpp `==`; go `==`; rust `==`; swift `==` | z3 |
| K0132 | K0132, K0984 | u64,u64 | bool | cpp, go, rust, swift | cpp `==`; go `==`; rust `==`; swift `==` | z3 |
| K0135 | K0135, K0987 | bool,bool | bool | cpp, go, rust, swift | cpp `==`; go `==`; rust `==`; swift `==` | z3 |
| K0352 | K0352, K1070 | i32,i64 | bool | cpp, swift | cpp `!=`; cpp `not_eq`; swift `!=` | z3 |
| K0353 | K0353, K1072 | i64,i32 | bool | cpp, swift | cpp `!=`; cpp `not_eq`; swift `!=` | z3 |
| K0669 | K0669, K0756 | bool,f64 | bool | cpp | cpp `not_eq`; cpp `!=` | byte |
| K0670 | K0670, K0671 | u64,None | bool | cpp | cpp `!`; cpp `not` | byte |
| K0672 | K0672, K0682 | f32,None | bool | cpp | cpp `not`; cpp `!` | byte |
| K0673 | K0673, K0701 | f64,None | bool | cpp | cpp `not`; cpp `!` | byte |
| K0674 | K0674, K0899 | i32,u64 | bool | cpp | cpp `||`; cpp `or` | byte |
| K0675 | K0675, K0900 | i64,u64 | bool | cpp | cpp `||`; cpp `or` | byte |
| K0676 | K0676, K0901 | u64,i32 | bool | cpp | cpp `||`; cpp `or` | byte |
| K0677 | K0677, K0902 | u64,i64 | bool | cpp | cpp `||`; cpp `or` | byte |
| K0678 | K0678, K0903 | u64,u64 | bool | cpp | cpp `||`; cpp `or` | byte |
| K0679 | K0679, K0904 | u64,f32 | bool | cpp | cpp `||`; cpp `or` | byte |
| K0680 | K0680, K0905 | u64,f64 | bool | cpp | cpp `||`; cpp `or` | byte |
| K0681 | K0681, K0906 | u64,bool | bool | cpp | cpp `||`; cpp `or` | byte |
| K0683 | K0683, K0907 | f32,u64 | bool | cpp | cpp `||`; cpp `or` | byte |
| K0684 | K0684, K0908 | f64,u64 | bool | cpp | cpp `||`; cpp `or` | byte |
| K0685 | K0685, K0909 | bool,u64 | bool | cpp | cpp `||`; cpp `or` | byte |
| K0686 | K0686, K0910 | bool,f32 | bool | cpp | cpp `||`; cpp `or` | byte |
| K0687 | K0687, K0911 | bool,f64 | bool | cpp | cpp `||`; cpp `or` | byte |
| K0688 | K0688, K0912 | i32,u64 | bool | cpp | cpp `&&`; cpp `and` | byte |
| K0689 | K0689, K0913 | i64,u64 | bool | cpp | cpp `&&`; cpp `and` | byte |
| K0690 | K0690, K0914 | u64,i32 | bool | cpp | cpp `&&`; cpp `and` | byte |
| K0691 | K0691, K0915 | u64,i64 | bool | cpp | cpp `&&`; cpp `and` | byte |
| K0692 | K0692, K0916 | u64,u64 | bool | cpp | cpp `&&`; cpp `and` | byte |
| K0693 | K0693, K0917 | u64,f32 | bool | cpp | cpp `&&`; cpp `and` | byte |
| K0694 | K0694, K0918 | u64,f64 | bool | cpp | cpp `&&`; cpp `and` | byte |
| K0695 | K0695, K0919 | u64,bool | bool | cpp | cpp `&&`; cpp `and` | byte |
| K0696 | K0696, K0920 | f32,u64 | bool | cpp | cpp `&&`; cpp `and` | byte |
| K0697 | K0697, K0921 | f64,u64 | bool | cpp | cpp `&&`; cpp `and` | byte |
| K0698 | K0698, K0922 | bool,u64 | bool | cpp | cpp `&&`; cpp `and` | byte |
| K0699 | K0699, K0923 | bool,f32 | bool | cpp | cpp `&&`; cpp `and` | byte |
| K0700 | K0700, K0924 | bool,f64 | bool | cpp | cpp `&&`; cpp `and` | byte |
| K0702 | K0702, K1076 | i32,i64 | bool | cpp, swift | cpp `==`; swift `==` | z3 |
| K0707 | K0707, K1078 | i64,i32 | bool | cpp, swift | cpp `==`; swift `==` | z3 |
| K0732 | K0732, K0925 | i32,u64 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0733 | K0733, K0926 | i32,f32 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0734 | K0734, K0927 | i32,f64 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0735 | K0735, K0928 | i32,bool | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0736 | K0736, K0929 | i64,u64 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0737 | K0737, K0930 | i64,f32 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0738 | K0738, K0931 | i64,f64 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0739 | K0739, K0932 | u64,i32 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0740 | K0740, K0933 | u64,i64 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0741 | K0741, K0934 | u64,f32 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0742 | K0742, K0935 | u64,f64 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0743 | K0743, K0936 | u64,bool | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0744 | K0744, K0937 | f32,i32 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0745 | K0745, K0938 | f32,i64 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0746 | K0746, K0939 | f32,u64 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0747 | K0747, K0940 | f32,f64 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0748 | K0748, K0941 | f32,bool | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0749 | K0749, K0942 | f64,i32 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0750 | K0750, K0943 | f64,i64 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0751 | K0751, K0944 | f64,u64 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0752 | K0752, K0945 | f64,f32 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0753 | K0753, K0946 | f64,bool | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0754 | K0754, K0947 | bool,u64 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0755 | K0755, K0948 | bool,f32 | bool | cpp | cpp `!=`; cpp `not_eq` | byte |
| K0757 | K0757, K1052 | i32,i64 | bool | cpp, swift | cpp `>`; swift `>` | z3 |
| K0762 | K0762, K1054 | i64,i32 | bool | cpp, swift | cpp `>`; swift `>` | z3 |
| K0787 | K0787, K1064 | i32,i64 | bool | cpp, swift | cpp `>=`; swift `>=` | z3 |
| K0792 | K0792, K1066 | i64,i32 | bool | cpp, swift | cpp `>=`; swift `>=` | z3 |
| K0817 | K0817, K1058 | i32,i64 | bool | cpp, swift | cpp `<=`; swift `<=` | z3 |
| K0822 | K0822, K1060 | i64,i32 | bool | cpp, swift | cpp `<=`; swift `<=` | z3 |
| K0847 | K0847, K1046 | i32,i64 | bool | cpp, swift | cpp `<`; swift `<` | z3 |
| K0852 | K0852, K1048 | i64,i32 | bool | cpp, swift | cpp `<`; swift `<` | z3 |
| K1082 | K1082, K1090 | i32,i32 | i32 | swift | swift `<<`; swift `>>` | byte |
| K1083 | K1083, K1091 | i32,i64 | i32 | swift | swift `<<`; swift `>>` | byte |
| K1084 | K1084, K1092 | i32,u64 | i32 | swift | swift `<<`; swift `>>` | byte |
| K1085 | K1085, K1093 | i64,i32 | i64 | swift | swift `<<`; swift `>>` | byte |
| K1086 | K1086, K1094 | i64,i64 | i64 | swift | swift `<<`; swift `>>` | byte |
| K1087 | K1087, K1095 | i64,u64 | i64 | swift | swift `<<`; swift `>>` | byte |
| K1088 | K1088, K1096 | u64,i32 | u64 | swift | swift `<<`; swift `>>` | byte |
