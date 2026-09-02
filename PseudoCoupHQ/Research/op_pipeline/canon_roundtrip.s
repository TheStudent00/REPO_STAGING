        .text
        .globl u_c_0
        .type u_c_0, @function
u_c_0:
        xor %eax,%eax
        test %edi,%edi
        sete %al
        ret
        .size u_c_0, .-u_c_0
        .globl u_c_1
        .type u_c_1, @function
u_c_1:
        xor %eax,%eax
        test %rdi,%rdi
        sete %al
        ret
        .size u_c_1, .-u_c_1
        .globl u_c_2
        .type u_c_2, @function
u_c_2:
        xor %eax,%eax
        test %rdi,%rdi
        sete %al
        ret
        .size u_c_2, .-u_c_2
        .globl u_c_3
        .type u_c_3, @function
u_c_3:
        xorps %xmm1,%xmm1
        cmpeqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_c_3, .-u_c_3
        .globl u_c_4
        .type u_c_4, @function
u_c_4:
        xorpd %xmm1,%xmm1
        cmpeqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_c_4, .-u_c_4
        .globl u_c_5
        .type u_c_5, @function
u_c_5:
        xor $0x1,%dil
        movzbl %dil,%eax
        ret
        .size u_c_5, .-u_c_5
        .globl u_c_6
        .type u_c_6, @function
u_c_6:
        mov %edi,%eax
        not %eax
        ret
        .size u_c_6, .-u_c_6
        .globl u_c_7
        .type u_c_7, @function
u_c_7:
        mov %rdi,%rax
        not %rax
        ret
        .size u_c_7, .-u_c_7
        .globl u_c_8
        .type u_c_8, @function
u_c_8:
        mov %rdi,%rax
        not %rax
        ret
        .size u_c_8, .-u_c_8
        .globl u_c_11
        .type u_c_11, @function
u_c_11:
        mov %edi,%eax
        not %eax
        ret
        .size u_c_11, .-u_c_11
        .globl u_c_12
        .type u_c_12, @function
u_c_12:
        mov %edi,%eax
        neg %eax
        ret
        .size u_c_12, .-u_c_12
        .globl u_c_13
        .type u_c_13, @function
u_c_13:
        mov %rdi,%rax
        neg %rax
        ret
        .size u_c_13, .-u_c_13
        .globl u_c_14
        .type u_c_14, @function
u_c_14:
        mov %rdi,%rax
        neg %rax
        ret
        .size u_c_14, .-u_c_14
        .globl u_c_17
        .type u_c_17, @function
u_c_17:
        mov %edi,%eax
        neg %eax
        ret
        .size u_c_17, .-u_c_17
        .globl u_c_18
        .type u_c_18, @function
u_c_18:
        mov %edi,%eax
        ret
        .size u_c_18, .-u_c_18
        .globl u_c_19
        .type u_c_19, @function
u_c_19:
        mov %rdi,%rax
        ret
        .size u_c_19, .-u_c_19
        .globl u_c_20
        .type u_c_20, @function
u_c_20:
        mov %rdi,%rax
        ret
        .size u_c_20, .-u_c_20
        .globl u_c_21
        .type u_c_21, @function
u_c_21:
        ret
        .size u_c_21, .-u_c_21
        .globl u_c_22
        .type u_c_22, @function
u_c_22:
        ret
        .size u_c_22, .-u_c_22
        .globl u_c_23
        .type u_c_23, @function
u_c_23:
        mov %edi,%eax
        ret
        .size u_c_23, .-u_c_23
        .globl u_c_30
        .type u_c_30, @function
u_c_30:
        mov %edi,-0x4(%rsp)
        lea -0x4(%rsp),%rax
        ret
        .size u_c_30, .-u_c_30
        .globl u_c_31
        .type u_c_31, @function
u_c_31:
        mov %rdi,-0x8(%rsp)
        lea -0x8(%rsp),%rax
        ret
        .size u_c_31, .-u_c_31
        .globl u_c_32
        .type u_c_32, @function
u_c_32:
        mov %rdi,-0x8(%rsp)
        lea -0x8(%rsp),%rax
        ret
        .size u_c_32, .-u_c_32
        .globl u_c_33
        .type u_c_33, @function
u_c_33:
        movss %xmm0,-0x4(%rsp)
        lea -0x4(%rsp),%rax
        ret
        .size u_c_33, .-u_c_33
        .globl u_c_34
        .type u_c_34, @function
u_c_34:
        movsd %xmm0,-0x8(%rsp)
        lea -0x8(%rsp),%rax
        ret
        .size u_c_34, .-u_c_34
        .globl u_c_35
        .type u_c_35, @function
u_c_35:
        mov %dil,-0x1(%rsp)
        lea -0x1(%rsp),%rax
        ret
        .size u_c_35, .-u_c_35
        .globl u_c_36
        .type u_c_36, @function
u_c_36:
        lea 0x1(%rdi),%eax
        ret
        .size u_c_36, .-u_c_36
        .globl u_c_37
        .type u_c_37, @function
u_c_37:
        lea 0x1(%rdi),%rax
        ret
        .size u_c_37, .-u_c_37
        .globl u_c_38
        .type u_c_38, @function
u_c_38:
        lea 0x1(%rdi),%rax
        ret
        .size u_c_38, .-u_c_38
        .globl u_c_41
        .type u_c_41, @function
u_c_41:
        mov $0x1,%al
        ret
        .size u_c_41, .-u_c_41
        .globl u_c_42
        .type u_c_42, @function
u_c_42:
        lea -0x1(%rdi),%eax
        ret
        .size u_c_42, .-u_c_42
        .globl u_c_43
        .type u_c_43, @function
u_c_43:
        lea -0x1(%rdi),%rax
        ret
        .size u_c_43, .-u_c_43
        .globl u_c_44
        .type u_c_44, @function
u_c_44:
        lea -0x1(%rdi),%rax
        ret
        .size u_c_44, .-u_c_44
        .globl u_c_47
        .type u_c_47, @function
u_c_47:
        mov %edi,%eax
        xor $0x1,%al
        ret
        .size u_c_47, .-u_c_47
        .globl u_c_48
        .type u_c_48, @function
u_c_48:
        mov $0x4,%eax
        ret
        .size u_c_48, .-u_c_48
        .globl u_c_49
        .type u_c_49, @function
u_c_49:
        mov $0x8,%eax
        ret
        .size u_c_49, .-u_c_49
        .globl u_c_50
        .type u_c_50, @function
u_c_50:
        mov $0x8,%eax
        ret
        .size u_c_50, .-u_c_50
        .globl u_c_51
        .type u_c_51, @function
u_c_51:
        mov $0x4,%eax
        ret
        .size u_c_51, .-u_c_51
        .globl u_c_52
        .type u_c_52, @function
u_c_52:
        mov $0x8,%eax
        ret
        .size u_c_52, .-u_c_52
        .globl u_c_53
        .type u_c_53, @function
u_c_53:
        mov $0x1,%eax
        ret
        .size u_c_53, .-u_c_53
        .globl u_c_54
        .type u_c_54, @function
u_c_54:
        mov $0x4,%eax
        ret
        .size u_c_54, .-u_c_54
        .globl u_c_55
        .type u_c_55, @function
u_c_55:
        mov $0x8,%eax
        ret
        .size u_c_55, .-u_c_55
        .globl u_c_56
        .type u_c_56, @function
u_c_56:
        mov $0x8,%eax
        ret
        .size u_c_56, .-u_c_56
        .globl u_c_57
        .type u_c_57, @function
u_c_57:
        mov $0x4,%eax
        ret
        .size u_c_57, .-u_c_57
        .globl u_c_58
        .type u_c_58, @function
u_c_58:
        mov $0x8,%eax
        ret
        .size u_c_58, .-u_c_58
        .globl u_c_59
        .type u_c_59, @function
u_c_59:
        mov $0x1,%eax
        ret
        .size u_c_59, .-u_c_59
        .globl u_c_60
        .type u_c_60, @function
u_c_60:
        mov $0x4,%eax
        ret
        .size u_c_60, .-u_c_60
        .globl u_c_61
        .type u_c_61, @function
u_c_61:
        mov $0x8,%eax
        ret
        .size u_c_61, .-u_c_61
        .globl u_c_62
        .type u_c_62, @function
u_c_62:
        mov $0x8,%eax
        ret
        .size u_c_62, .-u_c_62
        .globl u_c_63
        .type u_c_63, @function
u_c_63:
        mov $0x4,%eax
        ret
        .size u_c_63, .-u_c_63
        .globl u_c_64
        .type u_c_64, @function
u_c_64:
        mov $0x8,%eax
        ret
        .size u_c_64, .-u_c_64
        .globl u_c_65
        .type u_c_65, @function
u_c_65:
        mov $0x1,%eax
        ret
        .size u_c_65, .-u_c_65
        .globl u_c_78
        .type u_c_78, @function
u_c_78:
        mov $0x4,%eax
        ret
        .size u_c_78, .-u_c_78
        .globl u_c_79
        .type u_c_79, @function
u_c_79:
        mov $0x8,%eax
        ret
        .size u_c_79, .-u_c_79
        .globl u_c_80
        .type u_c_80, @function
u_c_80:
        mov $0x8,%eax
        ret
        .size u_c_80, .-u_c_80
        .globl u_c_81
        .type u_c_81, @function
u_c_81:
        mov $0x4,%eax
        ret
        .size u_c_81, .-u_c_81
        .globl u_c_82
        .type u_c_82, @function
u_c_82:
        mov $0x8,%eax
        ret
        .size u_c_82, .-u_c_82
        .globl u_c_83
        .type u_c_83, @function
u_c_83:
        mov $0x1,%eax
        ret
        .size u_c_83, .-u_c_83
        .globl u_c_84
        .type u_c_84, @function
u_c_84:
        mov %edi,%eax
        ret
        .size u_c_84, .-u_c_84
        .globl u_c_85
        .type u_c_85, @function
u_c_85:
        mov %rdi,%rax
        ret
        .size u_c_85, .-u_c_85
        .globl u_c_86
        .type u_c_86, @function
u_c_86:
        mov %rdi,%rax
        ret
        .size u_c_86, .-u_c_86
        .globl u_c_87
        .type u_c_87, @function
u_c_87:
        ret
        .size u_c_87, .-u_c_87
        .globl u_c_88
        .type u_c_88, @function
u_c_88:
        ret
        .size u_c_88, .-u_c_88
        .globl u_c_89
        .type u_c_89, @function
u_c_89:
        mov %edi,%eax
        ret
        .size u_c_89, .-u_c_89
        .globl u_c_90
        .type u_c_90, @function
u_c_90:
        mov %edi,%eax
        ret
        .size u_c_90, .-u_c_90
        .globl u_c_91
        .type u_c_91, @function
u_c_91:
        mov %rdi,%rax
        ret
        .size u_c_91, .-u_c_91
        .globl u_c_92
        .type u_c_92, @function
u_c_92:
        mov %rdi,%rax
        ret
        .size u_c_92, .-u_c_92
        .globl u_c_93
        .type u_c_93, @function
u_c_93:
        ret
        .size u_c_93, .-u_c_93
        .globl u_c_94
        .type u_c_94, @function
u_c_94:
        ret
        .size u_c_94, .-u_c_94
        .globl u_c_95
        .type u_c_95, @function
u_c_95:
        mov %edi,%eax
        ret
        .size u_c_95, .-u_c_95
        .globl u_c_96
        .type u_c_96, @function
u_c_96:
        mov %edi,%eax
        ret
        .size u_c_96, .-u_c_96
        .globl u_c_97
        .type u_c_97, @function
u_c_97:
        mov %rdi,%rax
        ret
        .size u_c_97, .-u_c_97
        .globl u_c_98
        .type u_c_98, @function
u_c_98:
        mov %rdi,%rax
        ret
        .size u_c_98, .-u_c_98
        .globl u_c_99
        .type u_c_99, @function
u_c_99:
        ret
        .size u_c_99, .-u_c_99
        .globl u_c_100
        .type u_c_100, @function
u_c_100:
        ret
        .size u_c_100, .-u_c_100
        .globl u_c_101
        .type u_c_101, @function
u_c_101:
        mov %edi,%eax
        ret
        .size u_c_101, .-u_c_101
        .globl u_c_102
        .type u_c_102, @function
u_c_102:
        lea (%rdi,%rsi,1),%eax
        ret
        .size u_c_102, .-u_c_102
        .globl u_c_103
        .type u_c_103, @function
u_c_103:
        movslq %edi,%rax
        add %rsi,%rax
        ret
        .size u_c_103, .-u_c_103
        .globl u_c_104
        .type u_c_104, @function
u_c_104:
        movslq %edi,%rax
        add %rsi,%rax
        ret
        .size u_c_104, .-u_c_104
        .globl u_c_105
        .type u_c_105, @function
u_c_105:
        cvtsi2ss %edi,%xmm1
        addss %xmm1,%xmm0
        ret
        .size u_c_105, .-u_c_105
        .globl u_c_106
        .type u_c_106, @function
u_c_106:
        cvtsi2sd %edi,%xmm1
        addsd %xmm1,%xmm0
        ret
        .size u_c_106, .-u_c_106
        .globl u_c_107
        .type u_c_107, @function
u_c_107:
        lea (%rdi,%rsi,1),%eax
        ret
        .size u_c_107, .-u_c_107
        .globl u_c_108
        .type u_c_108, @function
u_c_108:
        movslq %esi,%rax
        add %rdi,%rax
        ret
        .size u_c_108, .-u_c_108
        .globl u_c_109
        .type u_c_109, @function
u_c_109:
        lea (%rdi,%rsi,1),%rax
        ret
        .size u_c_109, .-u_c_109
        .globl u_c_110
        .type u_c_110, @function
u_c_110:
        lea (%rdi,%rsi,1),%rax
        ret
        .size u_c_110, .-u_c_110
        .globl u_c_111
        .type u_c_111, @function
u_c_111:
        cvtsi2ss %rdi,%xmm1
        addss %xmm1,%xmm0
        ret
        .size u_c_111, .-u_c_111
        .globl u_c_112
        .type u_c_112, @function
u_c_112:
        cvtsi2sd %rdi,%xmm1
        addsd %xmm1,%xmm0
        ret
        .size u_c_112, .-u_c_112
        .globl u_c_113
        .type u_c_113, @function
u_c_113:
        mov %esi,%eax
        add %rdi,%rax
        ret
        .size u_c_113, .-u_c_113
        .globl u_c_114
        .type u_c_114, @function
u_c_114:
        movslq %esi,%rax
        add %rdi,%rax
        ret
        .size u_c_114, .-u_c_114
        .globl u_c_115
        .type u_c_115, @function
u_c_115:
        lea (%rdi,%rsi,1),%rax
        ret
        .size u_c_115, .-u_c_115
        .globl u_c_116
        .type u_c_116, @function
u_c_116:
        lea (%rdi,%rsi,1),%rax
        ret
        .size u_c_116, .-u_c_116
        .globl u_c_119
        .type u_c_119, @function
u_c_119:
        mov %esi,%eax
        add %rdi,%rax
        ret
        .size u_c_119, .-u_c_119
        .globl u_c_120
        .type u_c_120, @function
u_c_120:
        cvtsi2ss %edi,%xmm1
        addss %xmm1,%xmm0
        ret
        .size u_c_120, .-u_c_120
        .globl u_c_121
        .type u_c_121, @function
u_c_121:
        cvtsi2ss %rdi,%xmm1
        addss %xmm1,%xmm0
        ret
        .size u_c_121, .-u_c_121
        .globl u_c_123
        .type u_c_123, @function
u_c_123:
        addss %xmm1,%xmm0
        ret
        .size u_c_123, .-u_c_123
        .globl u_c_124
        .type u_c_124, @function
u_c_124:
        cvtss2sd %xmm0,%xmm0
        addsd %xmm1,%xmm0
        ret
        .size u_c_124, .-u_c_124
        .globl u_c_125
        .type u_c_125, @function
u_c_125:
        cvtsi2ss %edi,%xmm1
        addss %xmm1,%xmm0
        ret
        .size u_c_125, .-u_c_125
        .globl u_c_126
        .type u_c_126, @function
u_c_126:
        cvtsi2sd %edi,%xmm1
        addsd %xmm1,%xmm0
        ret
        .size u_c_126, .-u_c_126
        .globl u_c_127
        .type u_c_127, @function
u_c_127:
        cvtsi2sd %rdi,%xmm1
        addsd %xmm1,%xmm0
        ret
        .size u_c_127, .-u_c_127
        .globl u_c_129
        .type u_c_129, @function
u_c_129:
        cvtss2sd %xmm1,%xmm2
        addsd %xmm2,%xmm0
        ret
        .size u_c_129, .-u_c_129
        .globl u_c_130
        .type u_c_130, @function
u_c_130:
        addsd %xmm1,%xmm0
        ret
        .size u_c_130, .-u_c_130
        .globl u_c_131
        .type u_c_131, @function
u_c_131:
        cvtsi2sd %edi,%xmm1
        addsd %xmm1,%xmm0
        ret
        .size u_c_131, .-u_c_131
        .globl u_c_132
        .type u_c_132, @function
u_c_132:
        lea (%rdi,%rsi,1),%eax
        ret
        .size u_c_132, .-u_c_132
        .globl u_c_133
        .type u_c_133, @function
u_c_133:
        mov %edi,%eax
        add %rsi,%rax
        ret
        .size u_c_133, .-u_c_133
        .globl u_c_134
        .type u_c_134, @function
u_c_134:
        mov %edi,%eax
        add %rsi,%rax
        ret
        .size u_c_134, .-u_c_134
        .globl u_c_135
        .type u_c_135, @function
u_c_135:
        cvtsi2ss %edi,%xmm1
        addss %xmm1,%xmm0
        ret
        .size u_c_135, .-u_c_135
        .globl u_c_136
        .type u_c_136, @function
u_c_136:
        cvtsi2sd %edi,%xmm1
        addsd %xmm1,%xmm0
        ret
        .size u_c_136, .-u_c_136
        .globl u_c_137
        .type u_c_137, @function
u_c_137:
        lea (%rdi,%rsi,1),%eax
        ret
        .size u_c_137, .-u_c_137
        .globl u_c_138
        .type u_c_138, @function
u_c_138:
        mov %edi,%eax
        sub %esi,%eax
        ret
        .size u_c_138, .-u_c_138
        .globl u_c_139
        .type u_c_139, @function
u_c_139:
        movslq %edi,%rax
        sub %rsi,%rax
        ret
        .size u_c_139, .-u_c_139
        .globl u_c_140
        .type u_c_140, @function
u_c_140:
        movslq %edi,%rax
        sub %rsi,%rax
        ret
        .size u_c_140, .-u_c_140
        .globl u_c_141
        .type u_c_141, @function
u_c_141:
        cvtsi2ss %edi,%xmm1
        subss %xmm0,%xmm1
        movaps %xmm1,%xmm0
        ret
        .size u_c_141, .-u_c_141
        .globl u_c_142
        .type u_c_142, @function
u_c_142:
        cvtsi2sd %edi,%xmm1
        subsd %xmm0,%xmm1
        movapd %xmm1,%xmm0
        ret
        .size u_c_142, .-u_c_142
        .globl u_c_143
        .type u_c_143, @function
u_c_143:
        mov %edi,%eax
        sub %esi,%eax
        ret
        .size u_c_143, .-u_c_143
        .globl u_c_144
        .type u_c_144, @function
u_c_144:
        mov %rdi,%rax
        movslq %esi,%rcx
        sub %rcx,%rax
        ret
        .size u_c_144, .-u_c_144
        .globl u_c_145
        .type u_c_145, @function
u_c_145:
        mov %rdi,%rax
        sub %rsi,%rax
        ret
        .size u_c_145, .-u_c_145
        .globl u_c_146
        .type u_c_146, @function
u_c_146:
        mov %rdi,%rax
        sub %rsi,%rax
        ret
        .size u_c_146, .-u_c_146
        .globl u_c_147
        .type u_c_147, @function
u_c_147:
        cvtsi2ss %rdi,%xmm1
        subss %xmm0,%xmm1
        movaps %xmm1,%xmm0
        ret
        .size u_c_147, .-u_c_147
        .globl u_c_148
        .type u_c_148, @function
u_c_148:
        cvtsi2sd %rdi,%xmm1
        subsd %xmm0,%xmm1
        movapd %xmm1,%xmm0
        ret
        .size u_c_148, .-u_c_148
        .globl u_c_149
        .type u_c_149, @function
u_c_149:
        mov %rdi,%rax
        mov %esi,%ecx
        sub %rcx,%rax
        ret
        .size u_c_149, .-u_c_149
        .globl u_c_150
        .type u_c_150, @function
u_c_150:
        mov %rdi,%rax
        movslq %esi,%rcx
        sub %rcx,%rax
        ret
        .size u_c_150, .-u_c_150
        .globl u_c_151
        .type u_c_151, @function
u_c_151:
        mov %rdi,%rax
        sub %rsi,%rax
        ret
        .size u_c_151, .-u_c_151
        .globl u_c_152
        .type u_c_152, @function
u_c_152:
        mov %rdi,%rax
        sub %rsi,%rax
        ret
        .size u_c_152, .-u_c_152
        .globl u_c_155
        .type u_c_155, @function
u_c_155:
        mov %rdi,%rax
        mov %esi,%ecx
        sub %rcx,%rax
        ret
        .size u_c_155, .-u_c_155
        .globl u_c_156
        .type u_c_156, @function
u_c_156:
        cvtsi2ss %edi,%xmm1
        subss %xmm1,%xmm0
        ret
        .size u_c_156, .-u_c_156
        .globl u_c_157
        .type u_c_157, @function
u_c_157:
        cvtsi2ss %rdi,%xmm1
        subss %xmm1,%xmm0
        ret
        .size u_c_157, .-u_c_157
        .globl u_c_159
        .type u_c_159, @function
u_c_159:
        subss %xmm1,%xmm0
        ret
        .size u_c_159, .-u_c_159
        .globl u_c_160
        .type u_c_160, @function
u_c_160:
        cvtss2sd %xmm0,%xmm0
        subsd %xmm1,%xmm0
        ret
        .size u_c_160, .-u_c_160
        .globl u_c_161
        .type u_c_161, @function
u_c_161:
        cvtsi2ss %edi,%xmm1
        subss %xmm1,%xmm0
        ret
        .size u_c_161, .-u_c_161
        .globl u_c_162
        .type u_c_162, @function
u_c_162:
        cvtsi2sd %edi,%xmm1
        subsd %xmm1,%xmm0
        ret
        .size u_c_162, .-u_c_162
        .globl u_c_163
        .type u_c_163, @function
u_c_163:
        cvtsi2sd %rdi,%xmm1
        subsd %xmm1,%xmm0
        ret
        .size u_c_163, .-u_c_163
        .globl u_c_165
        .type u_c_165, @function
u_c_165:
        cvtss2sd %xmm1,%xmm2
        subsd %xmm2,%xmm0
        ret
        .size u_c_165, .-u_c_165
        .globl u_c_166
        .type u_c_166, @function
u_c_166:
        subsd %xmm1,%xmm0
        ret
        .size u_c_166, .-u_c_166
        .globl u_c_167
        .type u_c_167, @function
u_c_167:
        cvtsi2sd %edi,%xmm1
        subsd %xmm1,%xmm0
        ret
        .size u_c_167, .-u_c_167
        .globl u_c_168
        .type u_c_168, @function
u_c_168:
        mov %edi,%eax
        sub %esi,%eax
        ret
        .size u_c_168, .-u_c_168
        .globl u_c_169
        .type u_c_169, @function
u_c_169:
        mov %edi,%eax
        sub %rsi,%rax
        ret
        .size u_c_169, .-u_c_169
        .globl u_c_170
        .type u_c_170, @function
u_c_170:
        mov %edi,%eax
        sub %rsi,%rax
        ret
        .size u_c_170, .-u_c_170
        .globl u_c_171
        .type u_c_171, @function
u_c_171:
        cvtsi2ss %edi,%xmm1
        subss %xmm0,%xmm1
        movaps %xmm1,%xmm0
        ret
        .size u_c_171, .-u_c_171
        .globl u_c_172
        .type u_c_172, @function
u_c_172:
        cvtsi2sd %edi,%xmm1
        subsd %xmm0,%xmm1
        movapd %xmm1,%xmm0
        ret
        .size u_c_172, .-u_c_172
        .globl u_c_173
        .type u_c_173, @function
u_c_173:
        mov %edi,%eax
        sub %esi,%eax
        ret
        .size u_c_173, .-u_c_173
        .globl u_c_174
        .type u_c_174, @function
u_c_174:
        mov %edi,%eax
        imul %esi,%eax
        ret
        .size u_c_174, .-u_c_174
        .globl u_c_175
        .type u_c_175, @function
u_c_175:
        movslq %edi,%rax
        imul %rsi,%rax
        ret
        .size u_c_175, .-u_c_175
        .globl u_c_176
        .type u_c_176, @function
u_c_176:
        movslq %edi,%rax
        imul %rsi,%rax
        ret
        .size u_c_176, .-u_c_176
        .globl u_c_177
        .type u_c_177, @function
u_c_177:
        cvtsi2ss %edi,%xmm1
        mulss %xmm1,%xmm0
        ret
        .size u_c_177, .-u_c_177
        .globl u_c_178
        .type u_c_178, @function
u_c_178:
        cvtsi2sd %edi,%xmm1
        mulsd %xmm1,%xmm0
        ret
        .size u_c_178, .-u_c_178
        .globl u_c_179
        .type u_c_179, @function
u_c_179:
        mov %edi,%eax
        test %esi,%esi
        cmove %esi,%eax
        ret
        .size u_c_179, .-u_c_179
        .globl u_c_180
        .type u_c_180, @function
u_c_180:
        movslq %esi,%rax
        imul %rdi,%rax
        ret
        .size u_c_180, .-u_c_180
        .globl u_c_181
        .type u_c_181, @function
u_c_181:
        mov %rdi,%rax
        imul %rsi,%rax
        ret
        .size u_c_181, .-u_c_181
        .globl u_c_182
        .type u_c_182, @function
u_c_182:
        mov %rdi,%rax
        imul %rsi,%rax
        ret
        .size u_c_182, .-u_c_182
        .globl u_c_183
        .type u_c_183, @function
u_c_183:
        cvtsi2ss %rdi,%xmm1
        mulss %xmm1,%xmm0
        ret
        .size u_c_183, .-u_c_183
        .globl u_c_184
        .type u_c_184, @function
u_c_184:
        cvtsi2sd %rdi,%xmm1
        mulsd %xmm1,%xmm0
        ret
        .size u_c_184, .-u_c_184
        .globl u_c_185
        .type u_c_185, @function
u_c_185:
        xor %eax,%eax
        test %esi,%esi
        cmovne %rdi,%rax
        ret
        .size u_c_185, .-u_c_185
        .globl u_c_186
        .type u_c_186, @function
u_c_186:
        movslq %esi,%rax
        imul %rdi,%rax
        ret
        .size u_c_186, .-u_c_186
        .globl u_c_187
        .type u_c_187, @function
u_c_187:
        mov %rdi,%rax
        imul %rsi,%rax
        ret
        .size u_c_187, .-u_c_187
        .globl u_c_188
        .type u_c_188, @function
u_c_188:
        mov %rdi,%rax
        imul %rsi,%rax
        ret
        .size u_c_188, .-u_c_188
        .globl u_c_191
        .type u_c_191, @function
u_c_191:
        xor %eax,%eax
        test %esi,%esi
        cmovne %rdi,%rax
        ret
        .size u_c_191, .-u_c_191
        .globl u_c_192
        .type u_c_192, @function
u_c_192:
        cvtsi2ss %edi,%xmm1
        mulss %xmm1,%xmm0
        ret
        .size u_c_192, .-u_c_192
        .globl u_c_193
        .type u_c_193, @function
u_c_193:
        cvtsi2ss %rdi,%xmm1
        mulss %xmm1,%xmm0
        ret
        .size u_c_193, .-u_c_193
        .globl u_c_195
        .type u_c_195, @function
u_c_195:
        mulss %xmm1,%xmm0
        ret
        .size u_c_195, .-u_c_195
        .globl u_c_196
        .type u_c_196, @function
u_c_196:
        cvtss2sd %xmm0,%xmm0
        mulsd %xmm1,%xmm0
        ret
        .size u_c_196, .-u_c_196
        .globl u_c_197
        .type u_c_197, @function
u_c_197:
        cvtsi2ss %edi,%xmm1
        mulss %xmm1,%xmm0
        ret
        .size u_c_197, .-u_c_197
        .globl u_c_198
        .type u_c_198, @function
u_c_198:
        cvtsi2sd %edi,%xmm1
        mulsd %xmm1,%xmm0
        ret
        .size u_c_198, .-u_c_198
        .globl u_c_199
        .type u_c_199, @function
u_c_199:
        cvtsi2sd %rdi,%xmm1
        mulsd %xmm1,%xmm0
        ret
        .size u_c_199, .-u_c_199
        .globl u_c_201
        .type u_c_201, @function
u_c_201:
        cvtss2sd %xmm1,%xmm2
        mulsd %xmm2,%xmm0
        ret
        .size u_c_201, .-u_c_201
        .globl u_c_202
        .type u_c_202, @function
u_c_202:
        mulsd %xmm1,%xmm0
        ret
        .size u_c_202, .-u_c_202
        .globl u_c_203
        .type u_c_203, @function
u_c_203:
        cvtsi2sd %edi,%xmm1
        mulsd %xmm1,%xmm0
        ret
        .size u_c_203, .-u_c_203
        .globl u_c_204
        .type u_c_204, @function
u_c_204:
        mov %esi,%eax
        test %edi,%edi
        cmove %edi,%eax
        ret
        .size u_c_204, .-u_c_204
        .globl u_c_205
        .type u_c_205, @function
u_c_205:
        xor %eax,%eax
        test %edi,%edi
        cmovne %rsi,%rax
        ret
        .size u_c_205, .-u_c_205
        .globl u_c_206
        .type u_c_206, @function
u_c_206:
        xor %eax,%eax
        test %edi,%edi
        cmovne %rsi,%rax
        ret
        .size u_c_206, .-u_c_206
        .globl u_c_207
        .type u_c_207, @function
u_c_207:
        cvtsi2ss %edi,%xmm1
        mulss %xmm1,%xmm0
        ret
        .size u_c_207, .-u_c_207
        .globl u_c_208
        .type u_c_208, @function
u_c_208:
        cvtsi2sd %edi,%xmm1
        mulsd %xmm1,%xmm0
        ret
        .size u_c_208, .-u_c_208
        .globl u_c_209
        .type u_c_209, @function
u_c_209:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_c_209, .-u_c_209
        .globl u_c_210
        .type u_c_210, @function
u_c_210:
        mov %edi,%eax
        cltd
        idiv %esi
        ret
        .size u_c_210, .-u_c_210
        .globl u_c_211
        .type u_c_211, @function
u_c_211:
        movslq %edi,%rax
        cqto
        idiv %rsi
        ret
        .size u_c_211, .-u_c_211
        .globl u_c_212
        .type u_c_212, @function
u_c_212:
        movslq %edi,%rax
        xor %edx,%edx
        div %rsi
        ret
        .size u_c_212, .-u_c_212
        .globl u_c_213
        .type u_c_213, @function
u_c_213:
        cvtsi2ss %edi,%xmm1
        divss %xmm0,%xmm1
        movaps %xmm1,%xmm0
        ret
        .size u_c_213, .-u_c_213
        .globl u_c_214
        .type u_c_214, @function
u_c_214:
        cvtsi2sd %edi,%xmm1
        divsd %xmm0,%xmm1
        movapd %xmm1,%xmm0
        ret
        .size u_c_214, .-u_c_214
        .globl u_c_215
        .type u_c_215, @function
u_c_215:
        mov %edi,%eax
        ret
        .size u_c_215, .-u_c_215
        .globl u_c_216
        .type u_c_216, @function
u_c_216:
        mov %rdi,%rax
        movslq %esi,%rcx
        cqto
        idiv %rcx
        ret
        .size u_c_216, .-u_c_216
        .globl u_c_217
        .type u_c_217, @function
u_c_217:
        mov %rdi,%rax
        cqto
        idiv %rsi
        ret
        .size u_c_217, .-u_c_217
        .globl u_c_218
        .type u_c_218, @function
u_c_218:
        mov %rdi,%rax
        xor %edx,%edx
        div %rsi
        ret
        .size u_c_218, .-u_c_218
        .globl u_c_219
        .type u_c_219, @function
u_c_219:
        cvtsi2ss %rdi,%xmm1
        divss %xmm0,%xmm1
        movaps %xmm1,%xmm0
        ret
        .size u_c_219, .-u_c_219
        .globl u_c_220
        .type u_c_220, @function
u_c_220:
        cvtsi2sd %rdi,%xmm1
        divsd %xmm0,%xmm1
        movapd %xmm1,%xmm0
        ret
        .size u_c_220, .-u_c_220
        .globl u_c_221
        .type u_c_221, @function
u_c_221:
        mov %rdi,%rax
        ret
        .size u_c_221, .-u_c_221
        .globl u_c_222
        .type u_c_222, @function
u_c_222:
        mov %rdi,%rax
        movslq %esi,%rcx
        xor %edx,%edx
        div %rcx
        ret
        .size u_c_222, .-u_c_222
        .globl u_c_223
        .type u_c_223, @function
u_c_223:
        mov %rdi,%rax
        xor %edx,%edx
        div %rsi
        ret
        .size u_c_223, .-u_c_223
        .globl u_c_224
        .type u_c_224, @function
u_c_224:
        mov %rdi,%rax
        xor %edx,%edx
        div %rsi
        ret
        .size u_c_224, .-u_c_224
        .globl u_c_227
        .type u_c_227, @function
u_c_227:
        mov %rdi,%rax
        ret
        .size u_c_227, .-u_c_227
        .globl u_c_228
        .type u_c_228, @function
u_c_228:
        cvtsi2ss %edi,%xmm1
        divss %xmm1,%xmm0
        ret
        .size u_c_228, .-u_c_228
        .globl u_c_229
        .type u_c_229, @function
u_c_229:
        cvtsi2ss %rdi,%xmm1
        divss %xmm1,%xmm0
        ret
        .size u_c_229, .-u_c_229
        .globl u_c_231
        .type u_c_231, @function
u_c_231:
        divss %xmm1,%xmm0
        ret
        .size u_c_231, .-u_c_231
        .globl u_c_232
        .type u_c_232, @function
u_c_232:
        cvtss2sd %xmm0,%xmm0
        divsd %xmm1,%xmm0
        ret
        .size u_c_232, .-u_c_232
        .globl u_c_233
        .type u_c_233, @function
u_c_233:
        cvtsi2ss %edi,%xmm1
        divss %xmm1,%xmm0
        ret
        .size u_c_233, .-u_c_233
        .globl u_c_234
        .type u_c_234, @function
u_c_234:
        cvtsi2sd %edi,%xmm1
        divsd %xmm1,%xmm0
        ret
        .size u_c_234, .-u_c_234
        .globl u_c_235
        .type u_c_235, @function
u_c_235:
        cvtsi2sd %rdi,%xmm1
        divsd %xmm1,%xmm0
        ret
        .size u_c_235, .-u_c_235
        .globl u_c_237
        .type u_c_237, @function
u_c_237:
        cvtss2sd %xmm1,%xmm2
        divsd %xmm2,%xmm0
        ret
        .size u_c_237, .-u_c_237
        .globl u_c_238
        .type u_c_238, @function
u_c_238:
        divsd %xmm1,%xmm0
        ret
        .size u_c_238, .-u_c_238
        .globl u_c_239
        .type u_c_239, @function
u_c_239:
        cvtsi2sd %edi,%xmm1
        divsd %xmm1,%xmm0
        ret
        .size u_c_239, .-u_c_239
        .globl u_c_240
        .type u_c_240, @function
u_c_240:
        mov %edi,%eax
        xor %edx,%edx
        idiv %esi
        ret
        .size u_c_240, .-u_c_240
        .globl u_c_241
        .type u_c_241, @function
u_c_241:
        mov %edi,%eax
        xor %edx,%edx
        idiv %rsi
        ret
        .size u_c_241, .-u_c_241
        .globl u_c_242
        .type u_c_242, @function
u_c_242:
        mov %edi,%eax
        xor %edx,%edx
        div %rsi
        ret
        .size u_c_242, .-u_c_242
        .globl u_c_243
        .type u_c_243, @function
u_c_243:
        cvtsi2ss %edi,%xmm1
        divss %xmm0,%xmm1
        movaps %xmm1,%xmm0
        ret
        .size u_c_243, .-u_c_243
        .globl u_c_244
        .type u_c_244, @function
u_c_244:
        cvtsi2sd %edi,%xmm1
        divsd %xmm0,%xmm1
        movapd %xmm1,%xmm0
        ret
        .size u_c_244, .-u_c_244
        .globl u_c_245
        .type u_c_245, @function
u_c_245:
        mov %edi,%eax
        ret
        .size u_c_245, .-u_c_245
        .globl u_c_246
        .type u_c_246, @function
u_c_246:
        mov %edi,%eax
        cltd
        idiv %esi
        mov %edx,%eax
        ret
        .size u_c_246, .-u_c_246
        .globl u_c_247
        .type u_c_247, @function
u_c_247:
        movslq %edi,%rax
        cqto
        idiv %rsi
        mov %rdx,%rax
        ret
        .size u_c_247, .-u_c_247
        .globl u_c_248
        .type u_c_248, @function
u_c_248:
        movslq %edi,%rax
        xor %edx,%edx
        div %rsi
        mov %rdx,%rax
        ret
        .size u_c_248, .-u_c_248
        .globl u_c_251
        .type u_c_251, @function
u_c_251:
        xor %eax,%eax
        ret
        .size u_c_251, .-u_c_251
        .globl u_c_252
        .type u_c_252, @function
u_c_252:
        mov %rdi,%rax
        movslq %esi,%rcx
        cqto
        idiv %rcx
        mov %rdx,%rax
        ret
        .size u_c_252, .-u_c_252
        .globl u_c_253
        .type u_c_253, @function
u_c_253:
        mov %rdi,%rax
        cqto
        idiv %rsi
        mov %rdx,%rax
        ret
        .size u_c_253, .-u_c_253
        .globl u_c_254
        .type u_c_254, @function
u_c_254:
        mov %rdi,%rax
        xor %edx,%edx
        div %rsi
        mov %rdx,%rax
        ret
        .size u_c_254, .-u_c_254
        .globl u_c_257
        .type u_c_257, @function
u_c_257:
        xor %eax,%eax
        ret
        .size u_c_257, .-u_c_257
        .globl u_c_258
        .type u_c_258, @function
u_c_258:
        mov %rdi,%rax
        movslq %esi,%rcx
        xor %edx,%edx
        div %rcx
        mov %rdx,%rax
        ret
        .size u_c_258, .-u_c_258
        .globl u_c_259
        .type u_c_259, @function
u_c_259:
        mov %rdi,%rax
        xor %edx,%edx
        div %rsi
        mov %rdx,%rax
        ret
        .size u_c_259, .-u_c_259
        .globl u_c_260
        .type u_c_260, @function
u_c_260:
        mov %rdi,%rax
        xor %edx,%edx
        div %rsi
        mov %rdx,%rax
        ret
        .size u_c_260, .-u_c_260
        .globl u_c_263
        .type u_c_263, @function
u_c_263:
        xor %eax,%eax
        ret
        .size u_c_263, .-u_c_263
        .globl u_c_276
        .type u_c_276, @function
u_c_276:
        mov %edi,%eax
        xor %edx,%edx
        idiv %esi
        mov %edx,%eax
        ret
        .size u_c_276, .-u_c_276
        .globl u_c_277
        .type u_c_277, @function
u_c_277:
        mov %edi,%eax
        xor %edx,%edx
        idiv %rsi
        mov %rdx,%rax
        ret
        .size u_c_277, .-u_c_277
        .globl u_c_278
        .type u_c_278, @function
u_c_278:
        mov %edi,%eax
        xor %edx,%edx
        div %rsi
        mov %rdx,%rax
        ret
        .size u_c_278, .-u_c_278
        .globl u_c_281
        .type u_c_281, @function
u_c_281:
        xor %eax,%eax
        ret
        .size u_c_281, .-u_c_281
        .globl u_c_282
        .type u_c_282, @function
u_c_282:
        xor %eax,%eax
        or %esi,%edi
        setne %al
        ret
        .size u_c_282, .-u_c_282
        .globl u_c_283
        .type u_c_283, @function
u_c_283:
        test %edi,%edi
        setne %r10b
        test %rsi,%rsi
        setne %cl
        or %r10b,%cl
        movzbl %cl,%eax
        ret
        .size u_c_283, .-u_c_283
        .globl u_c_284
        .type u_c_284, @function
u_c_284:
        test %edi,%edi
        setne %r10b
        test %rsi,%rsi
        setne %cl
        or %r10b,%cl
        movzbl %cl,%eax
        ret
        .size u_c_284, .-u_c_284
        .globl u_c_285
        .type u_c_285, @function
u_c_285:
        test %edi,%edi
        setne %r10b
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %cl
        setne %dl
        or %cl,%dl
        or %r10b,%dl
        movzbl %dl,%eax
        ret
        .size u_c_285, .-u_c_285
        .globl u_c_286
        .type u_c_286, @function
u_c_286:
        test %edi,%edi
        setne %r10b
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %cl
        setne %dl
        or %cl,%dl
        or %r10b,%dl
        movzbl %dl,%eax
        ret
        .size u_c_286, .-u_c_286
        .globl u_c_287
        .type u_c_287, @function
u_c_287:
        test %edi,%edi
        setne %r10b
        or %sil,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_287, .-u_c_287
        .globl u_c_288
        .type u_c_288, @function
u_c_288:
        test %rdi,%rdi
        setne %r10b
        test %esi,%esi
        setne %cl
        or %r10b,%cl
        movzbl %cl,%eax
        ret
        .size u_c_288, .-u_c_288
        .globl u_c_289
        .type u_c_289, @function
u_c_289:
        xor %eax,%eax
        or %rsi,%rdi
        setne %al
        ret
        .size u_c_289, .-u_c_289
        .globl u_c_290
        .type u_c_290, @function
u_c_290:
        xor %eax,%eax
        or %rsi,%rdi
        setne %al
        ret
        .size u_c_290, .-u_c_290
        .globl u_c_291
        .type u_c_291, @function
u_c_291:
        test %rdi,%rdi
        setne %r10b
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %cl
        setne %dl
        or %cl,%dl
        or %r10b,%dl
        movzbl %dl,%eax
        ret
        .size u_c_291, .-u_c_291
        .globl u_c_292
        .type u_c_292, @function
u_c_292:
        test %rdi,%rdi
        setne %r10b
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %cl
        setne %dl
        or %cl,%dl
        or %r10b,%dl
        movzbl %dl,%eax
        ret
        .size u_c_292, .-u_c_292
        .globl u_c_293
        .type u_c_293, @function
u_c_293:
        test %rdi,%rdi
        setne %r10b
        or %sil,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_293, .-u_c_293
        .globl u_c_294
        .type u_c_294, @function
u_c_294:
        test %rdi,%rdi
        setne %r10b
        test %esi,%esi
        setne %cl
        or %r10b,%cl
        movzbl %cl,%eax
        ret
        .size u_c_294, .-u_c_294
        .globl u_c_295
        .type u_c_295, @function
u_c_295:
        xor %eax,%eax
        or %rsi,%rdi
        setne %al
        ret
        .size u_c_295, .-u_c_295
        .globl u_c_296
        .type u_c_296, @function
u_c_296:
        xor %eax,%eax
        or %rsi,%rdi
        setne %al
        ret
        .size u_c_296, .-u_c_296
        .globl u_c_297
        .type u_c_297, @function
u_c_297:
        test %rdi,%rdi
        setne %r10b
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %cl
        setne %dl
        or %cl,%dl
        or %r10b,%dl
        movzbl %dl,%eax
        ret
        .size u_c_297, .-u_c_297
        .globl u_c_298
        .type u_c_298, @function
u_c_298:
        test %rdi,%rdi
        setne %r10b
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %cl
        setne %dl
        or %cl,%dl
        or %r10b,%dl
        movzbl %dl,%eax
        ret
        .size u_c_298, .-u_c_298
        .globl u_c_299
        .type u_c_299, @function
u_c_299:
        test %rdi,%rdi
        setne %r10b
        or %sil,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_299, .-u_c_299
        .globl u_c_300
        .type u_c_300, @function
u_c_300:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        test %edi,%edi
        setne %r10b
        or %cl,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_300, .-u_c_300
        .globl u_c_301
        .type u_c_301, @function
u_c_301:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        test %rdi,%rdi
        setne %r10b
        or %cl,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_301, .-u_c_301
        .globl u_c_302
        .type u_c_302, @function
u_c_302:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        test %rdi,%rdi
        setne %r10b
        or %cl,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_302, .-u_c_302
        .globl u_c_303
        .type u_c_303, @function
u_c_303:
        xorps %xmm2,%xmm2
        cmpneqss %xmm2,%xmm1
        cmpneqss %xmm2,%xmm0
        orps %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%eax
        ret
        .size u_c_303, .-u_c_303
        .globl u_c_304
        .type u_c_304, @function
u_c_304:
        xorps %xmm2,%xmm2
        ucomiss %xmm2,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        xorps %xmm2,%xmm2
        ucomisd %xmm2,%xmm1
        setp %r10b
        setne %dl
        or %r10b,%dl
        or %cl,%dl
        movzbl %dl,%eax
        ret
        .size u_c_304, .-u_c_304
        .globl u_c_305
        .type u_c_305, @function
u_c_305:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        or %dil,%cl
        movzbl %cl,%eax
        ret
        .size u_c_305, .-u_c_305
        .globl u_c_306
        .type u_c_306, @function
u_c_306:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        test %edi,%edi
        setne %r10b
        or %cl,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_306, .-u_c_306
        .globl u_c_307
        .type u_c_307, @function
u_c_307:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        test %rdi,%rdi
        setne %r10b
        or %cl,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_307, .-u_c_307
        .globl u_c_308
        .type u_c_308, @function
u_c_308:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        test %rdi,%rdi
        setne %r10b
        or %cl,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_308, .-u_c_308
        .globl u_c_309
        .type u_c_309, @function
u_c_309:
        xorpd %xmm2,%xmm2
        ucomisd %xmm2,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        xorpd %xmm2,%xmm2
        ucomiss %xmm2,%xmm1
        setp %r10b
        setne %dl
        or %r10b,%dl
        or %cl,%dl
        movzbl %dl,%eax
        ret
        .size u_c_309, .-u_c_309
        .globl u_c_310
        .type u_c_310, @function
u_c_310:
        xorpd %xmm2,%xmm2
        cmpneqsd %xmm2,%xmm1
        cmpneqsd %xmm2,%xmm0
        orpd %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%eax
        ret
        .size u_c_310, .-u_c_310
        .globl u_c_311
        .type u_c_311, @function
u_c_311:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        or %dil,%cl
        movzbl %cl,%eax
        ret
        .size u_c_311, .-u_c_311
        .globl u_c_312
        .type u_c_312, @function
u_c_312:
        test %esi,%esi
        setne %r10b
        or %dil,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_312, .-u_c_312
        .globl u_c_313
        .type u_c_313, @function
u_c_313:
        test %rsi,%rsi
        setne %r10b
        or %dil,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_313, .-u_c_313
        .globl u_c_314
        .type u_c_314, @function
u_c_314:
        test %rsi,%rsi
        setne %r10b
        or %dil,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_314, .-u_c_314
        .globl u_c_315
        .type u_c_315, @function
u_c_315:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        or %dil,%cl
        movzbl %cl,%eax
        ret
        .size u_c_315, .-u_c_315
        .globl u_c_316
        .type u_c_316, @function
u_c_316:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        or %dil,%cl
        movzbl %cl,%eax
        ret
        .size u_c_316, .-u_c_316
        .globl u_c_317
        .type u_c_317, @function
u_c_317:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_c_317, .-u_c_317
        .globl u_c_318
        .type u_c_318, @function
u_c_318:
        test %edi,%edi
        setne %r10b
        test %esi,%esi
        setne %cl
        and %r10b,%cl
        movzbl %cl,%eax
        ret
        .size u_c_318, .-u_c_318
        .globl u_c_319
        .type u_c_319, @function
u_c_319:
        test %edi,%edi
        setne %r10b
        test %rsi,%rsi
        setne %cl
        and %r10b,%cl
        movzbl %cl,%eax
        ret
        .size u_c_319, .-u_c_319
        .globl u_c_320
        .type u_c_320, @function
u_c_320:
        test %edi,%edi
        setne %r10b
        test %rsi,%rsi
        setne %cl
        and %r10b,%cl
        movzbl %cl,%eax
        ret
        .size u_c_320, .-u_c_320
        .globl u_c_321
        .type u_c_321, @function
u_c_321:
        test %edi,%edi
        setne %r10b
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %cl
        setne %dl
        or %cl,%dl
        and %r10b,%dl
        movzbl %dl,%eax
        ret
        .size u_c_321, .-u_c_321
        .globl u_c_322
        .type u_c_322, @function
u_c_322:
        test %edi,%edi
        setne %r10b
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %cl
        setne %dl
        or %cl,%dl
        and %r10b,%dl
        movzbl %dl,%eax
        ret
        .size u_c_322, .-u_c_322
        .globl u_c_323
        .type u_c_323, @function
u_c_323:
        test %edi,%edi
        setne %r10b
        and %sil,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_323, .-u_c_323
        .globl u_c_324
        .type u_c_324, @function
u_c_324:
        test %rdi,%rdi
        setne %r10b
        test %esi,%esi
        setne %cl
        and %r10b,%cl
        movzbl %cl,%eax
        ret
        .size u_c_324, .-u_c_324
        .globl u_c_325
        .type u_c_325, @function
u_c_325:
        test %rdi,%rdi
        setne %r10b
        test %rsi,%rsi
        setne %cl
        and %r10b,%cl
        movzbl %cl,%eax
        ret
        .size u_c_325, .-u_c_325
        .globl u_c_326
        .type u_c_326, @function
u_c_326:
        test %rdi,%rdi
        setne %r10b
        test %rsi,%rsi
        setne %cl
        and %r10b,%cl
        movzbl %cl,%eax
        ret
        .size u_c_326, .-u_c_326
        .globl u_c_327
        .type u_c_327, @function
u_c_327:
        test %rdi,%rdi
        setne %r10b
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %cl
        setne %dl
        or %cl,%dl
        and %r10b,%dl
        movzbl %dl,%eax
        ret
        .size u_c_327, .-u_c_327
        .globl u_c_328
        .type u_c_328, @function
u_c_328:
        test %rdi,%rdi
        setne %r10b
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %cl
        setne %dl
        or %cl,%dl
        and %r10b,%dl
        movzbl %dl,%eax
        ret
        .size u_c_328, .-u_c_328
        .globl u_c_329
        .type u_c_329, @function
u_c_329:
        test %rdi,%rdi
        setne %r10b
        and %sil,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_329, .-u_c_329
        .globl u_c_330
        .type u_c_330, @function
u_c_330:
        test %rdi,%rdi
        setne %r10b
        test %esi,%esi
        setne %cl
        and %r10b,%cl
        movzbl %cl,%eax
        ret
        .size u_c_330, .-u_c_330
        .globl u_c_331
        .type u_c_331, @function
u_c_331:
        test %rdi,%rdi
        setne %r10b
        test %rsi,%rsi
        setne %cl
        and %r10b,%cl
        movzbl %cl,%eax
        ret
        .size u_c_331, .-u_c_331
        .globl u_c_332
        .type u_c_332, @function
u_c_332:
        test %rdi,%rdi
        setne %r10b
        test %rsi,%rsi
        setne %cl
        and %r10b,%cl
        movzbl %cl,%eax
        ret
        .size u_c_332, .-u_c_332
        .globl u_c_333
        .type u_c_333, @function
u_c_333:
        test %rdi,%rdi
        setne %r10b
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %cl
        setne %dl
        or %cl,%dl
        and %r10b,%dl
        movzbl %dl,%eax
        ret
        .size u_c_333, .-u_c_333
        .globl u_c_334
        .type u_c_334, @function
u_c_334:
        test %rdi,%rdi
        setne %r10b
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %cl
        setne %dl
        or %cl,%dl
        and %r10b,%dl
        movzbl %dl,%eax
        ret
        .size u_c_334, .-u_c_334
        .globl u_c_335
        .type u_c_335, @function
u_c_335:
        test %rdi,%rdi
        setne %r10b
        and %sil,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_335, .-u_c_335
        .globl u_c_336
        .type u_c_336, @function
u_c_336:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        test %edi,%edi
        setne %r10b
        and %cl,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_336, .-u_c_336
        .globl u_c_337
        .type u_c_337, @function
u_c_337:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        test %rdi,%rdi
        setne %r10b
        and %cl,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_337, .-u_c_337
        .globl u_c_338
        .type u_c_338, @function
u_c_338:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        test %rdi,%rdi
        setne %r10b
        and %cl,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_338, .-u_c_338
        .globl u_c_339
        .type u_c_339, @function
u_c_339:
        xorps %xmm2,%xmm2
        cmpneqss %xmm2,%xmm1
        cmpneqss %xmm2,%xmm0
        andps %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%eax
        ret
        .size u_c_339, .-u_c_339
        .globl u_c_340
        .type u_c_340, @function
u_c_340:
        xorps %xmm2,%xmm2
        ucomiss %xmm2,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        xorps %xmm2,%xmm2
        ucomisd %xmm2,%xmm1
        setp %r10b
        setne %dl
        or %r10b,%dl
        and %cl,%dl
        movzbl %dl,%eax
        ret
        .size u_c_340, .-u_c_340
        .globl u_c_341
        .type u_c_341, @function
u_c_341:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        and %dil,%cl
        movzbl %cl,%eax
        ret
        .size u_c_341, .-u_c_341
        .globl u_c_342
        .type u_c_342, @function
u_c_342:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        test %edi,%edi
        setne %r10b
        and %cl,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_342, .-u_c_342
        .globl u_c_343
        .type u_c_343, @function
u_c_343:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        test %rdi,%rdi
        setne %r10b
        and %cl,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_343, .-u_c_343
        .globl u_c_344
        .type u_c_344, @function
u_c_344:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        test %rdi,%rdi
        setne %r10b
        and %cl,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_344, .-u_c_344
        .globl u_c_345
        .type u_c_345, @function
u_c_345:
        xorpd %xmm2,%xmm2
        ucomisd %xmm2,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        xorpd %xmm2,%xmm2
        ucomiss %xmm2,%xmm1
        setp %r10b
        setne %dl
        or %r10b,%dl
        and %cl,%dl
        movzbl %dl,%eax
        ret
        .size u_c_345, .-u_c_345
        .globl u_c_346
        .type u_c_346, @function
u_c_346:
        xorpd %xmm2,%xmm2
        cmpneqsd %xmm2,%xmm1
        cmpneqsd %xmm2,%xmm0
        andpd %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%eax
        ret
        .size u_c_346, .-u_c_346
        .globl u_c_347
        .type u_c_347, @function
u_c_347:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        and %dil,%cl
        movzbl %cl,%eax
        ret
        .size u_c_347, .-u_c_347
        .globl u_c_348
        .type u_c_348, @function
u_c_348:
        test %esi,%esi
        setne %r10b
        and %dil,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_348, .-u_c_348
        .globl u_c_349
        .type u_c_349, @function
u_c_349:
        test %rsi,%rsi
        setne %r10b
        and %dil,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_349, .-u_c_349
        .globl u_c_350
        .type u_c_350, @function
u_c_350:
        test %rsi,%rsi
        setne %r10b
        and %dil,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_350, .-u_c_350
        .globl u_c_351
        .type u_c_351, @function
u_c_351:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        and %dil,%cl
        movzbl %cl,%eax
        ret
        .size u_c_351, .-u_c_351
        .globl u_c_352
        .type u_c_352, @function
u_c_352:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        and %dil,%cl
        movzbl %cl,%eax
        ret
        .size u_c_352, .-u_c_352
        .globl u_c_353
        .type u_c_353, @function
u_c_353:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_c_353, .-u_c_353
        .globl u_c_354
        .type u_c_354, @function
u_c_354:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_c_354, .-u_c_354
        .globl u_c_355
        .type u_c_355, @function
u_c_355:
        movslq %edi,%rax
        or %rsi,%rax
        ret
        .size u_c_355, .-u_c_355
        .globl u_c_356
        .type u_c_356, @function
u_c_356:
        movslq %edi,%rax
        or %rsi,%rax
        ret
        .size u_c_356, .-u_c_356
        .globl u_c_359
        .type u_c_359, @function
u_c_359:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_c_359, .-u_c_359
        .globl u_c_360
        .type u_c_360, @function
u_c_360:
        movslq %esi,%rax
        or %rdi,%rax
        ret
        .size u_c_360, .-u_c_360
        .globl u_c_361
        .type u_c_361, @function
u_c_361:
        mov %rdi,%rax
        or %rsi,%rax
        ret
        .size u_c_361, .-u_c_361
        .globl u_c_362
        .type u_c_362, @function
u_c_362:
        mov %rdi,%rax
        or %rsi,%rax
        ret
        .size u_c_362, .-u_c_362
        .globl u_c_365
        .type u_c_365, @function
u_c_365:
        mov %esi,%eax
        or %rdi,%rax
        ret
        .size u_c_365, .-u_c_365
        .globl u_c_366
        .type u_c_366, @function
u_c_366:
        movslq %esi,%rax
        or %rdi,%rax
        ret
        .size u_c_366, .-u_c_366
        .globl u_c_367
        .type u_c_367, @function
u_c_367:
        mov %rdi,%rax
        or %rsi,%rax
        ret
        .size u_c_367, .-u_c_367
        .globl u_c_368
        .type u_c_368, @function
u_c_368:
        mov %rdi,%rax
        or %rsi,%rax
        ret
        .size u_c_368, .-u_c_368
        .globl u_c_371
        .type u_c_371, @function
u_c_371:
        mov %esi,%eax
        or %rdi,%rax
        ret
        .size u_c_371, .-u_c_371
        .globl u_c_384
        .type u_c_384, @function
u_c_384:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_c_384, .-u_c_384
        .globl u_c_385
        .type u_c_385, @function
u_c_385:
        mov %edi,%eax
        or %rsi,%rax
        ret
        .size u_c_385, .-u_c_385
        .globl u_c_386
        .type u_c_386, @function
u_c_386:
        mov %edi,%eax
        or %rsi,%rax
        ret
        .size u_c_386, .-u_c_386
        .globl u_c_389
        .type u_c_389, @function
u_c_389:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_c_389, .-u_c_389
        .globl u_c_390
        .type u_c_390, @function
u_c_390:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_c_390, .-u_c_390
        .globl u_c_391
        .type u_c_391, @function
u_c_391:
        movslq %edi,%rax
        xor %rsi,%rax
        ret
        .size u_c_391, .-u_c_391
        .globl u_c_392
        .type u_c_392, @function
u_c_392:
        movslq %edi,%rax
        xor %rsi,%rax
        ret
        .size u_c_392, .-u_c_392
        .globl u_c_395
        .type u_c_395, @function
u_c_395:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_c_395, .-u_c_395
        .globl u_c_396
        .type u_c_396, @function
u_c_396:
        movslq %esi,%rax
        xor %rdi,%rax
        ret
        .size u_c_396, .-u_c_396
        .globl u_c_397
        .type u_c_397, @function
u_c_397:
        mov %rdi,%rax
        xor %rsi,%rax
        ret
        .size u_c_397, .-u_c_397
        .globl u_c_398
        .type u_c_398, @function
u_c_398:
        mov %rdi,%rax
        xor %rsi,%rax
        ret
        .size u_c_398, .-u_c_398
        .globl u_c_401
        .type u_c_401, @function
u_c_401:
        mov %esi,%eax
        xor %rdi,%rax
        ret
        .size u_c_401, .-u_c_401
        .globl u_c_402
        .type u_c_402, @function
u_c_402:
        movslq %esi,%rax
        xor %rdi,%rax
        ret
        .size u_c_402, .-u_c_402
        .globl u_c_403
        .type u_c_403, @function
u_c_403:
        mov %rdi,%rax
        xor %rsi,%rax
        ret
        .size u_c_403, .-u_c_403
        .globl u_c_404
        .type u_c_404, @function
u_c_404:
        mov %rdi,%rax
        xor %rsi,%rax
        ret
        .size u_c_404, .-u_c_404
        .globl u_c_407
        .type u_c_407, @function
u_c_407:
        mov %esi,%eax
        xor %rdi,%rax
        ret
        .size u_c_407, .-u_c_407
        .globl u_c_420
        .type u_c_420, @function
u_c_420:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_c_420, .-u_c_420
        .globl u_c_421
        .type u_c_421, @function
u_c_421:
        mov %edi,%eax
        xor %rsi,%rax
        ret
        .size u_c_421, .-u_c_421
        .globl u_c_422
        .type u_c_422, @function
u_c_422:
        mov %edi,%eax
        xor %rsi,%rax
        ret
        .size u_c_422, .-u_c_422
        .globl u_c_425
        .type u_c_425, @function
u_c_425:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_c_425, .-u_c_425
        .globl u_c_426
        .type u_c_426, @function
u_c_426:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_c_426, .-u_c_426
        .globl u_c_427
        .type u_c_427, @function
u_c_427:
        movslq %edi,%rax
        and %rsi,%rax
        ret
        .size u_c_427, .-u_c_427
        .globl u_c_428
        .type u_c_428, @function
u_c_428:
        movslq %edi,%rax
        and %rsi,%rax
        ret
        .size u_c_428, .-u_c_428
        .globl u_c_431
        .type u_c_431, @function
u_c_431:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_c_431, .-u_c_431
        .globl u_c_432
        .type u_c_432, @function
u_c_432:
        movslq %esi,%rax
        and %rdi,%rax
        ret
        .size u_c_432, .-u_c_432
        .globl u_c_433
        .type u_c_433, @function
u_c_433:
        mov %rdi,%rax
        and %rsi,%rax
        ret
        .size u_c_433, .-u_c_433
        .globl u_c_434
        .type u_c_434, @function
u_c_434:
        mov %rdi,%rax
        and %rsi,%rax
        ret
        .size u_c_434, .-u_c_434
        .globl u_c_437
        .type u_c_437, @function
u_c_437:
        mov %rdi,%rax
        and %esi,%eax
        ret
        .size u_c_437, .-u_c_437
        .globl u_c_438
        .type u_c_438, @function
u_c_438:
        movslq %esi,%rax
        and %rdi,%rax
        ret
        .size u_c_438, .-u_c_438
        .globl u_c_439
        .type u_c_439, @function
u_c_439:
        mov %rdi,%rax
        and %rsi,%rax
        ret
        .size u_c_439, .-u_c_439
        .globl u_c_440
        .type u_c_440, @function
u_c_440:
        mov %rdi,%rax
        and %rsi,%rax
        ret
        .size u_c_440, .-u_c_440
        .globl u_c_443
        .type u_c_443, @function
u_c_443:
        mov %rdi,%rax
        and %esi,%eax
        ret
        .size u_c_443, .-u_c_443
        .globl u_c_456
        .type u_c_456, @function
u_c_456:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_c_456, .-u_c_456
        .globl u_c_457
        .type u_c_457, @function
u_c_457:
        mov %rsi,%rax
        and %edi,%eax
        ret
        .size u_c_457, .-u_c_457
        .globl u_c_458
        .type u_c_458, @function
u_c_458:
        mov %rsi,%rax
        and %edi,%eax
        ret
        .size u_c_458, .-u_c_458
        .globl u_c_461
        .type u_c_461, @function
u_c_461:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_c_461, .-u_c_461
        .globl u_c_462
        .type u_c_462, @function
u_c_462:
        xor %eax,%eax
        cmp %esi,%edi
        sete %al
        ret
        .size u_c_462, .-u_c_462
        .globl u_c_463
        .type u_c_463, @function
u_c_463:
        movslq %edi,%rcx
        xor %eax,%eax
        cmp %rcx,%rsi
        sete %al
        ret
        .size u_c_463, .-u_c_463
        .globl u_c_464
        .type u_c_464, @function
u_c_464:
        movslq %edi,%rcx
        xor %eax,%eax
        cmp %rcx,%rsi
        sete %al
        ret
        .size u_c_464, .-u_c_464
        .globl u_c_465
        .type u_c_465, @function
u_c_465:
        cvtsi2ss %edi,%xmm1
        cmpeqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_c_465, .-u_c_465
        .globl u_c_466
        .type u_c_466, @function
u_c_466:
        cvtsi2sd %edi,%xmm1
        cmpeqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_c_466, .-u_c_466
        .globl u_c_467
        .type u_c_467, @function
u_c_467:
        xor %eax,%eax
        cmp %esi,%edi
        sete %al
        ret
        .size u_c_467, .-u_c_467
        .globl u_c_468
        .type u_c_468, @function
u_c_468:
        movslq %esi,%rcx
        xor %eax,%eax
        cmp %rcx,%rdi
        sete %al
        ret
        .size u_c_468, .-u_c_468
        .globl u_c_469
        .type u_c_469, @function
u_c_469:
        xor %eax,%eax
        cmp %rsi,%rdi
        sete %al
        ret
        .size u_c_469, .-u_c_469
        .globl u_c_470
        .type u_c_470, @function
u_c_470:
        xor %eax,%eax
        cmp %rsi,%rdi
        sete %al
        ret
        .size u_c_470, .-u_c_470
        .globl u_c_471
        .type u_c_471, @function
u_c_471:
        cvtsi2ss %rdi,%xmm1
        cmpeqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_c_471, .-u_c_471
        .globl u_c_472
        .type u_c_472, @function
u_c_472:
        cvtsi2sd %rdi,%xmm1
        cmpeqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_c_472, .-u_c_472
        .globl u_c_473
        .type u_c_473, @function
u_c_473:
        mov %esi,%ecx
        xor %eax,%eax
        cmp %rcx,%rdi
        sete %al
        ret
        .size u_c_473, .-u_c_473
        .globl u_c_474
        .type u_c_474, @function
u_c_474:
        movslq %esi,%rcx
        xor %eax,%eax
        cmp %rcx,%rdi
        sete %al
        ret
        .size u_c_474, .-u_c_474
        .globl u_c_475
        .type u_c_475, @function
u_c_475:
        xor %eax,%eax
        cmp %rsi,%rdi
        sete %al
        ret
        .size u_c_475, .-u_c_475
        .globl u_c_476
        .type u_c_476, @function
u_c_476:
        xor %eax,%eax
        cmp %rsi,%rdi
        sete %al
        ret
        .size u_c_476, .-u_c_476
        .globl u_c_479
        .type u_c_479, @function
u_c_479:
        mov %esi,%ecx
        xor %eax,%eax
        cmp %rcx,%rdi
        sete %al
        ret
        .size u_c_479, .-u_c_479
        .globl u_c_480
        .type u_c_480, @function
u_c_480:
        cvtsi2ss %edi,%xmm1
        cmpeqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_c_480, .-u_c_480
        .globl u_c_481
        .type u_c_481, @function
u_c_481:
        cvtsi2ss %rdi,%xmm1
        cmpeqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_c_481, .-u_c_481
        .globl u_c_483
        .type u_c_483, @function
u_c_483:
        cmpeqss %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%eax
        ret
        .size u_c_483, .-u_c_483
        .globl u_c_484
        .type u_c_484, @function
u_c_484:
        cvtss2sd %xmm0,%xmm2
        cmpeqsd %xmm1,%xmm2
        movq %xmm2,%rax
        and $0x1,%eax
        ret
        .size u_c_484, .-u_c_484
        .globl u_c_485
        .type u_c_485, @function
u_c_485:
        cvtsi2ss %edi,%xmm1
        cmpeqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_c_485, .-u_c_485
        .globl u_c_486
        .type u_c_486, @function
u_c_486:
        cvtsi2sd %edi,%xmm1
        cmpeqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_c_486, .-u_c_486
        .globl u_c_487
        .type u_c_487, @function
u_c_487:
        cvtsi2sd %rdi,%xmm1
        cmpeqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_c_487, .-u_c_487
        .globl u_c_489
        .type u_c_489, @function
u_c_489:
        cvtss2sd %xmm1,%xmm2
        cmpeqsd %xmm0,%xmm2
        movq %xmm2,%rax
        and $0x1,%eax
        ret
        .size u_c_489, .-u_c_489
        .globl u_c_490
        .type u_c_490, @function
u_c_490:
        cmpeqsd %xmm1,%xmm0
        movq %xmm0,%rax
        and $0x1,%eax
        ret
        .size u_c_490, .-u_c_490
        .globl u_c_491
        .type u_c_491, @function
u_c_491:
        cvtsi2sd %edi,%xmm1
        cmpeqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_c_491, .-u_c_491
        .globl u_c_492
        .type u_c_492, @function
u_c_492:
        xor %eax,%eax
        cmp %edi,%esi
        sete %al
        ret
        .size u_c_492, .-u_c_492
        .globl u_c_493
        .type u_c_493, @function
u_c_493:
        mov %edi,%ecx
        xor %eax,%eax
        cmp %rcx,%rsi
        sete %al
        ret
        .size u_c_493, .-u_c_493
        .globl u_c_494
        .type u_c_494, @function
u_c_494:
        mov %edi,%ecx
        xor %eax,%eax
        cmp %rcx,%rsi
        sete %al
        ret
        .size u_c_494, .-u_c_494
        .globl u_c_495
        .type u_c_495, @function
u_c_495:
        cvtsi2ss %edi,%xmm1
        cmpeqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_c_495, .-u_c_495
        .globl u_c_496
        .type u_c_496, @function
u_c_496:
        cvtsi2sd %edi,%xmm1
        cmpeqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_c_496, .-u_c_496
        .globl u_c_497
        .type u_c_497, @function
u_c_497:
        xor %esi,%edi
        xor $0x1,%dil
        movzbl %dil,%eax
        ret
        .size u_c_497, .-u_c_497
        .globl u_c_498
        .type u_c_498, @function
u_c_498:
        xor %eax,%eax
        cmp %esi,%edi
        setne %al
        ret
        .size u_c_498, .-u_c_498
        .globl u_c_499
        .type u_c_499, @function
u_c_499:
        movslq %edi,%rcx
        xor %eax,%eax
        cmp %rcx,%rsi
        setne %al
        ret
        .size u_c_499, .-u_c_499
        .globl u_c_500
        .type u_c_500, @function
u_c_500:
        movslq %edi,%rcx
        xor %eax,%eax
        cmp %rcx,%rsi
        setne %al
        ret
        .size u_c_500, .-u_c_500
        .globl u_c_501
        .type u_c_501, @function
u_c_501:
        cvtsi2ss %edi,%xmm1
        cmpneqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_c_501, .-u_c_501
        .globl u_c_502
        .type u_c_502, @function
u_c_502:
        cvtsi2sd %edi,%xmm1
        cmpneqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_c_502, .-u_c_502
        .globl u_c_503
        .type u_c_503, @function
u_c_503:
        xor %eax,%eax
        cmp %esi,%edi
        setne %al
        ret
        .size u_c_503, .-u_c_503
        .globl u_c_504
        .type u_c_504, @function
u_c_504:
        movslq %esi,%rcx
        xor %eax,%eax
        cmp %rcx,%rdi
        setne %al
        ret
        .size u_c_504, .-u_c_504
        .globl u_c_505
        .type u_c_505, @function
u_c_505:
        xor %eax,%eax
        cmp %rsi,%rdi
        setne %al
        ret
        .size u_c_505, .-u_c_505
        .globl u_c_506
        .type u_c_506, @function
u_c_506:
        xor %eax,%eax
        cmp %rsi,%rdi
        setne %al
        ret
        .size u_c_506, .-u_c_506
        .globl u_c_507
        .type u_c_507, @function
u_c_507:
        cvtsi2ss %rdi,%xmm1
        cmpneqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_c_507, .-u_c_507
        .globl u_c_508
        .type u_c_508, @function
u_c_508:
        cvtsi2sd %rdi,%xmm1
        cmpneqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_c_508, .-u_c_508
        .globl u_c_509
        .type u_c_509, @function
u_c_509:
        mov %esi,%ecx
        xor %eax,%eax
        cmp %rcx,%rdi
        setne %al
        ret
        .size u_c_509, .-u_c_509
        .globl u_c_510
        .type u_c_510, @function
u_c_510:
        movslq %esi,%rcx
        xor %eax,%eax
        cmp %rcx,%rdi
        setne %al
        ret
        .size u_c_510, .-u_c_510
        .globl u_c_511
        .type u_c_511, @function
u_c_511:
        xor %eax,%eax
        cmp %rsi,%rdi
        setne %al
        ret
        .size u_c_511, .-u_c_511
        .globl u_c_512
        .type u_c_512, @function
u_c_512:
        xor %eax,%eax
        cmp %rsi,%rdi
        setne %al
        ret
        .size u_c_512, .-u_c_512
        .globl u_c_515
        .type u_c_515, @function
u_c_515:
        mov %esi,%ecx
        xor %eax,%eax
        cmp %rcx,%rdi
        setne %al
        ret
        .size u_c_515, .-u_c_515
        .globl u_c_516
        .type u_c_516, @function
u_c_516:
        cvtsi2ss %edi,%xmm1
        cmpneqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_c_516, .-u_c_516
        .globl u_c_517
        .type u_c_517, @function
u_c_517:
        cvtsi2ss %rdi,%xmm1
        cmpneqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_c_517, .-u_c_517
        .globl u_c_519
        .type u_c_519, @function
u_c_519:
        cmpneqss %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%eax
        ret
        .size u_c_519, .-u_c_519
        .globl u_c_520
        .type u_c_520, @function
u_c_520:
        cvtss2sd %xmm0,%xmm2
        cmpneqsd %xmm1,%xmm2
        movq %xmm2,%rax
        and $0x1,%eax
        ret
        .size u_c_520, .-u_c_520
        .globl u_c_521
        .type u_c_521, @function
u_c_521:
        cvtsi2ss %edi,%xmm1
        cmpneqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_c_521, .-u_c_521
        .globl u_c_522
        .type u_c_522, @function
u_c_522:
        cvtsi2sd %edi,%xmm1
        cmpneqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_c_522, .-u_c_522
        .globl u_c_523
        .type u_c_523, @function
u_c_523:
        cvtsi2sd %rdi,%xmm1
        cmpneqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_c_523, .-u_c_523
        .globl u_c_525
        .type u_c_525, @function
u_c_525:
        cvtss2sd %xmm1,%xmm2
        cmpneqsd %xmm0,%xmm2
        movq %xmm2,%rax
        and $0x1,%eax
        ret
        .size u_c_525, .-u_c_525
        .globl u_c_526
        .type u_c_526, @function
u_c_526:
        cmpneqsd %xmm1,%xmm0
        movq %xmm0,%rax
        and $0x1,%eax
        ret
        .size u_c_526, .-u_c_526
        .globl u_c_527
        .type u_c_527, @function
u_c_527:
        cvtsi2sd %edi,%xmm1
        cmpneqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_c_527, .-u_c_527
        .globl u_c_528
        .type u_c_528, @function
u_c_528:
        xor %eax,%eax
        cmp %edi,%esi
        setne %al
        ret
        .size u_c_528, .-u_c_528
        .globl u_c_529
        .type u_c_529, @function
u_c_529:
        mov %edi,%ecx
        xor %eax,%eax
        cmp %rcx,%rsi
        setne %al
        ret
        .size u_c_529, .-u_c_529
        .globl u_c_530
        .type u_c_530, @function
u_c_530:
        mov %edi,%ecx
        xor %eax,%eax
        cmp %rcx,%rsi
        setne %al
        ret
        .size u_c_530, .-u_c_530
        .globl u_c_531
        .type u_c_531, @function
u_c_531:
        cvtsi2ss %edi,%xmm1
        cmpneqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_c_531, .-u_c_531
        .globl u_c_532
        .type u_c_532, @function
u_c_532:
        cvtsi2sd %edi,%xmm1
        cmpneqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_c_532, .-u_c_532
        .globl u_c_533
        .type u_c_533, @function
u_c_533:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_c_533, .-u_c_533
        .globl u_c_534
        .type u_c_534, @function
u_c_534:
        xor %eax,%eax
        cmp %esi,%edi
        setg %al
        ret
        .size u_c_534, .-u_c_534
        .globl u_c_535
        .type u_c_535, @function
u_c_535:
        movslq %edi,%rcx
        xor %eax,%eax
        cmp %rcx,%rsi
        setl %al
        ret
        .size u_c_535, .-u_c_535
        .globl u_c_536
        .type u_c_536, @function
u_c_536:
        movslq %edi,%rcx
        xor %eax,%eax
        cmp %rcx,%rsi
        setb %al
        ret
        .size u_c_536, .-u_c_536
        .globl u_c_537
        .type u_c_537, @function
u_c_537:
        cvtsi2ss %edi,%xmm1
        xor %eax,%eax
        ucomiss %xmm0,%xmm1
        seta %al
        ret
        .size u_c_537, .-u_c_537
        .globl u_c_538
        .type u_c_538, @function
u_c_538:
        cvtsi2sd %edi,%xmm1
        xor %eax,%eax
        ucomisd %xmm0,%xmm1
        seta %al
        ret
        .size u_c_538, .-u_c_538
        .globl u_c_539
        .type u_c_539, @function
u_c_539:
        xor %eax,%eax
        cmp %esi,%edi
        setg %al
        ret
        .size u_c_539, .-u_c_539
        .globl u_c_540
        .type u_c_540, @function
u_c_540:
        movslq %esi,%rcx
        xor %eax,%eax
        cmp %rcx,%rdi
        setg %al
        ret
        .size u_c_540, .-u_c_540
        .globl u_c_541
        .type u_c_541, @function
u_c_541:
        xor %eax,%eax
        cmp %rsi,%rdi
        setg %al
        ret
        .size u_c_541, .-u_c_541
        .globl u_c_542
        .type u_c_542, @function
u_c_542:
        xor %eax,%eax
        cmp %rsi,%rdi
        seta %al
        ret
        .size u_c_542, .-u_c_542
        .globl u_c_543
        .type u_c_543, @function
u_c_543:
        cvtsi2ss %rdi,%xmm1
        xor %eax,%eax
        ucomiss %xmm0,%xmm1
        seta %al
        ret
        .size u_c_543, .-u_c_543
        .globl u_c_544
        .type u_c_544, @function
u_c_544:
        cvtsi2sd %rdi,%xmm1
        xor %eax,%eax
        ucomisd %xmm0,%xmm1
        seta %al
        ret
        .size u_c_544, .-u_c_544
        .globl u_c_545
        .type u_c_545, @function
u_c_545:
        mov %esi,%ecx
        xor %eax,%eax
        cmp %rcx,%rdi
        setg %al
        ret
        .size u_c_545, .-u_c_545
        .globl u_c_546
        .type u_c_546, @function
u_c_546:
        movslq %esi,%rcx
        xor %eax,%eax
        cmp %rcx,%rdi
        seta %al
        ret
        .size u_c_546, .-u_c_546
        .globl u_c_547
        .type u_c_547, @function
u_c_547:
        xor %eax,%eax
        cmp %rsi,%rdi
        seta %al
        ret
        .size u_c_547, .-u_c_547
        .globl u_c_548
        .type u_c_548, @function
u_c_548:
        xor %eax,%eax
        cmp %rsi,%rdi
        seta %al
        ret
        .size u_c_548, .-u_c_548
        .globl u_c_551
        .type u_c_551, @function
u_c_551:
        mov %esi,%ecx
        xor %eax,%eax
        cmp %rcx,%rdi
        seta %al
        ret
        .size u_c_551, .-u_c_551
        .globl u_c_552
        .type u_c_552, @function
u_c_552:
        cvtsi2ss %edi,%xmm1
        xor %eax,%eax
        ucomiss %xmm1,%xmm0
        seta %al
        ret
        .size u_c_552, .-u_c_552
        .globl u_c_553
        .type u_c_553, @function
u_c_553:
        cvtsi2ss %rdi,%xmm1
        xor %eax,%eax
        ucomiss %xmm1,%xmm0
        seta %al
        ret
        .size u_c_553, .-u_c_553
        .globl u_c_555
        .type u_c_555, @function
u_c_555:
        xor %eax,%eax
        ucomiss %xmm1,%xmm0
        seta %al
        ret
        .size u_c_555, .-u_c_555
        .globl u_c_556
        .type u_c_556, @function
u_c_556:
        cvtss2sd %xmm0,%xmm2
        xor %eax,%eax
        ucomisd %xmm1,%xmm2
        seta %al
        ret
        .size u_c_556, .-u_c_556
        .globl u_c_557
        .type u_c_557, @function
u_c_557:
        cvtsi2ss %edi,%xmm1
        xor %eax,%eax
        ucomiss %xmm1,%xmm0
        seta %al
        ret
        .size u_c_557, .-u_c_557
        .globl u_c_558
        .type u_c_558, @function
u_c_558:
        cvtsi2sd %edi,%xmm1
        xor %eax,%eax
        ucomisd %xmm1,%xmm0
        seta %al
        ret
        .size u_c_558, .-u_c_558
        .globl u_c_559
        .type u_c_559, @function
u_c_559:
        cvtsi2sd %rdi,%xmm1
        xor %eax,%eax
        ucomisd %xmm1,%xmm0
        seta %al
        ret
        .size u_c_559, .-u_c_559
        .globl u_c_561
        .type u_c_561, @function
u_c_561:
        cvtss2sd %xmm1,%xmm2
        xor %eax,%eax
        ucomisd %xmm2,%xmm0
        seta %al
        ret
        .size u_c_561, .-u_c_561
        .globl u_c_562
        .type u_c_562, @function
u_c_562:
        xor %eax,%eax
        ucomisd %xmm1,%xmm0
        seta %al
        ret
        .size u_c_562, .-u_c_562
        .globl u_c_563
        .type u_c_563, @function
u_c_563:
        cvtsi2sd %edi,%xmm1
        xor %eax,%eax
        ucomisd %xmm1,%xmm0
        seta %al
        ret
        .size u_c_563, .-u_c_563
        .globl u_c_564
        .type u_c_564, @function
u_c_564:
        xor %eax,%eax
        cmp %edi,%esi
        setl %al
        ret
        .size u_c_564, .-u_c_564
        .globl u_c_565
        .type u_c_565, @function
u_c_565:
        mov %edi,%ecx
        xor %eax,%eax
        cmp %rcx,%rsi
        setl %al
        ret
        .size u_c_565, .-u_c_565
        .globl u_c_566
        .type u_c_566, @function
u_c_566:
        test %rsi,%rsi
        sete %r10b
        and %dil,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_566, .-u_c_566
        .globl u_c_567
        .type u_c_567, @function
u_c_567:
        cvtsi2ss %edi,%xmm1
        xor %eax,%eax
        ucomiss %xmm0,%xmm1
        seta %al
        ret
        .size u_c_567, .-u_c_567
        .globl u_c_568
        .type u_c_568, @function
u_c_568:
        cvtsi2sd %edi,%xmm1
        xor %eax,%eax
        ucomisd %xmm0,%xmm1
        seta %al
        ret
        .size u_c_568, .-u_c_568
        .globl u_c_569
        .type u_c_569, @function
u_c_569:
        xor $0x1,%sil
        and %dil,%sil
        movzbl %sil,%eax
        ret
        .size u_c_569, .-u_c_569
        .globl u_c_570
        .type u_c_570, @function
u_c_570:
        xor %eax,%eax
        cmp %esi,%edi
        setge %al
        ret
        .size u_c_570, .-u_c_570
        .globl u_c_571
        .type u_c_571, @function
u_c_571:
        movslq %edi,%rcx
        xor %eax,%eax
        cmp %rcx,%rsi
        setle %al
        ret
        .size u_c_571, .-u_c_571
        .globl u_c_572
        .type u_c_572, @function
u_c_572:
        movslq %edi,%rcx
        xor %eax,%eax
        cmp %rcx,%rsi
        setbe %al
        ret
        .size u_c_572, .-u_c_572
        .globl u_c_573
        .type u_c_573, @function
u_c_573:
        cvtsi2ss %edi,%xmm1
        xor %eax,%eax
        ucomiss %xmm0,%xmm1
        setae %al
        ret
        .size u_c_573, .-u_c_573
        .globl u_c_574
        .type u_c_574, @function
u_c_574:
        cvtsi2sd %edi,%xmm1
        xor %eax,%eax
        ucomisd %xmm0,%xmm1
        setae %al
        ret
        .size u_c_574, .-u_c_574
        .globl u_c_575
        .type u_c_575, @function
u_c_575:
        xor %eax,%eax
        cmp %esi,%edi
        setge %al
        ret
        .size u_c_575, .-u_c_575
        .globl u_c_576
        .type u_c_576, @function
u_c_576:
        movslq %esi,%rcx
        xor %eax,%eax
        cmp %rcx,%rdi
        setge %al
        ret
        .size u_c_576, .-u_c_576
        .globl u_c_577
        .type u_c_577, @function
u_c_577:
        xor %eax,%eax
        cmp %rsi,%rdi
        setge %al
        ret
        .size u_c_577, .-u_c_577
        .globl u_c_578
        .type u_c_578, @function
u_c_578:
        xor %eax,%eax
        cmp %rsi,%rdi
        setae %al
        ret
        .size u_c_578, .-u_c_578
        .globl u_c_579
        .type u_c_579, @function
u_c_579:
        cvtsi2ss %rdi,%xmm1
        xor %eax,%eax
        ucomiss %xmm0,%xmm1
        setae %al
        ret
        .size u_c_579, .-u_c_579
        .globl u_c_580
        .type u_c_580, @function
u_c_580:
        cvtsi2sd %rdi,%xmm1
        xor %eax,%eax
        ucomisd %xmm0,%xmm1
        setae %al
        ret
        .size u_c_580, .-u_c_580
        .globl u_c_581
        .type u_c_581, @function
u_c_581:
        mov %esi,%ecx
        xor %eax,%eax
        cmp %rcx,%rdi
        setge %al
        ret
        .size u_c_581, .-u_c_581
        .globl u_c_582
        .type u_c_582, @function
u_c_582:
        movslq %esi,%rcx
        xor %eax,%eax
        cmp %rcx,%rdi
        setae %al
        ret
        .size u_c_582, .-u_c_582
        .globl u_c_583
        .type u_c_583, @function
u_c_583:
        xor %eax,%eax
        cmp %rsi,%rdi
        setae %al
        ret
        .size u_c_583, .-u_c_583
        .globl u_c_584
        .type u_c_584, @function
u_c_584:
        xor %eax,%eax
        cmp %rsi,%rdi
        setae %al
        ret
        .size u_c_584, .-u_c_584
        .globl u_c_587
        .type u_c_587, @function
u_c_587:
        mov %esi,%ecx
        xor %eax,%eax
        cmp %rcx,%rdi
        setae %al
        ret
        .size u_c_587, .-u_c_587
        .globl u_c_588
        .type u_c_588, @function
u_c_588:
        cvtsi2ss %edi,%xmm1
        xor %eax,%eax
        ucomiss %xmm1,%xmm0
        setae %al
        ret
        .size u_c_588, .-u_c_588
        .globl u_c_589
        .type u_c_589, @function
u_c_589:
        cvtsi2ss %rdi,%xmm1
        xor %eax,%eax
        ucomiss %xmm1,%xmm0
        setae %al
        ret
        .size u_c_589, .-u_c_589
        .globl u_c_591
        .type u_c_591, @function
u_c_591:
        xor %eax,%eax
        ucomiss %xmm1,%xmm0
        setae %al
        ret
        .size u_c_591, .-u_c_591
        .globl u_c_592
        .type u_c_592, @function
u_c_592:
        cvtss2sd %xmm0,%xmm2
        xor %eax,%eax
        ucomisd %xmm1,%xmm2
        setae %al
        ret
        .size u_c_592, .-u_c_592
        .globl u_c_593
        .type u_c_593, @function
u_c_593:
        cvtsi2ss %edi,%xmm1
        xor %eax,%eax
        ucomiss %xmm1,%xmm0
        setae %al
        ret
        .size u_c_593, .-u_c_593
        .globl u_c_594
        .type u_c_594, @function
u_c_594:
        cvtsi2sd %edi,%xmm1
        xor %eax,%eax
        ucomisd %xmm1,%xmm0
        setae %al
        ret
        .size u_c_594, .-u_c_594
        .globl u_c_595
        .type u_c_595, @function
u_c_595:
        cvtsi2sd %rdi,%xmm1
        xor %eax,%eax
        ucomisd %xmm1,%xmm0
        setae %al
        ret
        .size u_c_595, .-u_c_595
        .globl u_c_597
        .type u_c_597, @function
u_c_597:
        cvtss2sd %xmm1,%xmm2
        xor %eax,%eax
        ucomisd %xmm2,%xmm0
        setae %al
        ret
        .size u_c_597, .-u_c_597
        .globl u_c_598
        .type u_c_598, @function
u_c_598:
        xor %eax,%eax
        ucomisd %xmm1,%xmm0
        setae %al
        ret
        .size u_c_598, .-u_c_598
        .globl u_c_599
        .type u_c_599, @function
u_c_599:
        cvtsi2sd %edi,%xmm1
        xor %eax,%eax
        ucomisd %xmm1,%xmm0
        setae %al
        ret
        .size u_c_599, .-u_c_599
        .globl u_c_600
        .type u_c_600, @function
u_c_600:
        xor %eax,%eax
        cmp %edi,%esi
        setle %al
        ret
        .size u_c_600, .-u_c_600
        .globl u_c_601
        .type u_c_601, @function
u_c_601:
        mov %edi,%ecx
        xor %eax,%eax
        cmp %rcx,%rsi
        setle %al
        ret
        .size u_c_601, .-u_c_601
        .globl u_c_602
        .type u_c_602, @function
u_c_602:
        mov %edi,%ecx
        xor %eax,%eax
        cmp %rcx,%rsi
        setbe %al
        ret
        .size u_c_602, .-u_c_602
        .globl u_c_603
        .type u_c_603, @function
u_c_603:
        cvtsi2ss %edi,%xmm1
        xor %eax,%eax
        ucomiss %xmm0,%xmm1
        setae %al
        ret
        .size u_c_603, .-u_c_603
        .globl u_c_604
        .type u_c_604, @function
u_c_604:
        cvtsi2sd %edi,%xmm1
        xor %eax,%eax
        ucomisd %xmm0,%xmm1
        setae %al
        ret
        .size u_c_604, .-u_c_604
        .globl u_c_605
        .type u_c_605, @function
u_c_605:
        xor $0x1,%sil
        or %dil,%sil
        movzbl %sil,%eax
        ret
        .size u_c_605, .-u_c_605
        .globl u_c_606
        .type u_c_606, @function
u_c_606:
        xor %eax,%eax
        cmp %esi,%edi
        setle %al
        ret
        .size u_c_606, .-u_c_606
        .globl u_c_607
        .type u_c_607, @function
u_c_607:
        movslq %edi,%rcx
        xor %eax,%eax
        cmp %rcx,%rsi
        setge %al
        ret
        .size u_c_607, .-u_c_607
        .globl u_c_608
        .type u_c_608, @function
u_c_608:
        movslq %edi,%rcx
        xor %eax,%eax
        cmp %rcx,%rsi
        setae %al
        ret
        .size u_c_608, .-u_c_608
        .globl u_c_609
        .type u_c_609, @function
u_c_609:
        cvtsi2ss %edi,%xmm1
        xor %eax,%eax
        ucomiss %xmm1,%xmm0
        setae %al
        ret
        .size u_c_609, .-u_c_609
        .globl u_c_610
        .type u_c_610, @function
u_c_610:
        cvtsi2sd %edi,%xmm1
        xor %eax,%eax
        ucomisd %xmm1,%xmm0
        setae %al
        ret
        .size u_c_610, .-u_c_610
        .globl u_c_611
        .type u_c_611, @function
u_c_611:
        xor %eax,%eax
        cmp %esi,%edi
        setle %al
        ret
        .size u_c_611, .-u_c_611
        .globl u_c_612
        .type u_c_612, @function
u_c_612:
        movslq %esi,%rcx
        xor %eax,%eax
        cmp %rcx,%rdi
        setle %al
        ret
        .size u_c_612, .-u_c_612
        .globl u_c_613
        .type u_c_613, @function
u_c_613:
        xor %eax,%eax
        cmp %rsi,%rdi
        setle %al
        ret
        .size u_c_613, .-u_c_613
        .globl u_c_614
        .type u_c_614, @function
u_c_614:
        xor %eax,%eax
        cmp %rsi,%rdi
        setbe %al
        ret
        .size u_c_614, .-u_c_614
        .globl u_c_615
        .type u_c_615, @function
u_c_615:
        cvtsi2ss %rdi,%xmm1
        xor %eax,%eax
        ucomiss %xmm1,%xmm0
        setae %al
        ret
        .size u_c_615, .-u_c_615
        .globl u_c_616
        .type u_c_616, @function
u_c_616:
        cvtsi2sd %rdi,%xmm1
        xor %eax,%eax
        ucomisd %xmm1,%xmm0
        setae %al
        ret
        .size u_c_616, .-u_c_616
        .globl u_c_617
        .type u_c_617, @function
u_c_617:
        mov %esi,%ecx
        xor %eax,%eax
        cmp %rcx,%rdi
        setle %al
        ret
        .size u_c_617, .-u_c_617
        .globl u_c_618
        .type u_c_618, @function
u_c_618:
        movslq %esi,%rcx
        xor %eax,%eax
        cmp %rcx,%rdi
        setbe %al
        ret
        .size u_c_618, .-u_c_618
        .globl u_c_619
        .type u_c_619, @function
u_c_619:
        xor %eax,%eax
        cmp %rsi,%rdi
        setbe %al
        ret
        .size u_c_619, .-u_c_619
        .globl u_c_620
        .type u_c_620, @function
u_c_620:
        xor %eax,%eax
        cmp %rsi,%rdi
        setbe %al
        ret
        .size u_c_620, .-u_c_620
        .globl u_c_623
        .type u_c_623, @function
u_c_623:
        mov %esi,%ecx
        xor %eax,%eax
        cmp %rcx,%rdi
        setbe %al
        ret
        .size u_c_623, .-u_c_623
        .globl u_c_624
        .type u_c_624, @function
u_c_624:
        cvtsi2ss %edi,%xmm1
        xor %eax,%eax
        ucomiss %xmm0,%xmm1
        setae %al
        ret
        .size u_c_624, .-u_c_624
        .globl u_c_625
        .type u_c_625, @function
u_c_625:
        cvtsi2ss %rdi,%xmm1
        xor %eax,%eax
        ucomiss %xmm0,%xmm1
        setae %al
        ret
        .size u_c_625, .-u_c_625
        .globl u_c_627
        .type u_c_627, @function
u_c_627:
        xor %eax,%eax
        ucomiss %xmm0,%xmm1
        setae %al
        ret
        .size u_c_627, .-u_c_627
        .globl u_c_628
        .type u_c_628, @function
u_c_628:
        cvtss2sd %xmm0,%xmm2
        xor %eax,%eax
        ucomisd %xmm2,%xmm1
        setae %al
        ret
        .size u_c_628, .-u_c_628
        .globl u_c_629
        .type u_c_629, @function
u_c_629:
        cvtsi2ss %edi,%xmm1
        xor %eax,%eax
        ucomiss %xmm0,%xmm1
        setae %al
        ret
        .size u_c_629, .-u_c_629
        .globl u_c_630
        .type u_c_630, @function
u_c_630:
        cvtsi2sd %edi,%xmm1
        xor %eax,%eax
        ucomisd %xmm0,%xmm1
        setae %al
        ret
        .size u_c_630, .-u_c_630
        .globl u_c_631
        .type u_c_631, @function
u_c_631:
        cvtsi2sd %rdi,%xmm1
        xor %eax,%eax
        ucomisd %xmm0,%xmm1
        setae %al
        ret
        .size u_c_631, .-u_c_631
        .globl u_c_633
        .type u_c_633, @function
u_c_633:
        cvtss2sd %xmm1,%xmm2
        xor %eax,%eax
        ucomisd %xmm0,%xmm2
        setae %al
        ret
        .size u_c_633, .-u_c_633
        .globl u_c_634
        .type u_c_634, @function
u_c_634:
        xor %eax,%eax
        ucomisd %xmm0,%xmm1
        setae %al
        ret
        .size u_c_634, .-u_c_634
        .globl u_c_635
        .type u_c_635, @function
u_c_635:
        cvtsi2sd %edi,%xmm1
        xor %eax,%eax
        ucomisd %xmm0,%xmm1
        setae %al
        ret
        .size u_c_635, .-u_c_635
        .globl u_c_636
        .type u_c_636, @function
u_c_636:
        xor %eax,%eax
        cmp %edi,%esi
        setge %al
        ret
        .size u_c_636, .-u_c_636
        .globl u_c_637
        .type u_c_637, @function
u_c_637:
        mov %edi,%ecx
        xor %eax,%eax
        cmp %rcx,%rsi
        setge %al
        ret
        .size u_c_637, .-u_c_637
        .globl u_c_638
        .type u_c_638, @function
u_c_638:
        mov %edi,%ecx
        xor %eax,%eax
        cmp %rcx,%rsi
        setae %al
        ret
        .size u_c_638, .-u_c_638
        .globl u_c_639
        .type u_c_639, @function
u_c_639:
        cvtsi2ss %edi,%xmm1
        xor %eax,%eax
        ucomiss %xmm1,%xmm0
        setae %al
        ret
        .size u_c_639, .-u_c_639
        .globl u_c_640
        .type u_c_640, @function
u_c_640:
        cvtsi2sd %edi,%xmm1
        xor %eax,%eax
        ucomisd %xmm1,%xmm0
        setae %al
        ret
        .size u_c_640, .-u_c_640
        .globl u_c_641
        .type u_c_641, @function
u_c_641:
        xor $0x1,%dil
        or %sil,%dil
        movzbl %dil,%eax
        ret
        .size u_c_641, .-u_c_641
        .globl u_c_642
        .type u_c_642, @function
u_c_642:
        xor %eax,%eax
        cmp %esi,%edi
        setl %al
        ret
        .size u_c_642, .-u_c_642
        .globl u_c_643
        .type u_c_643, @function
u_c_643:
        movslq %edi,%rcx
        xor %eax,%eax
        cmp %rcx,%rsi
        setg %al
        ret
        .size u_c_643, .-u_c_643
        .globl u_c_644
        .type u_c_644, @function
u_c_644:
        movslq %edi,%rcx
        xor %eax,%eax
        cmp %rcx,%rsi
        seta %al
        ret
        .size u_c_644, .-u_c_644
        .globl u_c_645
        .type u_c_645, @function
u_c_645:
        cvtsi2ss %edi,%xmm1
        xor %eax,%eax
        ucomiss %xmm1,%xmm0
        seta %al
        ret
        .size u_c_645, .-u_c_645
        .globl u_c_646
        .type u_c_646, @function
u_c_646:
        cvtsi2sd %edi,%xmm1
        xor %eax,%eax
        ucomisd %xmm1,%xmm0
        seta %al
        ret
        .size u_c_646, .-u_c_646
        .globl u_c_647
        .type u_c_647, @function
u_c_647:
        xor %eax,%eax
        cmp %esi,%edi
        setl %al
        ret
        .size u_c_647, .-u_c_647
        .globl u_c_648
        .type u_c_648, @function
u_c_648:
        movslq %esi,%rcx
        xor %eax,%eax
        cmp %rcx,%rdi
        setl %al
        ret
        .size u_c_648, .-u_c_648
        .globl u_c_649
        .type u_c_649, @function
u_c_649:
        xor %eax,%eax
        cmp %rsi,%rdi
        setl %al
        ret
        .size u_c_649, .-u_c_649
        .globl u_c_650
        .type u_c_650, @function
u_c_650:
        xor %eax,%eax
        cmp %rsi,%rdi
        setb %al
        ret
        .size u_c_650, .-u_c_650
        .globl u_c_651
        .type u_c_651, @function
u_c_651:
        cvtsi2ss %rdi,%xmm1
        xor %eax,%eax
        ucomiss %xmm1,%xmm0
        seta %al
        ret
        .size u_c_651, .-u_c_651
        .globl u_c_652
        .type u_c_652, @function
u_c_652:
        cvtsi2sd %rdi,%xmm1
        xor %eax,%eax
        ucomisd %xmm1,%xmm0
        seta %al
        ret
        .size u_c_652, .-u_c_652
        .globl u_c_653
        .type u_c_653, @function
u_c_653:
        mov %esi,%ecx
        xor %eax,%eax
        cmp %rcx,%rdi
        setl %al
        ret
        .size u_c_653, .-u_c_653
        .globl u_c_654
        .type u_c_654, @function
u_c_654:
        movslq %esi,%rcx
        xor %eax,%eax
        cmp %rcx,%rdi
        setb %al
        ret
        .size u_c_654, .-u_c_654
        .globl u_c_655
        .type u_c_655, @function
u_c_655:
        xor %eax,%eax
        cmp %rsi,%rdi
        setb %al
        ret
        .size u_c_655, .-u_c_655
        .globl u_c_656
        .type u_c_656, @function
u_c_656:
        xor %eax,%eax
        cmp %rsi,%rdi
        setb %al
        ret
        .size u_c_656, .-u_c_656
        .globl u_c_659
        .type u_c_659, @function
u_c_659:
        test %rdi,%rdi
        sete %r10b
        and %sil,%r10b
        movzbl %r10b,%eax
        ret
        .size u_c_659, .-u_c_659
        .globl u_c_660
        .type u_c_660, @function
u_c_660:
        cvtsi2ss %edi,%xmm1
        xor %eax,%eax
        ucomiss %xmm0,%xmm1
        seta %al
        ret
        .size u_c_660, .-u_c_660
        .globl u_c_661
        .type u_c_661, @function
u_c_661:
        cvtsi2ss %rdi,%xmm1
        xor %eax,%eax
        ucomiss %xmm0,%xmm1
        seta %al
        ret
        .size u_c_661, .-u_c_661
        .globl u_c_663
        .type u_c_663, @function
u_c_663:
        xor %eax,%eax
        ucomiss %xmm0,%xmm1
        seta %al
        ret
        .size u_c_663, .-u_c_663
        .globl u_c_664
        .type u_c_664, @function
u_c_664:
        cvtss2sd %xmm0,%xmm2
        xor %eax,%eax
        ucomisd %xmm2,%xmm1
        seta %al
        ret
        .size u_c_664, .-u_c_664
        .globl u_c_665
        .type u_c_665, @function
u_c_665:
        cvtsi2ss %edi,%xmm1
        xor %eax,%eax
        ucomiss %xmm0,%xmm1
        seta %al
        ret
        .size u_c_665, .-u_c_665
        .globl u_c_666
        .type u_c_666, @function
u_c_666:
        cvtsi2sd %edi,%xmm1
        xor %eax,%eax
        ucomisd %xmm0,%xmm1
        seta %al
        ret
        .size u_c_666, .-u_c_666
        .globl u_c_667
        .type u_c_667, @function
u_c_667:
        cvtsi2sd %rdi,%xmm1
        xor %eax,%eax
        ucomisd %xmm0,%xmm1
        seta %al
        ret
        .size u_c_667, .-u_c_667
        .globl u_c_669
        .type u_c_669, @function
u_c_669:
        cvtss2sd %xmm1,%xmm2
        xor %eax,%eax
        ucomisd %xmm0,%xmm2
        seta %al
        ret
        .size u_c_669, .-u_c_669
        .globl u_c_670
        .type u_c_670, @function
u_c_670:
        xor %eax,%eax
        ucomisd %xmm0,%xmm1
        seta %al
        ret
        .size u_c_670, .-u_c_670
        .globl u_c_671
        .type u_c_671, @function
u_c_671:
        cvtsi2sd %edi,%xmm1
        xor %eax,%eax
        ucomisd %xmm0,%xmm1
        seta %al
        ret
        .size u_c_671, .-u_c_671
        .globl u_c_672
        .type u_c_672, @function
u_c_672:
        xor %eax,%eax
        cmp %edi,%esi
        setg %al
        ret
        .size u_c_672, .-u_c_672
        .globl u_c_673
        .type u_c_673, @function
u_c_673:
        mov %edi,%ecx
        xor %eax,%eax
        cmp %rcx,%rsi
        setg %al
        ret
        .size u_c_673, .-u_c_673
        .globl u_c_674
        .type u_c_674, @function
u_c_674:
        mov %edi,%ecx
        xor %eax,%eax
        cmp %rcx,%rsi
        seta %al
        ret
        .size u_c_674, .-u_c_674
        .globl u_c_675
        .type u_c_675, @function
u_c_675:
        cvtsi2ss %edi,%xmm1
        xor %eax,%eax
        ucomiss %xmm1,%xmm0
        seta %al
        ret
        .size u_c_675, .-u_c_675
        .globl u_c_676
        .type u_c_676, @function
u_c_676:
        cvtsi2sd %edi,%xmm1
        xor %eax,%eax
        ucomisd %xmm1,%xmm0
        seta %al
        ret
        .size u_c_676, .-u_c_676
        .globl u_c_677
        .type u_c_677, @function
u_c_677:
        xor $0x1,%dil
        and %sil,%dil
        movzbl %dil,%eax
        ret
        .size u_c_677, .-u_c_677
        .globl u_c_678
        .type u_c_678, @function
u_c_678:
        mov %esi,%ecx
        mov %edi,%eax
        shl %cl,%eax
        ret
        .size u_c_678, .-u_c_678
        .globl u_c_679
        .type u_c_679, @function
u_c_679:
        mov %rsi,%rcx
        mov %edi,%eax
        shl %cl,%eax
        ret
        .size u_c_679, .-u_c_679
        .globl u_c_680
        .type u_c_680, @function
u_c_680:
        mov %rsi,%rcx
        mov %edi,%eax
        shl %cl,%eax
        ret
        .size u_c_680, .-u_c_680
        .globl u_c_683
        .type u_c_683, @function
u_c_683:
        mov %esi,%ecx
        mov %edi,%eax
        shl %cl,%eax
        ret
        .size u_c_683, .-u_c_683
        .globl u_c_684
        .type u_c_684, @function
u_c_684:
        mov %esi,%ecx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_c_684, .-u_c_684
        .globl u_c_685
        .type u_c_685, @function
u_c_685:
        mov %rsi,%rcx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_c_685, .-u_c_685
        .globl u_c_686
        .type u_c_686, @function
u_c_686:
        mov %rsi,%rcx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_c_686, .-u_c_686
        .globl u_c_689
        .type u_c_689, @function
u_c_689:
        mov %esi,%ecx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_c_689, .-u_c_689
        .globl u_c_690
        .type u_c_690, @function
u_c_690:
        mov %esi,%ecx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_c_690, .-u_c_690
        .globl u_c_691
        .type u_c_691, @function
u_c_691:
        mov %rsi,%rcx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_c_691, .-u_c_691
        .globl u_c_692
        .type u_c_692, @function
u_c_692:
        mov %rsi,%rcx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_c_692, .-u_c_692
        .globl u_c_695
        .type u_c_695, @function
u_c_695:
        mov %esi,%ecx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_c_695, .-u_c_695
        .globl u_c_708
        .type u_c_708, @function
u_c_708:
        mov %esi,%ecx
        mov %edi,%eax
        shl %cl,%eax
        ret
        .size u_c_708, .-u_c_708
        .globl u_c_709
        .type u_c_709, @function
u_c_709:
        mov %rsi,%rcx
        mov %edi,%eax
        shl %cl,%eax
        ret
        .size u_c_709, .-u_c_709
        .globl u_c_710
        .type u_c_710, @function
u_c_710:
        mov %rsi,%rcx
        mov %edi,%eax
        shl %cl,%eax
        ret
        .size u_c_710, .-u_c_710
        .globl u_c_713
        .type u_c_713, @function
u_c_713:
        mov %esi,%ecx
        mov %edi,%eax
        shl %cl,%eax
        ret
        .size u_c_713, .-u_c_713
        .globl u_c_714
        .type u_c_714, @function
u_c_714:
        mov %esi,%ecx
        mov %edi,%eax
        sar %cl,%eax
        ret
        .size u_c_714, .-u_c_714
        .globl u_c_715
        .type u_c_715, @function
u_c_715:
        mov %rsi,%rcx
        mov %edi,%eax
        sar %cl,%eax
        ret
        .size u_c_715, .-u_c_715
        .globl u_c_716
        .type u_c_716, @function
u_c_716:
        mov %rsi,%rcx
        mov %edi,%eax
        sar %cl,%eax
        ret
        .size u_c_716, .-u_c_716
        .globl u_c_719
        .type u_c_719, @function
u_c_719:
        mov %esi,%ecx
        mov %edi,%eax
        sar %cl,%eax
        ret
        .size u_c_719, .-u_c_719
        .globl u_c_720
        .type u_c_720, @function
u_c_720:
        mov %esi,%ecx
        mov %rdi,%rax
        sar %cl,%rax
        ret
        .size u_c_720, .-u_c_720
        .globl u_c_721
        .type u_c_721, @function
u_c_721:
        mov %rsi,%rcx
        mov %rdi,%rax
        sar %cl,%rax
        ret
        .size u_c_721, .-u_c_721
        .globl u_c_722
        .type u_c_722, @function
u_c_722:
        mov %rsi,%rcx
        mov %rdi,%rax
        sar %cl,%rax
        ret
        .size u_c_722, .-u_c_722
        .globl u_c_725
        .type u_c_725, @function
u_c_725:
        mov %esi,%ecx
        mov %rdi,%rax
        sar %cl,%rax
        ret
        .size u_c_725, .-u_c_725
        .globl u_c_726
        .type u_c_726, @function
u_c_726:
        mov %esi,%ecx
        mov %rdi,%rax
        shr %cl,%rax
        ret
        .size u_c_726, .-u_c_726
        .globl u_c_727
        .type u_c_727, @function
u_c_727:
        mov %rsi,%rcx
        mov %rdi,%rax
        shr %cl,%rax
        ret
        .size u_c_727, .-u_c_727
        .globl u_c_728
        .type u_c_728, @function
u_c_728:
        mov %rsi,%rcx
        mov %rdi,%rax
        shr %cl,%rax
        ret
        .size u_c_728, .-u_c_728
        .globl u_c_731
        .type u_c_731, @function
u_c_731:
        mov %esi,%ecx
        mov %rdi,%rax
        shr %cl,%rax
        ret
        .size u_c_731, .-u_c_731
        .globl u_c_744
        .type u_c_744, @function
u_c_744:
        mov %esi,%ecx
        mov %edi,%eax
        shr %cl,%eax
        ret
        .size u_c_744, .-u_c_744
        .globl u_c_745
        .type u_c_745, @function
u_c_745:
        mov %rsi,%rcx
        mov %edi,%eax
        shr %cl,%eax
        ret
        .size u_c_745, .-u_c_745
        .globl u_c_746
        .type u_c_746, @function
u_c_746:
        mov %rsi,%rcx
        mov %edi,%eax
        shr %cl,%eax
        ret
        .size u_c_746, .-u_c_746
        .globl u_c_749
        .type u_c_749, @function
u_c_749:
        mov %esi,%ecx
        mov %edi,%eax
        shr %cl,%eax
        ret
        .size u_c_749, .-u_c_749
        .globl u_cpp_0
        .type u_cpp_0, @function
u_cpp_0:
        test %edi,%edi
        sete %al
        ret
        .size u_cpp_0, .-u_cpp_0
        .globl u_cpp_1
        .type u_cpp_1, @function
u_cpp_1:
        test %rdi,%rdi
        sete %al
        ret
        .size u_cpp_1, .-u_cpp_1
        .globl u_cpp_2
        .type u_cpp_2, @function
u_cpp_2:
        test %rdi,%rdi
        sete %al
        ret
        .size u_cpp_2, .-u_cpp_2
        .globl u_cpp_3
        .type u_cpp_3, @function
u_cpp_3:
        xorps %xmm1,%xmm1
        cmpeqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_3, .-u_cpp_3
        .globl u_cpp_4
        .type u_cpp_4, @function
u_cpp_4:
        xorpd %xmm1,%xmm1
        cmpeqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_4, .-u_cpp_4
        .globl u_cpp_5
        .type u_cpp_5, @function
u_cpp_5:
        mov %edi,%eax
        xor $0x1,%al
        ret
        .size u_cpp_5, .-u_cpp_5
        .globl u_cpp_6
        .type u_cpp_6, @function
u_cpp_6:
        mov %edi,%eax
        not %eax
        ret
        .size u_cpp_6, .-u_cpp_6
        .globl u_cpp_7
        .type u_cpp_7, @function
u_cpp_7:
        mov %rdi,%rax
        not %rax
        ret
        .size u_cpp_7, .-u_cpp_7
        .globl u_cpp_8
        .type u_cpp_8, @function
u_cpp_8:
        mov %rdi,%rax
        not %rax
        ret
        .size u_cpp_8, .-u_cpp_8
        .globl u_cpp_11
        .type u_cpp_11, @function
u_cpp_11:
        mov %edi,%eax
        not %eax
        ret
        .size u_cpp_11, .-u_cpp_11
        .globl u_cpp_12
        .type u_cpp_12, @function
u_cpp_12:
        mov %edi,%eax
        neg %eax
        ret
        .size u_cpp_12, .-u_cpp_12
        .globl u_cpp_13
        .type u_cpp_13, @function
u_cpp_13:
        mov %rdi,%rax
        neg %rax
        ret
        .size u_cpp_13, .-u_cpp_13
        .globl u_cpp_14
        .type u_cpp_14, @function
u_cpp_14:
        mov %rdi,%rax
        neg %rax
        ret
        .size u_cpp_14, .-u_cpp_14
        .globl u_cpp_17
        .type u_cpp_17, @function
u_cpp_17:
        mov %edi,%eax
        neg %eax
        ret
        .size u_cpp_17, .-u_cpp_17
        .globl u_cpp_18
        .type u_cpp_18, @function
u_cpp_18:
        mov %edi,%eax
        ret
        .size u_cpp_18, .-u_cpp_18
        .globl u_cpp_19
        .type u_cpp_19, @function
u_cpp_19:
        mov %rdi,%rax
        ret
        .size u_cpp_19, .-u_cpp_19
        .globl u_cpp_20
        .type u_cpp_20, @function
u_cpp_20:
        mov %rdi,%rax
        ret
        .size u_cpp_20, .-u_cpp_20
        .globl u_cpp_21
        .type u_cpp_21, @function
u_cpp_21:
        ret
        .size u_cpp_21, .-u_cpp_21
        .globl u_cpp_22
        .type u_cpp_22, @function
u_cpp_22:
        ret
        .size u_cpp_22, .-u_cpp_22
        .globl u_cpp_23
        .type u_cpp_23, @function
u_cpp_23:
        mov %edi,%eax
        ret
        .size u_cpp_23, .-u_cpp_23
        .globl u_cpp_24
        .type u_cpp_24, @function
u_cpp_24:
        test %edi,%edi
        sete %al
        ret
        .size u_cpp_24, .-u_cpp_24
        .globl u_cpp_25
        .type u_cpp_25, @function
u_cpp_25:
        test %rdi,%rdi
        sete %al
        ret
        .size u_cpp_25, .-u_cpp_25
        .globl u_cpp_26
        .type u_cpp_26, @function
u_cpp_26:
        test %rdi,%rdi
        sete %al
        ret
        .size u_cpp_26, .-u_cpp_26
        .globl u_cpp_27
        .type u_cpp_27, @function
u_cpp_27:
        xorps %xmm1,%xmm1
        cmpeqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_27, .-u_cpp_27
        .globl u_cpp_28
        .type u_cpp_28, @function
u_cpp_28:
        xorpd %xmm1,%xmm1
        cmpeqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_28, .-u_cpp_28
        .globl u_cpp_29
        .type u_cpp_29, @function
u_cpp_29:
        mov %edi,%eax
        xor $0x1,%al
        ret
        .size u_cpp_29, .-u_cpp_29
        .globl u_cpp_30
        .type u_cpp_30, @function
u_cpp_30:
        mov %edi,%eax
        not %eax
        ret
        .size u_cpp_30, .-u_cpp_30
        .globl u_cpp_31
        .type u_cpp_31, @function
u_cpp_31:
        mov %rdi,%rax
        not %rax
        ret
        .size u_cpp_31, .-u_cpp_31
        .globl u_cpp_32
        .type u_cpp_32, @function
u_cpp_32:
        mov %rdi,%rax
        not %rax
        ret
        .size u_cpp_32, .-u_cpp_32
        .globl u_cpp_35
        .type u_cpp_35, @function
u_cpp_35:
        mov %edi,%eax
        not %eax
        ret
        .size u_cpp_35, .-u_cpp_35
        .globl u_cpp_42
        .type u_cpp_42, @function
u_cpp_42:
        mov %edi,-0x4(%rsp)
        lea -0x4(%rsp),%rax
        ret
        .size u_cpp_42, .-u_cpp_42
        .globl u_cpp_43
        .type u_cpp_43, @function
u_cpp_43:
        mov %rdi,-0x8(%rsp)
        lea -0x8(%rsp),%rax
        ret
        .size u_cpp_43, .-u_cpp_43
        .globl u_cpp_44
        .type u_cpp_44, @function
u_cpp_44:
        mov %rdi,-0x8(%rsp)
        lea -0x8(%rsp),%rax
        ret
        .size u_cpp_44, .-u_cpp_44
        .globl u_cpp_45
        .type u_cpp_45, @function
u_cpp_45:
        movss %xmm0,-0x4(%rsp)
        lea -0x4(%rsp),%rax
        ret
        .size u_cpp_45, .-u_cpp_45
        .globl u_cpp_46
        .type u_cpp_46, @function
u_cpp_46:
        movsd %xmm0,-0x8(%rsp)
        lea -0x8(%rsp),%rax
        ret
        .size u_cpp_46, .-u_cpp_46
        .globl u_cpp_47
        .type u_cpp_47, @function
u_cpp_47:
        mov %dil,-0x1(%rsp)
        lea -0x1(%rsp),%rax
        ret
        .size u_cpp_47, .-u_cpp_47
        .globl u_cpp_48
        .type u_cpp_48, @function
u_cpp_48:
        lea 0x1(%rdi),%eax
        ret
        .size u_cpp_48, .-u_cpp_48
        .globl u_cpp_49
        .type u_cpp_49, @function
u_cpp_49:
        lea 0x1(%rdi),%rax
        ret
        .size u_cpp_49, .-u_cpp_49
        .globl u_cpp_50
        .type u_cpp_50, @function
u_cpp_50:
        lea 0x1(%rdi),%rax
        ret
        .size u_cpp_50, .-u_cpp_50
        .globl u_cpp_54
        .type u_cpp_54, @function
u_cpp_54:
        lea -0x1(%rdi),%eax
        ret
        .size u_cpp_54, .-u_cpp_54
        .globl u_cpp_55
        .type u_cpp_55, @function
u_cpp_55:
        lea -0x1(%rdi),%rax
        ret
        .size u_cpp_55, .-u_cpp_55
        .globl u_cpp_56
        .type u_cpp_56, @function
u_cpp_56:
        lea -0x1(%rdi),%rax
        ret
        .size u_cpp_56, .-u_cpp_56
        .globl u_cpp_60
        .type u_cpp_60, @function
u_cpp_60:
        mov $0x4,%eax
        ret
        .size u_cpp_60, .-u_cpp_60
        .globl u_cpp_61
        .type u_cpp_61, @function
u_cpp_61:
        mov $0x8,%eax
        ret
        .size u_cpp_61, .-u_cpp_61
        .globl u_cpp_62
        .type u_cpp_62, @function
u_cpp_62:
        mov $0x8,%eax
        ret
        .size u_cpp_62, .-u_cpp_62
        .globl u_cpp_63
        .type u_cpp_63, @function
u_cpp_63:
        mov $0x4,%eax
        ret
        .size u_cpp_63, .-u_cpp_63
        .globl u_cpp_64
        .type u_cpp_64, @function
u_cpp_64:
        mov $0x8,%eax
        ret
        .size u_cpp_64, .-u_cpp_64
        .globl u_cpp_65
        .type u_cpp_65, @function
u_cpp_65:
        mov $0x1,%eax
        ret
        .size u_cpp_65, .-u_cpp_65
        .globl u_cpp_84
        .type u_cpp_84, @function
u_cpp_84:
        mov %edi,%eax
        ret
        .size u_cpp_84, .-u_cpp_84
        .globl u_cpp_85
        .type u_cpp_85, @function
u_cpp_85:
        mov %rdi,%rax
        ret
        .size u_cpp_85, .-u_cpp_85
        .globl u_cpp_86
        .type u_cpp_86, @function
u_cpp_86:
        mov %rdi,%rax
        ret
        .size u_cpp_86, .-u_cpp_86
        .globl u_cpp_87
        .type u_cpp_87, @function
u_cpp_87:
        ret
        .size u_cpp_87, .-u_cpp_87
        .globl u_cpp_88
        .type u_cpp_88, @function
u_cpp_88:
        ret
        .size u_cpp_88, .-u_cpp_88
        .globl u_cpp_90
        .type u_cpp_90, @function
u_cpp_90:
        mov %edi,%eax
        ret
        .size u_cpp_90, .-u_cpp_90
        .globl u_cpp_91
        .type u_cpp_91, @function
u_cpp_91:
        mov %rdi,%rax
        ret
        .size u_cpp_91, .-u_cpp_91
        .globl u_cpp_92
        .type u_cpp_92, @function
u_cpp_92:
        mov %rdi,%rax
        ret
        .size u_cpp_92, .-u_cpp_92
        .globl u_cpp_93
        .type u_cpp_93, @function
u_cpp_93:
        ret
        .size u_cpp_93, .-u_cpp_93
        .globl u_cpp_94
        .type u_cpp_94, @function
u_cpp_94:
        ret
        .size u_cpp_94, .-u_cpp_94
        .globl u_cpp_102
        .type u_cpp_102, @function
u_cpp_102:
        lea (%rdi,%rsi,1),%eax
        ret
        .size u_cpp_102, .-u_cpp_102
        .globl u_cpp_103
        .type u_cpp_103, @function
u_cpp_103:
        movslq %edi,%rax
        add %rsi,%rax
        ret
        .size u_cpp_103, .-u_cpp_103
        .globl u_cpp_104
        .type u_cpp_104, @function
u_cpp_104:
        movslq %edi,%rax
        add %rsi,%rax
        ret
        .size u_cpp_104, .-u_cpp_104
        .globl u_cpp_105
        .type u_cpp_105, @function
u_cpp_105:
        cvtsi2ss %edi,%xmm1
        addss %xmm1,%xmm0
        ret
        .size u_cpp_105, .-u_cpp_105
        .globl u_cpp_106
        .type u_cpp_106, @function
u_cpp_106:
        cvtsi2sd %edi,%xmm1
        addsd %xmm1,%xmm0
        ret
        .size u_cpp_106, .-u_cpp_106
        .globl u_cpp_107
        .type u_cpp_107, @function
u_cpp_107:
        lea (%rdi,%rsi,1),%eax
        ret
        .size u_cpp_107, .-u_cpp_107
        .globl u_cpp_108
        .type u_cpp_108, @function
u_cpp_108:
        movslq %esi,%rax
        add %rdi,%rax
        ret
        .size u_cpp_108, .-u_cpp_108
        .globl u_cpp_109
        .type u_cpp_109, @function
u_cpp_109:
        lea (%rdi,%rsi,1),%rax
        ret
        .size u_cpp_109, .-u_cpp_109
        .globl u_cpp_110
        .type u_cpp_110, @function
u_cpp_110:
        lea (%rdi,%rsi,1),%rax
        ret
        .size u_cpp_110, .-u_cpp_110
        .globl u_cpp_111
        .type u_cpp_111, @function
u_cpp_111:
        cvtsi2ss %rdi,%xmm1
        addss %xmm1,%xmm0
        ret
        .size u_cpp_111, .-u_cpp_111
        .globl u_cpp_112
        .type u_cpp_112, @function
u_cpp_112:
        cvtsi2sd %rdi,%xmm1
        addsd %xmm1,%xmm0
        ret
        .size u_cpp_112, .-u_cpp_112
        .globl u_cpp_113
        .type u_cpp_113, @function
u_cpp_113:
        mov %esi,%eax
        add %rdi,%rax
        ret
        .size u_cpp_113, .-u_cpp_113
        .globl u_cpp_114
        .type u_cpp_114, @function
u_cpp_114:
        movslq %esi,%rax
        add %rdi,%rax
        ret
        .size u_cpp_114, .-u_cpp_114
        .globl u_cpp_115
        .type u_cpp_115, @function
u_cpp_115:
        lea (%rdi,%rsi,1),%rax
        ret
        .size u_cpp_115, .-u_cpp_115
        .globl u_cpp_116
        .type u_cpp_116, @function
u_cpp_116:
        lea (%rdi,%rsi,1),%rax
        ret
        .size u_cpp_116, .-u_cpp_116
        .globl u_cpp_119
        .type u_cpp_119, @function
u_cpp_119:
        mov %esi,%eax
        add %rdi,%rax
        ret
        .size u_cpp_119, .-u_cpp_119
        .globl u_cpp_120
        .type u_cpp_120, @function
u_cpp_120:
        cvtsi2ss %edi,%xmm1
        addss %xmm1,%xmm0
        ret
        .size u_cpp_120, .-u_cpp_120
        .globl u_cpp_121
        .type u_cpp_121, @function
u_cpp_121:
        cvtsi2ss %rdi,%xmm1
        addss %xmm1,%xmm0
        ret
        .size u_cpp_121, .-u_cpp_121
        .globl u_cpp_123
        .type u_cpp_123, @function
u_cpp_123:
        addss %xmm1,%xmm0
        ret
        .size u_cpp_123, .-u_cpp_123
        .globl u_cpp_124
        .type u_cpp_124, @function
u_cpp_124:
        cvtss2sd %xmm0,%xmm0
        addsd %xmm1,%xmm0
        ret
        .size u_cpp_124, .-u_cpp_124
        .globl u_cpp_125
        .type u_cpp_125, @function
u_cpp_125:
        cvtsi2ss %edi,%xmm1
        addss %xmm1,%xmm0
        ret
        .size u_cpp_125, .-u_cpp_125
        .globl u_cpp_126
        .type u_cpp_126, @function
u_cpp_126:
        cvtsi2sd %edi,%xmm1
        addsd %xmm1,%xmm0
        ret
        .size u_cpp_126, .-u_cpp_126
        .globl u_cpp_127
        .type u_cpp_127, @function
u_cpp_127:
        cvtsi2sd %rdi,%xmm1
        addsd %xmm1,%xmm0
        ret
        .size u_cpp_127, .-u_cpp_127
        .globl u_cpp_129
        .type u_cpp_129, @function
u_cpp_129:
        cvtss2sd %xmm1,%xmm2
        addsd %xmm2,%xmm0
        ret
        .size u_cpp_129, .-u_cpp_129
        .globl u_cpp_130
        .type u_cpp_130, @function
u_cpp_130:
        addsd %xmm1,%xmm0
        ret
        .size u_cpp_130, .-u_cpp_130
        .globl u_cpp_131
        .type u_cpp_131, @function
u_cpp_131:
        cvtsi2sd %edi,%xmm1
        addsd %xmm1,%xmm0
        ret
        .size u_cpp_131, .-u_cpp_131
        .globl u_cpp_132
        .type u_cpp_132, @function
u_cpp_132:
        lea (%rdi,%rsi,1),%eax
        ret
        .size u_cpp_132, .-u_cpp_132
        .globl u_cpp_133
        .type u_cpp_133, @function
u_cpp_133:
        mov %edi,%eax
        add %rsi,%rax
        ret
        .size u_cpp_133, .-u_cpp_133
        .globl u_cpp_134
        .type u_cpp_134, @function
u_cpp_134:
        mov %edi,%eax
        add %rsi,%rax
        ret
        .size u_cpp_134, .-u_cpp_134
        .globl u_cpp_135
        .type u_cpp_135, @function
u_cpp_135:
        cvtsi2ss %edi,%xmm1
        addss %xmm1,%xmm0
        ret
        .size u_cpp_135, .-u_cpp_135
        .globl u_cpp_136
        .type u_cpp_136, @function
u_cpp_136:
        cvtsi2sd %edi,%xmm1
        addsd %xmm1,%xmm0
        ret
        .size u_cpp_136, .-u_cpp_136
        .globl u_cpp_137
        .type u_cpp_137, @function
u_cpp_137:
        lea (%rdi,%rsi,1),%eax
        ret
        .size u_cpp_137, .-u_cpp_137
        .globl u_cpp_138
        .type u_cpp_138, @function
u_cpp_138:
        mov %edi,%eax
        sub %esi,%eax
        ret
        .size u_cpp_138, .-u_cpp_138
        .globl u_cpp_139
        .type u_cpp_139, @function
u_cpp_139:
        movslq %edi,%rax
        sub %rsi,%rax
        ret
        .size u_cpp_139, .-u_cpp_139
        .globl u_cpp_140
        .type u_cpp_140, @function
u_cpp_140:
        movslq %edi,%rax
        sub %rsi,%rax
        ret
        .size u_cpp_140, .-u_cpp_140
        .globl u_cpp_141
        .type u_cpp_141, @function
u_cpp_141:
        cvtsi2ss %edi,%xmm1
        subss %xmm0,%xmm1
        movaps %xmm1,%xmm0
        ret
        .size u_cpp_141, .-u_cpp_141
        .globl u_cpp_142
        .type u_cpp_142, @function
u_cpp_142:
        cvtsi2sd %edi,%xmm1
        subsd %xmm0,%xmm1
        movapd %xmm1,%xmm0
        ret
        .size u_cpp_142, .-u_cpp_142
        .globl u_cpp_143
        .type u_cpp_143, @function
u_cpp_143:
        mov %edi,%eax
        sub %esi,%eax
        ret
        .size u_cpp_143, .-u_cpp_143
        .globl u_cpp_144
        .type u_cpp_144, @function
u_cpp_144:
        mov %rdi,%rax
        movslq %esi,%rcx
        sub %rcx,%rax
        ret
        .size u_cpp_144, .-u_cpp_144
        .globl u_cpp_145
        .type u_cpp_145, @function
u_cpp_145:
        mov %rdi,%rax
        sub %rsi,%rax
        ret
        .size u_cpp_145, .-u_cpp_145
        .globl u_cpp_146
        .type u_cpp_146, @function
u_cpp_146:
        mov %rdi,%rax
        sub %rsi,%rax
        ret
        .size u_cpp_146, .-u_cpp_146
        .globl u_cpp_147
        .type u_cpp_147, @function
u_cpp_147:
        cvtsi2ss %rdi,%xmm1
        subss %xmm0,%xmm1
        movaps %xmm1,%xmm0
        ret
        .size u_cpp_147, .-u_cpp_147
        .globl u_cpp_148
        .type u_cpp_148, @function
u_cpp_148:
        cvtsi2sd %rdi,%xmm1
        subsd %xmm0,%xmm1
        movapd %xmm1,%xmm0
        ret
        .size u_cpp_148, .-u_cpp_148
        .globl u_cpp_149
        .type u_cpp_149, @function
u_cpp_149:
        mov %rdi,%rax
        mov %esi,%ecx
        sub %rcx,%rax
        ret
        .size u_cpp_149, .-u_cpp_149
        .globl u_cpp_150
        .type u_cpp_150, @function
u_cpp_150:
        mov %rdi,%rax
        movslq %esi,%rcx
        sub %rcx,%rax
        ret
        .size u_cpp_150, .-u_cpp_150
        .globl u_cpp_151
        .type u_cpp_151, @function
u_cpp_151:
        mov %rdi,%rax
        sub %rsi,%rax
        ret
        .size u_cpp_151, .-u_cpp_151
        .globl u_cpp_152
        .type u_cpp_152, @function
u_cpp_152:
        mov %rdi,%rax
        sub %rsi,%rax
        ret
        .size u_cpp_152, .-u_cpp_152
        .globl u_cpp_155
        .type u_cpp_155, @function
u_cpp_155:
        mov %rdi,%rax
        mov %esi,%ecx
        sub %rcx,%rax
        ret
        .size u_cpp_155, .-u_cpp_155
        .globl u_cpp_156
        .type u_cpp_156, @function
u_cpp_156:
        cvtsi2ss %edi,%xmm1
        subss %xmm1,%xmm0
        ret
        .size u_cpp_156, .-u_cpp_156
        .globl u_cpp_157
        .type u_cpp_157, @function
u_cpp_157:
        cvtsi2ss %rdi,%xmm1
        subss %xmm1,%xmm0
        ret
        .size u_cpp_157, .-u_cpp_157
        .globl u_cpp_159
        .type u_cpp_159, @function
u_cpp_159:
        subss %xmm1,%xmm0
        ret
        .size u_cpp_159, .-u_cpp_159
        .globl u_cpp_160
        .type u_cpp_160, @function
u_cpp_160:
        cvtss2sd %xmm0,%xmm0
        subsd %xmm1,%xmm0
        ret
        .size u_cpp_160, .-u_cpp_160
        .globl u_cpp_161
        .type u_cpp_161, @function
u_cpp_161:
        cvtsi2ss %edi,%xmm1
        subss %xmm1,%xmm0
        ret
        .size u_cpp_161, .-u_cpp_161
        .globl u_cpp_162
        .type u_cpp_162, @function
u_cpp_162:
        cvtsi2sd %edi,%xmm1
        subsd %xmm1,%xmm0
        ret
        .size u_cpp_162, .-u_cpp_162
        .globl u_cpp_163
        .type u_cpp_163, @function
u_cpp_163:
        cvtsi2sd %rdi,%xmm1
        subsd %xmm1,%xmm0
        ret
        .size u_cpp_163, .-u_cpp_163
        .globl u_cpp_165
        .type u_cpp_165, @function
u_cpp_165:
        cvtss2sd %xmm1,%xmm2
        subsd %xmm2,%xmm0
        ret
        .size u_cpp_165, .-u_cpp_165
        .globl u_cpp_166
        .type u_cpp_166, @function
u_cpp_166:
        subsd %xmm1,%xmm0
        ret
        .size u_cpp_166, .-u_cpp_166
        .globl u_cpp_167
        .type u_cpp_167, @function
u_cpp_167:
        cvtsi2sd %edi,%xmm1
        subsd %xmm1,%xmm0
        ret
        .size u_cpp_167, .-u_cpp_167
        .globl u_cpp_168
        .type u_cpp_168, @function
u_cpp_168:
        mov %edi,%eax
        sub %esi,%eax
        ret
        .size u_cpp_168, .-u_cpp_168
        .globl u_cpp_169
        .type u_cpp_169, @function
u_cpp_169:
        mov %edi,%eax
        sub %rsi,%rax
        ret
        .size u_cpp_169, .-u_cpp_169
        .globl u_cpp_170
        .type u_cpp_170, @function
u_cpp_170:
        mov %edi,%eax
        sub %rsi,%rax
        ret
        .size u_cpp_170, .-u_cpp_170
        .globl u_cpp_171
        .type u_cpp_171, @function
u_cpp_171:
        cvtsi2ss %edi,%xmm1
        subss %xmm0,%xmm1
        movaps %xmm1,%xmm0
        ret
        .size u_cpp_171, .-u_cpp_171
        .globl u_cpp_172
        .type u_cpp_172, @function
u_cpp_172:
        cvtsi2sd %edi,%xmm1
        subsd %xmm0,%xmm1
        movapd %xmm1,%xmm0
        ret
        .size u_cpp_172, .-u_cpp_172
        .globl u_cpp_173
        .type u_cpp_173, @function
u_cpp_173:
        mov %edi,%eax
        sub %esi,%eax
        ret
        .size u_cpp_173, .-u_cpp_173
        .globl u_cpp_174
        .type u_cpp_174, @function
u_cpp_174:
        mov %edi,%eax
        imul %esi,%eax
        ret
        .size u_cpp_174, .-u_cpp_174
        .globl u_cpp_175
        .type u_cpp_175, @function
u_cpp_175:
        movslq %edi,%rax
        imul %rsi,%rax
        ret
        .size u_cpp_175, .-u_cpp_175
        .globl u_cpp_176
        .type u_cpp_176, @function
u_cpp_176:
        movslq %edi,%rax
        imul %rsi,%rax
        ret
        .size u_cpp_176, .-u_cpp_176
        .globl u_cpp_177
        .type u_cpp_177, @function
u_cpp_177:
        cvtsi2ss %edi,%xmm1
        mulss %xmm1,%xmm0
        ret
        .size u_cpp_177, .-u_cpp_177
        .globl u_cpp_178
        .type u_cpp_178, @function
u_cpp_178:
        cvtsi2sd %edi,%xmm1
        mulsd %xmm1,%xmm0
        ret
        .size u_cpp_178, .-u_cpp_178
        .globl u_cpp_179
        .type u_cpp_179, @function
u_cpp_179:
        mov %edi,%eax
        test %esi,%esi
        cmove %esi,%eax
        ret
        .size u_cpp_179, .-u_cpp_179
        .globl u_cpp_180
        .type u_cpp_180, @function
u_cpp_180:
        movslq %esi,%rax
        imul %rdi,%rax
        ret
        .size u_cpp_180, .-u_cpp_180
        .globl u_cpp_181
        .type u_cpp_181, @function
u_cpp_181:
        mov %rdi,%rax
        imul %rsi,%rax
        ret
        .size u_cpp_181, .-u_cpp_181
        .globl u_cpp_182
        .type u_cpp_182, @function
u_cpp_182:
        mov %rdi,%rax
        imul %rsi,%rax
        ret
        .size u_cpp_182, .-u_cpp_182
        .globl u_cpp_183
        .type u_cpp_183, @function
u_cpp_183:
        cvtsi2ss %rdi,%xmm1
        mulss %xmm1,%xmm0
        ret
        .size u_cpp_183, .-u_cpp_183
        .globl u_cpp_184
        .type u_cpp_184, @function
u_cpp_184:
        cvtsi2sd %rdi,%xmm1
        mulsd %xmm1,%xmm0
        ret
        .size u_cpp_184, .-u_cpp_184
        .globl u_cpp_185
        .type u_cpp_185, @function
u_cpp_185:
        xor %eax,%eax
        test %esi,%esi
        cmovne %rdi,%rax
        ret
        .size u_cpp_185, .-u_cpp_185
        .globl u_cpp_186
        .type u_cpp_186, @function
u_cpp_186:
        movslq %esi,%rax
        imul %rdi,%rax
        ret
        .size u_cpp_186, .-u_cpp_186
        .globl u_cpp_187
        .type u_cpp_187, @function
u_cpp_187:
        mov %rdi,%rax
        imul %rsi,%rax
        ret
        .size u_cpp_187, .-u_cpp_187
        .globl u_cpp_188
        .type u_cpp_188, @function
u_cpp_188:
        mov %rdi,%rax
        imul %rsi,%rax
        ret
        .size u_cpp_188, .-u_cpp_188
        .globl u_cpp_191
        .type u_cpp_191, @function
u_cpp_191:
        xor %eax,%eax
        test %esi,%esi
        cmovne %rdi,%rax
        ret
        .size u_cpp_191, .-u_cpp_191
        .globl u_cpp_192
        .type u_cpp_192, @function
u_cpp_192:
        cvtsi2ss %edi,%xmm1
        mulss %xmm1,%xmm0
        ret
        .size u_cpp_192, .-u_cpp_192
        .globl u_cpp_193
        .type u_cpp_193, @function
u_cpp_193:
        cvtsi2ss %rdi,%xmm1
        mulss %xmm1,%xmm0
        ret
        .size u_cpp_193, .-u_cpp_193
        .globl u_cpp_195
        .type u_cpp_195, @function
u_cpp_195:
        mulss %xmm1,%xmm0
        ret
        .size u_cpp_195, .-u_cpp_195
        .globl u_cpp_196
        .type u_cpp_196, @function
u_cpp_196:
        cvtss2sd %xmm0,%xmm0
        mulsd %xmm1,%xmm0
        ret
        .size u_cpp_196, .-u_cpp_196
        .globl u_cpp_197
        .type u_cpp_197, @function
u_cpp_197:
        cvtsi2ss %edi,%xmm1
        mulss %xmm1,%xmm0
        ret
        .size u_cpp_197, .-u_cpp_197
        .globl u_cpp_198
        .type u_cpp_198, @function
u_cpp_198:
        cvtsi2sd %edi,%xmm1
        mulsd %xmm1,%xmm0
        ret
        .size u_cpp_198, .-u_cpp_198
        .globl u_cpp_199
        .type u_cpp_199, @function
u_cpp_199:
        cvtsi2sd %rdi,%xmm1
        mulsd %xmm1,%xmm0
        ret
        .size u_cpp_199, .-u_cpp_199
        .globl u_cpp_201
        .type u_cpp_201, @function
u_cpp_201:
        cvtss2sd %xmm1,%xmm2
        mulsd %xmm2,%xmm0
        ret
        .size u_cpp_201, .-u_cpp_201
        .globl u_cpp_202
        .type u_cpp_202, @function
u_cpp_202:
        mulsd %xmm1,%xmm0
        ret
        .size u_cpp_202, .-u_cpp_202
        .globl u_cpp_203
        .type u_cpp_203, @function
u_cpp_203:
        cvtsi2sd %edi,%xmm1
        mulsd %xmm1,%xmm0
        ret
        .size u_cpp_203, .-u_cpp_203
        .globl u_cpp_204
        .type u_cpp_204, @function
u_cpp_204:
        mov %esi,%eax
        test %edi,%edi
        cmove %edi,%eax
        ret
        .size u_cpp_204, .-u_cpp_204
        .globl u_cpp_205
        .type u_cpp_205, @function
u_cpp_205:
        xor %eax,%eax
        test %edi,%edi
        cmovne %rsi,%rax
        ret
        .size u_cpp_205, .-u_cpp_205
        .globl u_cpp_206
        .type u_cpp_206, @function
u_cpp_206:
        xor %eax,%eax
        test %edi,%edi
        cmovne %rsi,%rax
        ret
        .size u_cpp_206, .-u_cpp_206
        .globl u_cpp_207
        .type u_cpp_207, @function
u_cpp_207:
        cvtsi2ss %edi,%xmm1
        mulss %xmm1,%xmm0
        ret
        .size u_cpp_207, .-u_cpp_207
        .globl u_cpp_208
        .type u_cpp_208, @function
u_cpp_208:
        cvtsi2sd %edi,%xmm1
        mulsd %xmm1,%xmm0
        ret
        .size u_cpp_208, .-u_cpp_208
        .globl u_cpp_209
        .type u_cpp_209, @function
u_cpp_209:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_cpp_209, .-u_cpp_209
        .globl u_cpp_210
        .type u_cpp_210, @function
u_cpp_210:
        mov %edi,%eax
        cltd
        idiv %esi
        ret
        .size u_cpp_210, .-u_cpp_210
        .globl u_cpp_211
        .type u_cpp_211, @function
u_cpp_211:
        movslq %edi,%rax
        cqto
        idiv %rsi
        ret
        .size u_cpp_211, .-u_cpp_211
        .globl u_cpp_212
        .type u_cpp_212, @function
u_cpp_212:
        movslq %edi,%rax
        xor %edx,%edx
        div %rsi
        ret
        .size u_cpp_212, .-u_cpp_212
        .globl u_cpp_213
        .type u_cpp_213, @function
u_cpp_213:
        cvtsi2ss %edi,%xmm1
        divss %xmm0,%xmm1
        movaps %xmm1,%xmm0
        ret
        .size u_cpp_213, .-u_cpp_213
        .globl u_cpp_214
        .type u_cpp_214, @function
u_cpp_214:
        cvtsi2sd %edi,%xmm1
        divsd %xmm0,%xmm1
        movapd %xmm1,%xmm0
        ret
        .size u_cpp_214, .-u_cpp_214
        .globl u_cpp_215
        .type u_cpp_215, @function
u_cpp_215:
        mov %edi,%eax
        ret
        .size u_cpp_215, .-u_cpp_215
        .globl u_cpp_216
        .type u_cpp_216, @function
u_cpp_216:
        mov %rdi,%rax
        movslq %esi,%rcx
        cqto
        idiv %rcx
        ret
        .size u_cpp_216, .-u_cpp_216
        .globl u_cpp_217
        .type u_cpp_217, @function
u_cpp_217:
        mov %rdi,%rax
        cqto
        idiv %rsi
        ret
        .size u_cpp_217, .-u_cpp_217
        .globl u_cpp_218
        .type u_cpp_218, @function
u_cpp_218:
        mov %rdi,%rax
        xor %edx,%edx
        div %rsi
        ret
        .size u_cpp_218, .-u_cpp_218
        .globl u_cpp_219
        .type u_cpp_219, @function
u_cpp_219:
        cvtsi2ss %rdi,%xmm1
        divss %xmm0,%xmm1
        movaps %xmm1,%xmm0
        ret
        .size u_cpp_219, .-u_cpp_219
        .globl u_cpp_220
        .type u_cpp_220, @function
u_cpp_220:
        cvtsi2sd %rdi,%xmm1
        divsd %xmm0,%xmm1
        movapd %xmm1,%xmm0
        ret
        .size u_cpp_220, .-u_cpp_220
        .globl u_cpp_221
        .type u_cpp_221, @function
u_cpp_221:
        mov %rdi,%rax
        ret
        .size u_cpp_221, .-u_cpp_221
        .globl u_cpp_222
        .type u_cpp_222, @function
u_cpp_222:
        mov %rdi,%rax
        movslq %esi,%rcx
        xor %edx,%edx
        div %rcx
        ret
        .size u_cpp_222, .-u_cpp_222
        .globl u_cpp_223
        .type u_cpp_223, @function
u_cpp_223:
        mov %rdi,%rax
        xor %edx,%edx
        div %rsi
        ret
        .size u_cpp_223, .-u_cpp_223
        .globl u_cpp_224
        .type u_cpp_224, @function
u_cpp_224:
        mov %rdi,%rax
        xor %edx,%edx
        div %rsi
        ret
        .size u_cpp_224, .-u_cpp_224
        .globl u_cpp_227
        .type u_cpp_227, @function
u_cpp_227:
        mov %rdi,%rax
        ret
        .size u_cpp_227, .-u_cpp_227
        .globl u_cpp_228
        .type u_cpp_228, @function
u_cpp_228:
        cvtsi2ss %edi,%xmm1
        divss %xmm1,%xmm0
        ret
        .size u_cpp_228, .-u_cpp_228
        .globl u_cpp_229
        .type u_cpp_229, @function
u_cpp_229:
        cvtsi2ss %rdi,%xmm1
        divss %xmm1,%xmm0
        ret
        .size u_cpp_229, .-u_cpp_229
        .globl u_cpp_231
        .type u_cpp_231, @function
u_cpp_231:
        divss %xmm1,%xmm0
        ret
        .size u_cpp_231, .-u_cpp_231
        .globl u_cpp_232
        .type u_cpp_232, @function
u_cpp_232:
        cvtss2sd %xmm0,%xmm0
        divsd %xmm1,%xmm0
        ret
        .size u_cpp_232, .-u_cpp_232
        .globl u_cpp_233
        .type u_cpp_233, @function
u_cpp_233:
        cvtsi2ss %edi,%xmm1
        divss %xmm1,%xmm0
        ret
        .size u_cpp_233, .-u_cpp_233
        .globl u_cpp_234
        .type u_cpp_234, @function
u_cpp_234:
        cvtsi2sd %edi,%xmm1
        divsd %xmm1,%xmm0
        ret
        .size u_cpp_234, .-u_cpp_234
        .globl u_cpp_235
        .type u_cpp_235, @function
u_cpp_235:
        cvtsi2sd %rdi,%xmm1
        divsd %xmm1,%xmm0
        ret
        .size u_cpp_235, .-u_cpp_235
        .globl u_cpp_237
        .type u_cpp_237, @function
u_cpp_237:
        cvtss2sd %xmm1,%xmm2
        divsd %xmm2,%xmm0
        ret
        .size u_cpp_237, .-u_cpp_237
        .globl u_cpp_238
        .type u_cpp_238, @function
u_cpp_238:
        divsd %xmm1,%xmm0
        ret
        .size u_cpp_238, .-u_cpp_238
        .globl u_cpp_239
        .type u_cpp_239, @function
u_cpp_239:
        cvtsi2sd %edi,%xmm1
        divsd %xmm1,%xmm0
        ret
        .size u_cpp_239, .-u_cpp_239
        .globl u_cpp_240
        .type u_cpp_240, @function
u_cpp_240:
        mov %edi,%eax
        xor %edx,%edx
        idiv %esi
        ret
        .size u_cpp_240, .-u_cpp_240
        .globl u_cpp_241
        .type u_cpp_241, @function
u_cpp_241:
        mov %edi,%eax
        xor %edx,%edx
        idiv %rsi
        ret
        .size u_cpp_241, .-u_cpp_241
        .globl u_cpp_242
        .type u_cpp_242, @function
u_cpp_242:
        mov %edi,%eax
        xor %edx,%edx
        div %rsi
        ret
        .size u_cpp_242, .-u_cpp_242
        .globl u_cpp_243
        .type u_cpp_243, @function
u_cpp_243:
        cvtsi2ss %edi,%xmm1
        divss %xmm0,%xmm1
        movaps %xmm1,%xmm0
        ret
        .size u_cpp_243, .-u_cpp_243
        .globl u_cpp_244
        .type u_cpp_244, @function
u_cpp_244:
        cvtsi2sd %edi,%xmm1
        divsd %xmm0,%xmm1
        movapd %xmm1,%xmm0
        ret
        .size u_cpp_244, .-u_cpp_244
        .globl u_cpp_245
        .type u_cpp_245, @function
u_cpp_245:
        mov %edi,%eax
        ret
        .size u_cpp_245, .-u_cpp_245
        .globl u_cpp_246
        .type u_cpp_246, @function
u_cpp_246:
        mov %edi,%eax
        cltd
        idiv %esi
        mov %edx,%eax
        ret
        .size u_cpp_246, .-u_cpp_246
        .globl u_cpp_247
        .type u_cpp_247, @function
u_cpp_247:
        movslq %edi,%rax
        cqto
        idiv %rsi
        mov %rdx,%rax
        ret
        .size u_cpp_247, .-u_cpp_247
        .globl u_cpp_248
        .type u_cpp_248, @function
u_cpp_248:
        movslq %edi,%rax
        xor %edx,%edx
        div %rsi
        mov %rdx,%rax
        ret
        .size u_cpp_248, .-u_cpp_248
        .globl u_cpp_251
        .type u_cpp_251, @function
u_cpp_251:
        xor %eax,%eax
        ret
        .size u_cpp_251, .-u_cpp_251
        .globl u_cpp_252
        .type u_cpp_252, @function
u_cpp_252:
        mov %rdi,%rax
        movslq %esi,%rcx
        cqto
        idiv %rcx
        mov %rdx,%rax
        ret
        .size u_cpp_252, .-u_cpp_252
        .globl u_cpp_253
        .type u_cpp_253, @function
u_cpp_253:
        mov %rdi,%rax
        cqto
        idiv %rsi
        mov %rdx,%rax
        ret
        .size u_cpp_253, .-u_cpp_253
        .globl u_cpp_254
        .type u_cpp_254, @function
u_cpp_254:
        mov %rdi,%rax
        xor %edx,%edx
        div %rsi
        mov %rdx,%rax
        ret
        .size u_cpp_254, .-u_cpp_254
        .globl u_cpp_257
        .type u_cpp_257, @function
u_cpp_257:
        xor %eax,%eax
        ret
        .size u_cpp_257, .-u_cpp_257
        .globl u_cpp_258
        .type u_cpp_258, @function
u_cpp_258:
        mov %rdi,%rax
        movslq %esi,%rcx
        xor %edx,%edx
        div %rcx
        mov %rdx,%rax
        ret
        .size u_cpp_258, .-u_cpp_258
        .globl u_cpp_259
        .type u_cpp_259, @function
u_cpp_259:
        mov %rdi,%rax
        xor %edx,%edx
        div %rsi
        mov %rdx,%rax
        ret
        .size u_cpp_259, .-u_cpp_259
        .globl u_cpp_260
        .type u_cpp_260, @function
u_cpp_260:
        mov %rdi,%rax
        xor %edx,%edx
        div %rsi
        mov %rdx,%rax
        ret
        .size u_cpp_260, .-u_cpp_260
        .globl u_cpp_263
        .type u_cpp_263, @function
u_cpp_263:
        xor %eax,%eax
        ret
        .size u_cpp_263, .-u_cpp_263
        .globl u_cpp_276
        .type u_cpp_276, @function
u_cpp_276:
        mov %edi,%eax
        xor %edx,%edx
        idiv %esi
        mov %edx,%eax
        ret
        .size u_cpp_276, .-u_cpp_276
        .globl u_cpp_277
        .type u_cpp_277, @function
u_cpp_277:
        mov %edi,%eax
        xor %edx,%edx
        idiv %rsi
        mov %rdx,%rax
        ret
        .size u_cpp_277, .-u_cpp_277
        .globl u_cpp_278
        .type u_cpp_278, @function
u_cpp_278:
        mov %edi,%eax
        xor %edx,%edx
        div %rsi
        mov %rdx,%rax
        ret
        .size u_cpp_278, .-u_cpp_278
        .globl u_cpp_281
        .type u_cpp_281, @function
u_cpp_281:
        xor %eax,%eax
        ret
        .size u_cpp_281, .-u_cpp_281
        .globl u_cpp_282
        .type u_cpp_282, @function
u_cpp_282:
        or %esi,%edi
        setne %al
        ret
        .size u_cpp_282, .-u_cpp_282
        .globl u_cpp_283
        .type u_cpp_283, @function
u_cpp_283:
        test %edi,%edi
        setne %cl
        test %rsi,%rsi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_283, .-u_cpp_283
        .globl u_cpp_284
        .type u_cpp_284, @function
u_cpp_284:
        test %edi,%edi
        setne %cl
        test %rsi,%rsi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_284, .-u_cpp_284
        .globl u_cpp_285
        .type u_cpp_285, @function
u_cpp_285:
        test %edi,%edi
        setne %cl
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        or %cl,%al
        ret
        .size u_cpp_285, .-u_cpp_285
        .globl u_cpp_286
        .type u_cpp_286, @function
u_cpp_286:
        test %edi,%edi
        setne %cl
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        or %cl,%al
        ret
        .size u_cpp_286, .-u_cpp_286
        .globl u_cpp_287
        .type u_cpp_287, @function
u_cpp_287:
        test %edi,%edi
        setne %al
        or %sil,%al
        ret
        .size u_cpp_287, .-u_cpp_287
        .globl u_cpp_288
        .type u_cpp_288, @function
u_cpp_288:
        test %rdi,%rdi
        setne %cl
        test %esi,%esi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_288, .-u_cpp_288
        .globl u_cpp_289
        .type u_cpp_289, @function
u_cpp_289:
        or %rsi,%rdi
        setne %al
        ret
        .size u_cpp_289, .-u_cpp_289
        .globl u_cpp_290
        .type u_cpp_290, @function
u_cpp_290:
        or %rsi,%rdi
        setne %al
        ret
        .size u_cpp_290, .-u_cpp_290
        .globl u_cpp_291
        .type u_cpp_291, @function
u_cpp_291:
        test %rdi,%rdi
        setne %cl
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        or %cl,%al
        ret
        .size u_cpp_291, .-u_cpp_291
        .globl u_cpp_292
        .type u_cpp_292, @function
u_cpp_292:
        test %rdi,%rdi
        setne %cl
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        or %cl,%al
        ret
        .size u_cpp_292, .-u_cpp_292
        .globl u_cpp_293
        .type u_cpp_293, @function
u_cpp_293:
        test %rdi,%rdi
        setne %al
        or %sil,%al
        ret
        .size u_cpp_293, .-u_cpp_293
        .globl u_cpp_294
        .type u_cpp_294, @function
u_cpp_294:
        test %rdi,%rdi
        setne %cl
        test %esi,%esi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_294, .-u_cpp_294
        .globl u_cpp_295
        .type u_cpp_295, @function
u_cpp_295:
        or %rsi,%rdi
        setne %al
        ret
        .size u_cpp_295, .-u_cpp_295
        .globl u_cpp_296
        .type u_cpp_296, @function
u_cpp_296:
        or %rsi,%rdi
        setne %al
        ret
        .size u_cpp_296, .-u_cpp_296
        .globl u_cpp_297
        .type u_cpp_297, @function
u_cpp_297:
        test %rdi,%rdi
        setne %cl
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        or %cl,%al
        ret
        .size u_cpp_297, .-u_cpp_297
        .globl u_cpp_298
        .type u_cpp_298, @function
u_cpp_298:
        test %rdi,%rdi
        setne %cl
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        or %cl,%al
        ret
        .size u_cpp_298, .-u_cpp_298
        .globl u_cpp_299
        .type u_cpp_299, @function
u_cpp_299:
        test %rdi,%rdi
        setne %al
        or %sil,%al
        ret
        .size u_cpp_299, .-u_cpp_299
        .globl u_cpp_300
        .type u_cpp_300, @function
u_cpp_300:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %edi,%edi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_300, .-u_cpp_300
        .globl u_cpp_301
        .type u_cpp_301, @function
u_cpp_301:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %rdi,%rdi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_301, .-u_cpp_301
        .globl u_cpp_302
        .type u_cpp_302, @function
u_cpp_302:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %rdi,%rdi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_302, .-u_cpp_302
        .globl u_cpp_303
        .type u_cpp_303, @function
u_cpp_303:
        xorps %xmm2,%xmm2
        cmpneqss %xmm2,%xmm1
        cmpneqss %xmm2,%xmm0
        orps %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%al
        ret
        .size u_cpp_303, .-u_cpp_303
        .globl u_cpp_304
        .type u_cpp_304, @function
u_cpp_304:
        xorps %xmm2,%xmm2
        ucomiss %xmm2,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        xorps %xmm0,%xmm0
        ucomisd %xmm0,%xmm1
        setp %dl
        setne %al
        or %dl,%al
        or %cl,%al
        ret
        .size u_cpp_304, .-u_cpp_304
        .globl u_cpp_305
        .type u_cpp_305, @function
u_cpp_305:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %cl
        setne %al
        or %cl,%al
        or %dil,%al
        ret
        .size u_cpp_305, .-u_cpp_305
        .globl u_cpp_306
        .type u_cpp_306, @function
u_cpp_306:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %edi,%edi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_306, .-u_cpp_306
        .globl u_cpp_307
        .type u_cpp_307, @function
u_cpp_307:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %rdi,%rdi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_307, .-u_cpp_307
        .globl u_cpp_308
        .type u_cpp_308, @function
u_cpp_308:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %rdi,%rdi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_308, .-u_cpp_308
        .globl u_cpp_309
        .type u_cpp_309, @function
u_cpp_309:
        xorpd %xmm2,%xmm2
        ucomisd %xmm2,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        xorpd %xmm0,%xmm0
        ucomiss %xmm0,%xmm1
        setp %dl
        setne %al
        or %dl,%al
        or %cl,%al
        ret
        .size u_cpp_309, .-u_cpp_309
        .globl u_cpp_310
        .type u_cpp_310, @function
u_cpp_310:
        xorpd %xmm2,%xmm2
        cmpneqsd %xmm2,%xmm1
        cmpneqsd %xmm2,%xmm0
        orpd %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%al
        ret
        .size u_cpp_310, .-u_cpp_310
        .globl u_cpp_311
        .type u_cpp_311, @function
u_cpp_311:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %cl
        setne %al
        or %cl,%al
        or %dil,%al
        ret
        .size u_cpp_311, .-u_cpp_311
        .globl u_cpp_312
        .type u_cpp_312, @function
u_cpp_312:
        test %esi,%esi
        setne %al
        or %dil,%al
        ret
        .size u_cpp_312, .-u_cpp_312
        .globl u_cpp_313
        .type u_cpp_313, @function
u_cpp_313:
        test %rsi,%rsi
        setne %al
        or %dil,%al
        ret
        .size u_cpp_313, .-u_cpp_313
        .globl u_cpp_314
        .type u_cpp_314, @function
u_cpp_314:
        test %rsi,%rsi
        setne %al
        or %dil,%al
        ret
        .size u_cpp_314, .-u_cpp_314
        .globl u_cpp_315
        .type u_cpp_315, @function
u_cpp_315:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %cl
        setne %al
        or %cl,%al
        or %dil,%al
        ret
        .size u_cpp_315, .-u_cpp_315
        .globl u_cpp_316
        .type u_cpp_316, @function
u_cpp_316:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %cl
        setne %al
        or %cl,%al
        or %dil,%al
        ret
        .size u_cpp_316, .-u_cpp_316
        .globl u_cpp_317
        .type u_cpp_317, @function
u_cpp_317:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_cpp_317, .-u_cpp_317
        .globl u_cpp_318
        .type u_cpp_318, @function
u_cpp_318:
        test %edi,%edi
        setne %cl
        test %esi,%esi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_318, .-u_cpp_318
        .globl u_cpp_319
        .type u_cpp_319, @function
u_cpp_319:
        test %edi,%edi
        setne %cl
        test %rsi,%rsi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_319, .-u_cpp_319
        .globl u_cpp_320
        .type u_cpp_320, @function
u_cpp_320:
        test %edi,%edi
        setne %cl
        test %rsi,%rsi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_320, .-u_cpp_320
        .globl u_cpp_321
        .type u_cpp_321, @function
u_cpp_321:
        test %edi,%edi
        setne %cl
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        and %cl,%al
        ret
        .size u_cpp_321, .-u_cpp_321
        .globl u_cpp_322
        .type u_cpp_322, @function
u_cpp_322:
        test %edi,%edi
        setne %cl
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        and %cl,%al
        ret
        .size u_cpp_322, .-u_cpp_322
        .globl u_cpp_323
        .type u_cpp_323, @function
u_cpp_323:
        test %edi,%edi
        setne %al
        and %sil,%al
        ret
        .size u_cpp_323, .-u_cpp_323
        .globl u_cpp_324
        .type u_cpp_324, @function
u_cpp_324:
        test %rdi,%rdi
        setne %cl
        test %esi,%esi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_324, .-u_cpp_324
        .globl u_cpp_325
        .type u_cpp_325, @function
u_cpp_325:
        test %rdi,%rdi
        setne %cl
        test %rsi,%rsi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_325, .-u_cpp_325
        .globl u_cpp_326
        .type u_cpp_326, @function
u_cpp_326:
        test %rdi,%rdi
        setne %cl
        test %rsi,%rsi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_326, .-u_cpp_326
        .globl u_cpp_327
        .type u_cpp_327, @function
u_cpp_327:
        test %rdi,%rdi
        setne %cl
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        and %cl,%al
        ret
        .size u_cpp_327, .-u_cpp_327
        .globl u_cpp_328
        .type u_cpp_328, @function
u_cpp_328:
        test %rdi,%rdi
        setne %cl
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        and %cl,%al
        ret
        .size u_cpp_328, .-u_cpp_328
        .globl u_cpp_329
        .type u_cpp_329, @function
u_cpp_329:
        test %rdi,%rdi
        setne %al
        and %sil,%al
        ret
        .size u_cpp_329, .-u_cpp_329
        .globl u_cpp_330
        .type u_cpp_330, @function
u_cpp_330:
        test %rdi,%rdi
        setne %cl
        test %esi,%esi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_330, .-u_cpp_330
        .globl u_cpp_331
        .type u_cpp_331, @function
u_cpp_331:
        test %rdi,%rdi
        setne %cl
        test %rsi,%rsi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_331, .-u_cpp_331
        .globl u_cpp_332
        .type u_cpp_332, @function
u_cpp_332:
        test %rdi,%rdi
        setne %cl
        test %rsi,%rsi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_332, .-u_cpp_332
        .globl u_cpp_333
        .type u_cpp_333, @function
u_cpp_333:
        test %rdi,%rdi
        setne %cl
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        and %cl,%al
        ret
        .size u_cpp_333, .-u_cpp_333
        .globl u_cpp_334
        .type u_cpp_334, @function
u_cpp_334:
        test %rdi,%rdi
        setne %cl
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        and %cl,%al
        ret
        .size u_cpp_334, .-u_cpp_334
        .globl u_cpp_335
        .type u_cpp_335, @function
u_cpp_335:
        test %rdi,%rdi
        setne %al
        and %sil,%al
        ret
        .size u_cpp_335, .-u_cpp_335
        .globl u_cpp_336
        .type u_cpp_336, @function
u_cpp_336:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %edi,%edi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_336, .-u_cpp_336
        .globl u_cpp_337
        .type u_cpp_337, @function
u_cpp_337:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %rdi,%rdi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_337, .-u_cpp_337
        .globl u_cpp_338
        .type u_cpp_338, @function
u_cpp_338:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %rdi,%rdi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_338, .-u_cpp_338
        .globl u_cpp_339
        .type u_cpp_339, @function
u_cpp_339:
        xorps %xmm2,%xmm2
        cmpneqss %xmm2,%xmm1
        cmpneqss %xmm2,%xmm0
        andps %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%al
        ret
        .size u_cpp_339, .-u_cpp_339
        .globl u_cpp_340
        .type u_cpp_340, @function
u_cpp_340:
        xorps %xmm2,%xmm2
        ucomiss %xmm2,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        xorps %xmm0,%xmm0
        ucomisd %xmm0,%xmm1
        setp %dl
        setne %al
        or %dl,%al
        and %cl,%al
        ret
        .size u_cpp_340, .-u_cpp_340
        .globl u_cpp_341
        .type u_cpp_341, @function
u_cpp_341:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %cl
        setne %al
        or %cl,%al
        and %dil,%al
        ret
        .size u_cpp_341, .-u_cpp_341
        .globl u_cpp_342
        .type u_cpp_342, @function
u_cpp_342:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %edi,%edi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_342, .-u_cpp_342
        .globl u_cpp_343
        .type u_cpp_343, @function
u_cpp_343:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %rdi,%rdi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_343, .-u_cpp_343
        .globl u_cpp_344
        .type u_cpp_344, @function
u_cpp_344:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %rdi,%rdi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_344, .-u_cpp_344
        .globl u_cpp_345
        .type u_cpp_345, @function
u_cpp_345:
        xorpd %xmm2,%xmm2
        ucomisd %xmm2,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        xorpd %xmm0,%xmm0
        ucomiss %xmm0,%xmm1
        setp %dl
        setne %al
        or %dl,%al
        and %cl,%al
        ret
        .size u_cpp_345, .-u_cpp_345
        .globl u_cpp_346
        .type u_cpp_346, @function
u_cpp_346:
        xorpd %xmm2,%xmm2
        cmpneqsd %xmm2,%xmm1
        cmpneqsd %xmm2,%xmm0
        andpd %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%al
        ret
        .size u_cpp_346, .-u_cpp_346
        .globl u_cpp_347
        .type u_cpp_347, @function
u_cpp_347:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %cl
        setne %al
        or %cl,%al
        and %dil,%al
        ret
        .size u_cpp_347, .-u_cpp_347
        .globl u_cpp_348
        .type u_cpp_348, @function
u_cpp_348:
        test %esi,%esi
        setne %al
        and %dil,%al
        ret
        .size u_cpp_348, .-u_cpp_348
        .globl u_cpp_349
        .type u_cpp_349, @function
u_cpp_349:
        test %rsi,%rsi
        setne %al
        and %dil,%al
        ret
        .size u_cpp_349, .-u_cpp_349
        .globl u_cpp_350
        .type u_cpp_350, @function
u_cpp_350:
        test %rsi,%rsi
        setne %al
        and %dil,%al
        ret
        .size u_cpp_350, .-u_cpp_350
        .globl u_cpp_351
        .type u_cpp_351, @function
u_cpp_351:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %cl
        setne %al
        or %cl,%al
        and %dil,%al
        ret
        .size u_cpp_351, .-u_cpp_351
        .globl u_cpp_352
        .type u_cpp_352, @function
u_cpp_352:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %cl
        setne %al
        or %cl,%al
        and %dil,%al
        ret
        .size u_cpp_352, .-u_cpp_352
        .globl u_cpp_353
        .type u_cpp_353, @function
u_cpp_353:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_cpp_353, .-u_cpp_353
        .globl u_cpp_354
        .type u_cpp_354, @function
u_cpp_354:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_cpp_354, .-u_cpp_354
        .globl u_cpp_355
        .type u_cpp_355, @function
u_cpp_355:
        movslq %edi,%rax
        or %rsi,%rax
        ret
        .size u_cpp_355, .-u_cpp_355
        .globl u_cpp_356
        .type u_cpp_356, @function
u_cpp_356:
        movslq %edi,%rax
        or %rsi,%rax
        ret
        .size u_cpp_356, .-u_cpp_356
        .globl u_cpp_359
        .type u_cpp_359, @function
u_cpp_359:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_cpp_359, .-u_cpp_359
        .globl u_cpp_360
        .type u_cpp_360, @function
u_cpp_360:
        movslq %esi,%rax
        or %rdi,%rax
        ret
        .size u_cpp_360, .-u_cpp_360
        .globl u_cpp_361
        .type u_cpp_361, @function
u_cpp_361:
        mov %rdi,%rax
        or %rsi,%rax
        ret
        .size u_cpp_361, .-u_cpp_361
        .globl u_cpp_362
        .type u_cpp_362, @function
u_cpp_362:
        mov %rdi,%rax
        or %rsi,%rax
        ret
        .size u_cpp_362, .-u_cpp_362
        .globl u_cpp_365
        .type u_cpp_365, @function
u_cpp_365:
        mov %esi,%eax
        or %rdi,%rax
        ret
        .size u_cpp_365, .-u_cpp_365
        .globl u_cpp_366
        .type u_cpp_366, @function
u_cpp_366:
        movslq %esi,%rax
        or %rdi,%rax
        ret
        .size u_cpp_366, .-u_cpp_366
        .globl u_cpp_367
        .type u_cpp_367, @function
u_cpp_367:
        mov %rdi,%rax
        or %rsi,%rax
        ret
        .size u_cpp_367, .-u_cpp_367
        .globl u_cpp_368
        .type u_cpp_368, @function
u_cpp_368:
        mov %rdi,%rax
        or %rsi,%rax
        ret
        .size u_cpp_368, .-u_cpp_368
        .globl u_cpp_371
        .type u_cpp_371, @function
u_cpp_371:
        mov %esi,%eax
        or %rdi,%rax
        ret
        .size u_cpp_371, .-u_cpp_371
        .globl u_cpp_384
        .type u_cpp_384, @function
u_cpp_384:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_cpp_384, .-u_cpp_384
        .globl u_cpp_385
        .type u_cpp_385, @function
u_cpp_385:
        mov %edi,%eax
        or %rsi,%rax
        ret
        .size u_cpp_385, .-u_cpp_385
        .globl u_cpp_386
        .type u_cpp_386, @function
u_cpp_386:
        mov %edi,%eax
        or %rsi,%rax
        ret
        .size u_cpp_386, .-u_cpp_386
        .globl u_cpp_389
        .type u_cpp_389, @function
u_cpp_389:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_cpp_389, .-u_cpp_389
        .globl u_cpp_390
        .type u_cpp_390, @function
u_cpp_390:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_cpp_390, .-u_cpp_390
        .globl u_cpp_391
        .type u_cpp_391, @function
u_cpp_391:
        movslq %edi,%rax
        xor %rsi,%rax
        ret
        .size u_cpp_391, .-u_cpp_391
        .globl u_cpp_392
        .type u_cpp_392, @function
u_cpp_392:
        movslq %edi,%rax
        xor %rsi,%rax
        ret
        .size u_cpp_392, .-u_cpp_392
        .globl u_cpp_395
        .type u_cpp_395, @function
u_cpp_395:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_cpp_395, .-u_cpp_395
        .globl u_cpp_396
        .type u_cpp_396, @function
u_cpp_396:
        movslq %esi,%rax
        xor %rdi,%rax
        ret
        .size u_cpp_396, .-u_cpp_396
        .globl u_cpp_397
        .type u_cpp_397, @function
u_cpp_397:
        mov %rdi,%rax
        xor %rsi,%rax
        ret
        .size u_cpp_397, .-u_cpp_397
        .globl u_cpp_398
        .type u_cpp_398, @function
u_cpp_398:
        mov %rdi,%rax
        xor %rsi,%rax
        ret
        .size u_cpp_398, .-u_cpp_398
        .globl u_cpp_401
        .type u_cpp_401, @function
u_cpp_401:
        mov %esi,%eax
        xor %rdi,%rax
        ret
        .size u_cpp_401, .-u_cpp_401
        .globl u_cpp_402
        .type u_cpp_402, @function
u_cpp_402:
        movslq %esi,%rax
        xor %rdi,%rax
        ret
        .size u_cpp_402, .-u_cpp_402
        .globl u_cpp_403
        .type u_cpp_403, @function
u_cpp_403:
        mov %rdi,%rax
        xor %rsi,%rax
        ret
        .size u_cpp_403, .-u_cpp_403
        .globl u_cpp_404
        .type u_cpp_404, @function
u_cpp_404:
        mov %rdi,%rax
        xor %rsi,%rax
        ret
        .size u_cpp_404, .-u_cpp_404
        .globl u_cpp_407
        .type u_cpp_407, @function
u_cpp_407:
        mov %esi,%eax
        xor %rdi,%rax
        ret
        .size u_cpp_407, .-u_cpp_407
        .globl u_cpp_420
        .type u_cpp_420, @function
u_cpp_420:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_cpp_420, .-u_cpp_420
        .globl u_cpp_421
        .type u_cpp_421, @function
u_cpp_421:
        mov %edi,%eax
        xor %rsi,%rax
        ret
        .size u_cpp_421, .-u_cpp_421
        .globl u_cpp_422
        .type u_cpp_422, @function
u_cpp_422:
        mov %edi,%eax
        xor %rsi,%rax
        ret
        .size u_cpp_422, .-u_cpp_422
        .globl u_cpp_425
        .type u_cpp_425, @function
u_cpp_425:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_cpp_425, .-u_cpp_425
        .globl u_cpp_426
        .type u_cpp_426, @function
u_cpp_426:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_cpp_426, .-u_cpp_426
        .globl u_cpp_427
        .type u_cpp_427, @function
u_cpp_427:
        movslq %edi,%rax
        and %rsi,%rax
        ret
        .size u_cpp_427, .-u_cpp_427
        .globl u_cpp_428
        .type u_cpp_428, @function
u_cpp_428:
        movslq %edi,%rax
        and %rsi,%rax
        ret
        .size u_cpp_428, .-u_cpp_428
        .globl u_cpp_431
        .type u_cpp_431, @function
u_cpp_431:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_cpp_431, .-u_cpp_431
        .globl u_cpp_432
        .type u_cpp_432, @function
u_cpp_432:
        movslq %esi,%rax
        and %rdi,%rax
        ret
        .size u_cpp_432, .-u_cpp_432
        .globl u_cpp_433
        .type u_cpp_433, @function
u_cpp_433:
        mov %rdi,%rax
        and %rsi,%rax
        ret
        .size u_cpp_433, .-u_cpp_433
        .globl u_cpp_434
        .type u_cpp_434, @function
u_cpp_434:
        mov %rdi,%rax
        and %rsi,%rax
        ret
        .size u_cpp_434, .-u_cpp_434
        .globl u_cpp_437
        .type u_cpp_437, @function
u_cpp_437:
        mov %rdi,%rax
        and %esi,%eax
        ret
        .size u_cpp_437, .-u_cpp_437
        .globl u_cpp_438
        .type u_cpp_438, @function
u_cpp_438:
        movslq %esi,%rax
        and %rdi,%rax
        ret
        .size u_cpp_438, .-u_cpp_438
        .globl u_cpp_439
        .type u_cpp_439, @function
u_cpp_439:
        mov %rdi,%rax
        and %rsi,%rax
        ret
        .size u_cpp_439, .-u_cpp_439
        .globl u_cpp_440
        .type u_cpp_440, @function
u_cpp_440:
        mov %rdi,%rax
        and %rsi,%rax
        ret
        .size u_cpp_440, .-u_cpp_440
        .globl u_cpp_443
        .type u_cpp_443, @function
u_cpp_443:
        mov %rdi,%rax
        and %esi,%eax
        ret
        .size u_cpp_443, .-u_cpp_443
        .globl u_cpp_456
        .type u_cpp_456, @function
u_cpp_456:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_cpp_456, .-u_cpp_456
        .globl u_cpp_457
        .type u_cpp_457, @function
u_cpp_457:
        mov %rsi,%rax
        and %edi,%eax
        ret
        .size u_cpp_457, .-u_cpp_457
        .globl u_cpp_458
        .type u_cpp_458, @function
u_cpp_458:
        mov %rsi,%rax
        and %edi,%eax
        ret
        .size u_cpp_458, .-u_cpp_458
        .globl u_cpp_461
        .type u_cpp_461, @function
u_cpp_461:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_cpp_461, .-u_cpp_461
        .globl u_cpp_462
        .type u_cpp_462, @function
u_cpp_462:
        cmp %esi,%edi
        sete %al
        ret
        .size u_cpp_462, .-u_cpp_462
        .globl u_cpp_463
        .type u_cpp_463, @function
u_cpp_463:
        movslq %edi,%rax
        cmp %rax,%rsi
        sete %al
        ret
        .size u_cpp_463, .-u_cpp_463
        .globl u_cpp_464
        .type u_cpp_464, @function
u_cpp_464:
        movslq %edi,%rax
        cmp %rax,%rsi
        sete %al
        ret
        .size u_cpp_464, .-u_cpp_464
        .globl u_cpp_465
        .type u_cpp_465, @function
u_cpp_465:
        cvtsi2ss %edi,%xmm1
        cmpeqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_465, .-u_cpp_465
        .globl u_cpp_466
        .type u_cpp_466, @function
u_cpp_466:
        cvtsi2sd %edi,%xmm1
        cmpeqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_466, .-u_cpp_466
        .globl u_cpp_467
        .type u_cpp_467, @function
u_cpp_467:
        cmp %esi,%edi
        sete %al
        ret
        .size u_cpp_467, .-u_cpp_467
        .globl u_cpp_468
        .type u_cpp_468, @function
u_cpp_468:
        movslq %esi,%rax
        cmp %rax,%rdi
        sete %al
        ret
        .size u_cpp_468, .-u_cpp_468
        .globl u_cpp_469
        .type u_cpp_469, @function
u_cpp_469:
        cmp %rsi,%rdi
        sete %al
        ret
        .size u_cpp_469, .-u_cpp_469
        .globl u_cpp_470
        .type u_cpp_470, @function
u_cpp_470:
        cmp %rsi,%rdi
        sete %al
        ret
        .size u_cpp_470, .-u_cpp_470
        .globl u_cpp_471
        .type u_cpp_471, @function
u_cpp_471:
        cvtsi2ss %rdi,%xmm1
        cmpeqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_471, .-u_cpp_471
        .globl u_cpp_472
        .type u_cpp_472, @function
u_cpp_472:
        cvtsi2sd %rdi,%xmm1
        cmpeqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_472, .-u_cpp_472
        .globl u_cpp_473
        .type u_cpp_473, @function
u_cpp_473:
        mov %esi,%eax
        cmp %rax,%rdi
        sete %al
        ret
        .size u_cpp_473, .-u_cpp_473
        .globl u_cpp_474
        .type u_cpp_474, @function
u_cpp_474:
        movslq %esi,%rax
        cmp %rax,%rdi
        sete %al
        ret
        .size u_cpp_474, .-u_cpp_474
        .globl u_cpp_475
        .type u_cpp_475, @function
u_cpp_475:
        cmp %rsi,%rdi
        sete %al
        ret
        .size u_cpp_475, .-u_cpp_475
        .globl u_cpp_476
        .type u_cpp_476, @function
u_cpp_476:
        cmp %rsi,%rdi
        sete %al
        ret
        .size u_cpp_476, .-u_cpp_476
        .globl u_cpp_479
        .type u_cpp_479, @function
u_cpp_479:
        mov %esi,%eax
        cmp %rax,%rdi
        sete %al
        ret
        .size u_cpp_479, .-u_cpp_479
        .globl u_cpp_480
        .type u_cpp_480, @function
u_cpp_480:
        cvtsi2ss %edi,%xmm1
        cmpeqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_480, .-u_cpp_480
        .globl u_cpp_481
        .type u_cpp_481, @function
u_cpp_481:
        cvtsi2ss %rdi,%xmm1
        cmpeqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_481, .-u_cpp_481
        .globl u_cpp_483
        .type u_cpp_483, @function
u_cpp_483:
        cmpeqss %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%eax
        ret
        .size u_cpp_483, .-u_cpp_483
        .globl u_cpp_484
        .type u_cpp_484, @function
u_cpp_484:
        cvtss2sd %xmm0,%xmm2
        cmpeqsd %xmm1,%xmm2
        movq %xmm2,%rax
        and $0x1,%eax
        ret
        .size u_cpp_484, .-u_cpp_484
        .globl u_cpp_485
        .type u_cpp_485, @function
u_cpp_485:
        cvtsi2ss %edi,%xmm1
        cmpeqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_485, .-u_cpp_485
        .globl u_cpp_486
        .type u_cpp_486, @function
u_cpp_486:
        cvtsi2sd %edi,%xmm1
        cmpeqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_486, .-u_cpp_486
        .globl u_cpp_487
        .type u_cpp_487, @function
u_cpp_487:
        cvtsi2sd %rdi,%xmm1
        cmpeqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_487, .-u_cpp_487
        .globl u_cpp_489
        .type u_cpp_489, @function
u_cpp_489:
        cvtss2sd %xmm1,%xmm2
        cmpeqsd %xmm0,%xmm2
        movq %xmm2,%rax
        and $0x1,%eax
        ret
        .size u_cpp_489, .-u_cpp_489
        .globl u_cpp_490
        .type u_cpp_490, @function
u_cpp_490:
        cmpeqsd %xmm1,%xmm0
        movq %xmm0,%rax
        and $0x1,%eax
        ret
        .size u_cpp_490, .-u_cpp_490
        .globl u_cpp_491
        .type u_cpp_491, @function
u_cpp_491:
        cvtsi2sd %edi,%xmm1
        cmpeqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_491, .-u_cpp_491
        .globl u_cpp_492
        .type u_cpp_492, @function
u_cpp_492:
        cmp %edi,%esi
        sete %al
        ret
        .size u_cpp_492, .-u_cpp_492
        .globl u_cpp_493
        .type u_cpp_493, @function
u_cpp_493:
        mov %edi,%eax
        cmp %rax,%rsi
        sete %al
        ret
        .size u_cpp_493, .-u_cpp_493
        .globl u_cpp_494
        .type u_cpp_494, @function
u_cpp_494:
        mov %edi,%eax
        cmp %rax,%rsi
        sete %al
        ret
        .size u_cpp_494, .-u_cpp_494
        .globl u_cpp_495
        .type u_cpp_495, @function
u_cpp_495:
        cvtsi2ss %edi,%xmm1
        cmpeqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_495, .-u_cpp_495
        .globl u_cpp_496
        .type u_cpp_496, @function
u_cpp_496:
        cvtsi2sd %edi,%xmm1
        cmpeqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_496, .-u_cpp_496
        .globl u_cpp_497
        .type u_cpp_497, @function
u_cpp_497:
        mov %edi,%eax
        xor %esi,%eax
        xor $0x1,%al
        ret
        .size u_cpp_497, .-u_cpp_497
        .globl u_cpp_498
        .type u_cpp_498, @function
u_cpp_498:
        cmp %esi,%edi
        setne %al
        ret
        .size u_cpp_498, .-u_cpp_498
        .globl u_cpp_499
        .type u_cpp_499, @function
u_cpp_499:
        movslq %edi,%rax
        cmp %rax,%rsi
        setne %al
        ret
        .size u_cpp_499, .-u_cpp_499
        .globl u_cpp_500
        .type u_cpp_500, @function
u_cpp_500:
        movslq %edi,%rax
        cmp %rax,%rsi
        setne %al
        ret
        .size u_cpp_500, .-u_cpp_500
        .globl u_cpp_501
        .type u_cpp_501, @function
u_cpp_501:
        cvtsi2ss %edi,%xmm1
        cmpneqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_501, .-u_cpp_501
        .globl u_cpp_502
        .type u_cpp_502, @function
u_cpp_502:
        cvtsi2sd %edi,%xmm1
        cmpneqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_502, .-u_cpp_502
        .globl u_cpp_503
        .type u_cpp_503, @function
u_cpp_503:
        cmp %esi,%edi
        setne %al
        ret
        .size u_cpp_503, .-u_cpp_503
        .globl u_cpp_504
        .type u_cpp_504, @function
u_cpp_504:
        movslq %esi,%rax
        cmp %rax,%rdi
        setne %al
        ret
        .size u_cpp_504, .-u_cpp_504
        .globl u_cpp_505
        .type u_cpp_505, @function
u_cpp_505:
        cmp %rsi,%rdi
        setne %al
        ret
        .size u_cpp_505, .-u_cpp_505
        .globl u_cpp_506
        .type u_cpp_506, @function
u_cpp_506:
        cmp %rsi,%rdi
        setne %al
        ret
        .size u_cpp_506, .-u_cpp_506
        .globl u_cpp_507
        .type u_cpp_507, @function
u_cpp_507:
        cvtsi2ss %rdi,%xmm1
        cmpneqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_507, .-u_cpp_507
        .globl u_cpp_508
        .type u_cpp_508, @function
u_cpp_508:
        cvtsi2sd %rdi,%xmm1
        cmpneqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_508, .-u_cpp_508
        .globl u_cpp_509
        .type u_cpp_509, @function
u_cpp_509:
        mov %esi,%eax
        cmp %rax,%rdi
        setne %al
        ret
        .size u_cpp_509, .-u_cpp_509
        .globl u_cpp_510
        .type u_cpp_510, @function
u_cpp_510:
        movslq %esi,%rax
        cmp %rax,%rdi
        setne %al
        ret
        .size u_cpp_510, .-u_cpp_510
        .globl u_cpp_511
        .type u_cpp_511, @function
u_cpp_511:
        cmp %rsi,%rdi
        setne %al
        ret
        .size u_cpp_511, .-u_cpp_511
        .globl u_cpp_512
        .type u_cpp_512, @function
u_cpp_512:
        cmp %rsi,%rdi
        setne %al
        ret
        .size u_cpp_512, .-u_cpp_512
        .globl u_cpp_515
        .type u_cpp_515, @function
u_cpp_515:
        mov %esi,%eax
        cmp %rax,%rdi
        setne %al
        ret
        .size u_cpp_515, .-u_cpp_515
        .globl u_cpp_516
        .type u_cpp_516, @function
u_cpp_516:
        cvtsi2ss %edi,%xmm1
        cmpneqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_516, .-u_cpp_516
        .globl u_cpp_517
        .type u_cpp_517, @function
u_cpp_517:
        cvtsi2ss %rdi,%xmm1
        cmpneqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_517, .-u_cpp_517
        .globl u_cpp_519
        .type u_cpp_519, @function
u_cpp_519:
        cmpneqss %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%eax
        ret
        .size u_cpp_519, .-u_cpp_519
        .globl u_cpp_520
        .type u_cpp_520, @function
u_cpp_520:
        cvtss2sd %xmm0,%xmm2
        cmpneqsd %xmm1,%xmm2
        movq %xmm2,%rax
        and $0x1,%eax
        ret
        .size u_cpp_520, .-u_cpp_520
        .globl u_cpp_521
        .type u_cpp_521, @function
u_cpp_521:
        cvtsi2ss %edi,%xmm1
        cmpneqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_521, .-u_cpp_521
        .globl u_cpp_522
        .type u_cpp_522, @function
u_cpp_522:
        cvtsi2sd %edi,%xmm1
        cmpneqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_522, .-u_cpp_522
        .globl u_cpp_523
        .type u_cpp_523, @function
u_cpp_523:
        cvtsi2sd %rdi,%xmm1
        cmpneqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_523, .-u_cpp_523
        .globl u_cpp_525
        .type u_cpp_525, @function
u_cpp_525:
        cvtss2sd %xmm1,%xmm2
        cmpneqsd %xmm0,%xmm2
        movq %xmm2,%rax
        and $0x1,%eax
        ret
        .size u_cpp_525, .-u_cpp_525
        .globl u_cpp_526
        .type u_cpp_526, @function
u_cpp_526:
        cmpneqsd %xmm1,%xmm0
        movq %xmm0,%rax
        and $0x1,%eax
        ret
        .size u_cpp_526, .-u_cpp_526
        .globl u_cpp_527
        .type u_cpp_527, @function
u_cpp_527:
        cvtsi2sd %edi,%xmm1
        cmpneqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_527, .-u_cpp_527
        .globl u_cpp_528
        .type u_cpp_528, @function
u_cpp_528:
        cmp %edi,%esi
        setne %al
        ret
        .size u_cpp_528, .-u_cpp_528
        .globl u_cpp_529
        .type u_cpp_529, @function
u_cpp_529:
        mov %edi,%eax
        cmp %rax,%rsi
        setne %al
        ret
        .size u_cpp_529, .-u_cpp_529
        .globl u_cpp_530
        .type u_cpp_530, @function
u_cpp_530:
        mov %edi,%eax
        cmp %rax,%rsi
        setne %al
        ret
        .size u_cpp_530, .-u_cpp_530
        .globl u_cpp_531
        .type u_cpp_531, @function
u_cpp_531:
        cvtsi2ss %edi,%xmm1
        cmpneqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_531, .-u_cpp_531
        .globl u_cpp_532
        .type u_cpp_532, @function
u_cpp_532:
        cvtsi2sd %edi,%xmm1
        cmpneqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_532, .-u_cpp_532
        .globl u_cpp_533
        .type u_cpp_533, @function
u_cpp_533:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_cpp_533, .-u_cpp_533
        .globl u_cpp_534
        .type u_cpp_534, @function
u_cpp_534:
        cmp %esi,%edi
        setg %al
        ret
        .size u_cpp_534, .-u_cpp_534
        .globl u_cpp_535
        .type u_cpp_535, @function
u_cpp_535:
        movslq %edi,%rax
        cmp %rax,%rsi
        setl %al
        ret
        .size u_cpp_535, .-u_cpp_535
        .globl u_cpp_536
        .type u_cpp_536, @function
u_cpp_536:
        movslq %edi,%rax
        cmp %rax,%rsi
        setb %al
        ret
        .size u_cpp_536, .-u_cpp_536
        .globl u_cpp_537
        .type u_cpp_537, @function
u_cpp_537:
        cvtsi2ss %edi,%xmm1
        ucomiss %xmm0,%xmm1
        seta %al
        ret
        .size u_cpp_537, .-u_cpp_537
        .globl u_cpp_538
        .type u_cpp_538, @function
u_cpp_538:
        cvtsi2sd %edi,%xmm1
        ucomisd %xmm0,%xmm1
        seta %al
        ret
        .size u_cpp_538, .-u_cpp_538
        .globl u_cpp_539
        .type u_cpp_539, @function
u_cpp_539:
        cmp %esi,%edi
        setg %al
        ret
        .size u_cpp_539, .-u_cpp_539
        .globl u_cpp_540
        .type u_cpp_540, @function
u_cpp_540:
        movslq %esi,%rax
        cmp %rax,%rdi
        setg %al
        ret
        .size u_cpp_540, .-u_cpp_540
        .globl u_cpp_541
        .type u_cpp_541, @function
u_cpp_541:
        cmp %rsi,%rdi
        setg %al
        ret
        .size u_cpp_541, .-u_cpp_541
        .globl u_cpp_542
        .type u_cpp_542, @function
u_cpp_542:
        cmp %rsi,%rdi
        seta %al
        ret
        .size u_cpp_542, .-u_cpp_542
        .globl u_cpp_543
        .type u_cpp_543, @function
u_cpp_543:
        cvtsi2ss %rdi,%xmm1
        ucomiss %xmm0,%xmm1
        seta %al
        ret
        .size u_cpp_543, .-u_cpp_543
        .globl u_cpp_544
        .type u_cpp_544, @function
u_cpp_544:
        cvtsi2sd %rdi,%xmm1
        ucomisd %xmm0,%xmm1
        seta %al
        ret
        .size u_cpp_544, .-u_cpp_544
        .globl u_cpp_545
        .type u_cpp_545, @function
u_cpp_545:
        mov %esi,%eax
        cmp %rax,%rdi
        setg %al
        ret
        .size u_cpp_545, .-u_cpp_545
        .globl u_cpp_546
        .type u_cpp_546, @function
u_cpp_546:
        movslq %esi,%rax
        cmp %rax,%rdi
        seta %al
        ret
        .size u_cpp_546, .-u_cpp_546
        .globl u_cpp_547
        .type u_cpp_547, @function
u_cpp_547:
        cmp %rsi,%rdi
        seta %al
        ret
        .size u_cpp_547, .-u_cpp_547
        .globl u_cpp_548
        .type u_cpp_548, @function
u_cpp_548:
        cmp %rsi,%rdi
        seta %al
        ret
        .size u_cpp_548, .-u_cpp_548
        .globl u_cpp_551
        .type u_cpp_551, @function
u_cpp_551:
        mov %esi,%eax
        cmp %rax,%rdi
        seta %al
        ret
        .size u_cpp_551, .-u_cpp_551
        .globl u_cpp_552
        .type u_cpp_552, @function
u_cpp_552:
        cvtsi2ss %edi,%xmm1
        ucomiss %xmm1,%xmm0
        seta %al
        ret
        .size u_cpp_552, .-u_cpp_552
        .globl u_cpp_553
        .type u_cpp_553, @function
u_cpp_553:
        cvtsi2ss %rdi,%xmm1
        ucomiss %xmm1,%xmm0
        seta %al
        ret
        .size u_cpp_553, .-u_cpp_553
        .globl u_cpp_555
        .type u_cpp_555, @function
u_cpp_555:
        ucomiss %xmm1,%xmm0
        seta %al
        ret
        .size u_cpp_555, .-u_cpp_555
        .globl u_cpp_556
        .type u_cpp_556, @function
u_cpp_556:
        cvtss2sd %xmm0,%xmm2
        ucomisd %xmm1,%xmm2
        seta %al
        ret
        .size u_cpp_556, .-u_cpp_556
        .globl u_cpp_557
        .type u_cpp_557, @function
u_cpp_557:
        cvtsi2ss %edi,%xmm1
        ucomiss %xmm1,%xmm0
        seta %al
        ret
        .size u_cpp_557, .-u_cpp_557
        .globl u_cpp_558
        .type u_cpp_558, @function
u_cpp_558:
        cvtsi2sd %edi,%xmm1
        ucomisd %xmm1,%xmm0
        seta %al
        ret
        .size u_cpp_558, .-u_cpp_558
        .globl u_cpp_559
        .type u_cpp_559, @function
u_cpp_559:
        cvtsi2sd %rdi,%xmm1
        ucomisd %xmm1,%xmm0
        seta %al
        ret
        .size u_cpp_559, .-u_cpp_559
        .globl u_cpp_561
        .type u_cpp_561, @function
u_cpp_561:
        cvtss2sd %xmm1,%xmm2
        ucomisd %xmm2,%xmm0
        seta %al
        ret
        .size u_cpp_561, .-u_cpp_561
        .globl u_cpp_562
        .type u_cpp_562, @function
u_cpp_562:
        ucomisd %xmm1,%xmm0
        seta %al
        ret
        .size u_cpp_562, .-u_cpp_562
        .globl u_cpp_563
        .type u_cpp_563, @function
u_cpp_563:
        cvtsi2sd %edi,%xmm1
        ucomisd %xmm1,%xmm0
        seta %al
        ret
        .size u_cpp_563, .-u_cpp_563
        .globl u_cpp_564
        .type u_cpp_564, @function
u_cpp_564:
        cmp %edi,%esi
        setl %al
        ret
        .size u_cpp_564, .-u_cpp_564
        .globl u_cpp_565
        .type u_cpp_565, @function
u_cpp_565:
        mov %edi,%eax
        cmp %rax,%rsi
        setl %al
        ret
        .size u_cpp_565, .-u_cpp_565
        .globl u_cpp_566
        .type u_cpp_566, @function
u_cpp_566:
        test %rsi,%rsi
        sete %al
        and %dil,%al
        ret
        .size u_cpp_566, .-u_cpp_566
        .globl u_cpp_567
        .type u_cpp_567, @function
u_cpp_567:
        cvtsi2ss %edi,%xmm1
        ucomiss %xmm0,%xmm1
        seta %al
        ret
        .size u_cpp_567, .-u_cpp_567
        .globl u_cpp_568
        .type u_cpp_568, @function
u_cpp_568:
        cvtsi2sd %edi,%xmm1
        ucomisd %xmm0,%xmm1
        seta %al
        ret
        .size u_cpp_568, .-u_cpp_568
        .globl u_cpp_569
        .type u_cpp_569, @function
u_cpp_569:
        mov %esi,%eax
        xor $0x1,%al
        and %dil,%al
        ret
        .size u_cpp_569, .-u_cpp_569
        .globl u_cpp_570
        .type u_cpp_570, @function
u_cpp_570:
        cmp %esi,%edi
        setge %al
        ret
        .size u_cpp_570, .-u_cpp_570
        .globl u_cpp_571
        .type u_cpp_571, @function
u_cpp_571:
        movslq %edi,%rax
        cmp %rax,%rsi
        setle %al
        ret
        .size u_cpp_571, .-u_cpp_571
        .globl u_cpp_572
        .type u_cpp_572, @function
u_cpp_572:
        movslq %edi,%rax
        cmp %rax,%rsi
        setbe %al
        ret
        .size u_cpp_572, .-u_cpp_572
        .globl u_cpp_573
        .type u_cpp_573, @function
u_cpp_573:
        cvtsi2ss %edi,%xmm1
        ucomiss %xmm0,%xmm1
        setae %al
        ret
        .size u_cpp_573, .-u_cpp_573
        .globl u_cpp_574
        .type u_cpp_574, @function
u_cpp_574:
        cvtsi2sd %edi,%xmm1
        ucomisd %xmm0,%xmm1
        setae %al
        ret
        .size u_cpp_574, .-u_cpp_574
        .globl u_cpp_575
        .type u_cpp_575, @function
u_cpp_575:
        cmp %esi,%edi
        setge %al
        ret
        .size u_cpp_575, .-u_cpp_575
        .globl u_cpp_576
        .type u_cpp_576, @function
u_cpp_576:
        movslq %esi,%rax
        cmp %rax,%rdi
        setge %al
        ret
        .size u_cpp_576, .-u_cpp_576
        .globl u_cpp_577
        .type u_cpp_577, @function
u_cpp_577:
        cmp %rsi,%rdi
        setge %al
        ret
        .size u_cpp_577, .-u_cpp_577
        .globl u_cpp_578
        .type u_cpp_578, @function
u_cpp_578:
        cmp %rsi,%rdi
        setae %al
        ret
        .size u_cpp_578, .-u_cpp_578
        .globl u_cpp_579
        .type u_cpp_579, @function
u_cpp_579:
        cvtsi2ss %rdi,%xmm1
        ucomiss %xmm0,%xmm1
        setae %al
        ret
        .size u_cpp_579, .-u_cpp_579
        .globl u_cpp_580
        .type u_cpp_580, @function
u_cpp_580:
        cvtsi2sd %rdi,%xmm1
        ucomisd %xmm0,%xmm1
        setae %al
        ret
        .size u_cpp_580, .-u_cpp_580
        .globl u_cpp_581
        .type u_cpp_581, @function
u_cpp_581:
        mov %esi,%eax
        cmp %rax,%rdi
        setge %al
        ret
        .size u_cpp_581, .-u_cpp_581
        .globl u_cpp_582
        .type u_cpp_582, @function
u_cpp_582:
        movslq %esi,%rax
        cmp %rax,%rdi
        setae %al
        ret
        .size u_cpp_582, .-u_cpp_582
        .globl u_cpp_583
        .type u_cpp_583, @function
u_cpp_583:
        cmp %rsi,%rdi
        setae %al
        ret
        .size u_cpp_583, .-u_cpp_583
        .globl u_cpp_584
        .type u_cpp_584, @function
u_cpp_584:
        cmp %rsi,%rdi
        setae %al
        ret
        .size u_cpp_584, .-u_cpp_584
        .globl u_cpp_587
        .type u_cpp_587, @function
u_cpp_587:
        mov %esi,%eax
        cmp %rax,%rdi
        setae %al
        ret
        .size u_cpp_587, .-u_cpp_587
        .globl u_cpp_588
        .type u_cpp_588, @function
u_cpp_588:
        cvtsi2ss %edi,%xmm1
        ucomiss %xmm1,%xmm0
        setae %al
        ret
        .size u_cpp_588, .-u_cpp_588
        .globl u_cpp_589
        .type u_cpp_589, @function
u_cpp_589:
        cvtsi2ss %rdi,%xmm1
        ucomiss %xmm1,%xmm0
        setae %al
        ret
        .size u_cpp_589, .-u_cpp_589
        .globl u_cpp_591
        .type u_cpp_591, @function
u_cpp_591:
        ucomiss %xmm1,%xmm0
        setae %al
        ret
        .size u_cpp_591, .-u_cpp_591
        .globl u_cpp_592
        .type u_cpp_592, @function
u_cpp_592:
        cvtss2sd %xmm0,%xmm2
        ucomisd %xmm1,%xmm2
        setae %al
        ret
        .size u_cpp_592, .-u_cpp_592
        .globl u_cpp_593
        .type u_cpp_593, @function
u_cpp_593:
        cvtsi2ss %edi,%xmm1
        ucomiss %xmm1,%xmm0
        setae %al
        ret
        .size u_cpp_593, .-u_cpp_593
        .globl u_cpp_594
        .type u_cpp_594, @function
u_cpp_594:
        cvtsi2sd %edi,%xmm1
        ucomisd %xmm1,%xmm0
        setae %al
        ret
        .size u_cpp_594, .-u_cpp_594
        .globl u_cpp_595
        .type u_cpp_595, @function
u_cpp_595:
        cvtsi2sd %rdi,%xmm1
        ucomisd %xmm1,%xmm0
        setae %al
        ret
        .size u_cpp_595, .-u_cpp_595
        .globl u_cpp_597
        .type u_cpp_597, @function
u_cpp_597:
        cvtss2sd %xmm1,%xmm2
        ucomisd %xmm2,%xmm0
        setae %al
        ret
        .size u_cpp_597, .-u_cpp_597
        .globl u_cpp_598
        .type u_cpp_598, @function
u_cpp_598:
        ucomisd %xmm1,%xmm0
        setae %al
        ret
        .size u_cpp_598, .-u_cpp_598
        .globl u_cpp_599
        .type u_cpp_599, @function
u_cpp_599:
        cvtsi2sd %edi,%xmm1
        ucomisd %xmm1,%xmm0
        setae %al
        ret
        .size u_cpp_599, .-u_cpp_599
        .globl u_cpp_600
        .type u_cpp_600, @function
u_cpp_600:
        cmp %edi,%esi
        setle %al
        ret
        .size u_cpp_600, .-u_cpp_600
        .globl u_cpp_601
        .type u_cpp_601, @function
u_cpp_601:
        mov %edi,%eax
        cmp %rax,%rsi
        setle %al
        ret
        .size u_cpp_601, .-u_cpp_601
        .globl u_cpp_602
        .type u_cpp_602, @function
u_cpp_602:
        mov %edi,%eax
        cmp %rax,%rsi
        setbe %al
        ret
        .size u_cpp_602, .-u_cpp_602
        .globl u_cpp_603
        .type u_cpp_603, @function
u_cpp_603:
        cvtsi2ss %edi,%xmm1
        ucomiss %xmm0,%xmm1
        setae %al
        ret
        .size u_cpp_603, .-u_cpp_603
        .globl u_cpp_604
        .type u_cpp_604, @function
u_cpp_604:
        cvtsi2sd %edi,%xmm1
        ucomisd %xmm0,%xmm1
        setae %al
        ret
        .size u_cpp_604, .-u_cpp_604
        .globl u_cpp_605
        .type u_cpp_605, @function
u_cpp_605:
        mov %esi,%eax
        xor $0x1,%al
        or %dil,%al
        ret
        .size u_cpp_605, .-u_cpp_605
        .globl u_cpp_606
        .type u_cpp_606, @function
u_cpp_606:
        cmp %esi,%edi
        setle %al
        ret
        .size u_cpp_606, .-u_cpp_606
        .globl u_cpp_607
        .type u_cpp_607, @function
u_cpp_607:
        movslq %edi,%rax
        cmp %rax,%rsi
        setge %al
        ret
        .size u_cpp_607, .-u_cpp_607
        .globl u_cpp_608
        .type u_cpp_608, @function
u_cpp_608:
        movslq %edi,%rax
        cmp %rax,%rsi
        setae %al
        ret
        .size u_cpp_608, .-u_cpp_608
        .globl u_cpp_609
        .type u_cpp_609, @function
u_cpp_609:
        cvtsi2ss %edi,%xmm1
        ucomiss %xmm1,%xmm0
        setae %al
        ret
        .size u_cpp_609, .-u_cpp_609
        .globl u_cpp_610
        .type u_cpp_610, @function
u_cpp_610:
        cvtsi2sd %edi,%xmm1
        ucomisd %xmm1,%xmm0
        setae %al
        ret
        .size u_cpp_610, .-u_cpp_610
        .globl u_cpp_611
        .type u_cpp_611, @function
u_cpp_611:
        cmp %esi,%edi
        setle %al
        ret
        .size u_cpp_611, .-u_cpp_611
        .globl u_cpp_612
        .type u_cpp_612, @function
u_cpp_612:
        movslq %esi,%rax
        cmp %rax,%rdi
        setle %al
        ret
        .size u_cpp_612, .-u_cpp_612
        .globl u_cpp_613
        .type u_cpp_613, @function
u_cpp_613:
        cmp %rsi,%rdi
        setle %al
        ret
        .size u_cpp_613, .-u_cpp_613
        .globl u_cpp_614
        .type u_cpp_614, @function
u_cpp_614:
        cmp %rsi,%rdi
        setbe %al
        ret
        .size u_cpp_614, .-u_cpp_614
        .globl u_cpp_615
        .type u_cpp_615, @function
u_cpp_615:
        cvtsi2ss %rdi,%xmm1
        ucomiss %xmm1,%xmm0
        setae %al
        ret
        .size u_cpp_615, .-u_cpp_615
        .globl u_cpp_616
        .type u_cpp_616, @function
u_cpp_616:
        cvtsi2sd %rdi,%xmm1
        ucomisd %xmm1,%xmm0
        setae %al
        ret
        .size u_cpp_616, .-u_cpp_616
        .globl u_cpp_617
        .type u_cpp_617, @function
u_cpp_617:
        mov %esi,%eax
        cmp %rax,%rdi
        setle %al
        ret
        .size u_cpp_617, .-u_cpp_617
        .globl u_cpp_618
        .type u_cpp_618, @function
u_cpp_618:
        movslq %esi,%rax
        cmp %rax,%rdi
        setbe %al
        ret
        .size u_cpp_618, .-u_cpp_618
        .globl u_cpp_619
        .type u_cpp_619, @function
u_cpp_619:
        cmp %rsi,%rdi
        setbe %al
        ret
        .size u_cpp_619, .-u_cpp_619
        .globl u_cpp_620
        .type u_cpp_620, @function
u_cpp_620:
        cmp %rsi,%rdi
        setbe %al
        ret
        .size u_cpp_620, .-u_cpp_620
        .globl u_cpp_623
        .type u_cpp_623, @function
u_cpp_623:
        mov %esi,%eax
        cmp %rax,%rdi
        setbe %al
        ret
        .size u_cpp_623, .-u_cpp_623
        .globl u_cpp_624
        .type u_cpp_624, @function
u_cpp_624:
        cvtsi2ss %edi,%xmm1
        ucomiss %xmm0,%xmm1
        setae %al
        ret
        .size u_cpp_624, .-u_cpp_624
        .globl u_cpp_625
        .type u_cpp_625, @function
u_cpp_625:
        cvtsi2ss %rdi,%xmm1
        ucomiss %xmm0,%xmm1
        setae %al
        ret
        .size u_cpp_625, .-u_cpp_625
        .globl u_cpp_627
        .type u_cpp_627, @function
u_cpp_627:
        ucomiss %xmm0,%xmm1
        setae %al
        ret
        .size u_cpp_627, .-u_cpp_627
        .globl u_cpp_628
        .type u_cpp_628, @function
u_cpp_628:
        cvtss2sd %xmm0,%xmm2
        ucomisd %xmm2,%xmm1
        setae %al
        ret
        .size u_cpp_628, .-u_cpp_628
        .globl u_cpp_629
        .type u_cpp_629, @function
u_cpp_629:
        cvtsi2ss %edi,%xmm1
        ucomiss %xmm0,%xmm1
        setae %al
        ret
        .size u_cpp_629, .-u_cpp_629
        .globl u_cpp_630
        .type u_cpp_630, @function
u_cpp_630:
        cvtsi2sd %edi,%xmm1
        ucomisd %xmm0,%xmm1
        setae %al
        ret
        .size u_cpp_630, .-u_cpp_630
        .globl u_cpp_631
        .type u_cpp_631, @function
u_cpp_631:
        cvtsi2sd %rdi,%xmm1
        ucomisd %xmm0,%xmm1
        setae %al
        ret
        .size u_cpp_631, .-u_cpp_631
        .globl u_cpp_633
        .type u_cpp_633, @function
u_cpp_633:
        cvtss2sd %xmm1,%xmm2
        ucomisd %xmm0,%xmm2
        setae %al
        ret
        .size u_cpp_633, .-u_cpp_633
        .globl u_cpp_634
        .type u_cpp_634, @function
u_cpp_634:
        ucomisd %xmm0,%xmm1
        setae %al
        ret
        .size u_cpp_634, .-u_cpp_634
        .globl u_cpp_635
        .type u_cpp_635, @function
u_cpp_635:
        cvtsi2sd %edi,%xmm1
        ucomisd %xmm0,%xmm1
        setae %al
        ret
        .size u_cpp_635, .-u_cpp_635
        .globl u_cpp_636
        .type u_cpp_636, @function
u_cpp_636:
        cmp %edi,%esi
        setge %al
        ret
        .size u_cpp_636, .-u_cpp_636
        .globl u_cpp_637
        .type u_cpp_637, @function
u_cpp_637:
        mov %edi,%eax
        cmp %rax,%rsi
        setge %al
        ret
        .size u_cpp_637, .-u_cpp_637
        .globl u_cpp_638
        .type u_cpp_638, @function
u_cpp_638:
        mov %edi,%eax
        cmp %rax,%rsi
        setae %al
        ret
        .size u_cpp_638, .-u_cpp_638
        .globl u_cpp_639
        .type u_cpp_639, @function
u_cpp_639:
        cvtsi2ss %edi,%xmm1
        ucomiss %xmm1,%xmm0
        setae %al
        ret
        .size u_cpp_639, .-u_cpp_639
        .globl u_cpp_640
        .type u_cpp_640, @function
u_cpp_640:
        cvtsi2sd %edi,%xmm1
        ucomisd %xmm1,%xmm0
        setae %al
        ret
        .size u_cpp_640, .-u_cpp_640
        .globl u_cpp_641
        .type u_cpp_641, @function
u_cpp_641:
        mov %edi,%eax
        xor $0x1,%al
        or %sil,%al
        ret
        .size u_cpp_641, .-u_cpp_641
        .globl u_cpp_642
        .type u_cpp_642, @function
u_cpp_642:
        cmp %esi,%edi
        setl %al
        ret
        .size u_cpp_642, .-u_cpp_642
        .globl u_cpp_643
        .type u_cpp_643, @function
u_cpp_643:
        movslq %edi,%rax
        cmp %rax,%rsi
        setg %al
        ret
        .size u_cpp_643, .-u_cpp_643
        .globl u_cpp_644
        .type u_cpp_644, @function
u_cpp_644:
        movslq %edi,%rax
        cmp %rax,%rsi
        seta %al
        ret
        .size u_cpp_644, .-u_cpp_644
        .globl u_cpp_645
        .type u_cpp_645, @function
u_cpp_645:
        cvtsi2ss %edi,%xmm1
        ucomiss %xmm1,%xmm0
        seta %al
        ret
        .size u_cpp_645, .-u_cpp_645
        .globl u_cpp_646
        .type u_cpp_646, @function
u_cpp_646:
        cvtsi2sd %edi,%xmm1
        ucomisd %xmm1,%xmm0
        seta %al
        ret
        .size u_cpp_646, .-u_cpp_646
        .globl u_cpp_647
        .type u_cpp_647, @function
u_cpp_647:
        cmp %esi,%edi
        setl %al
        ret
        .size u_cpp_647, .-u_cpp_647
        .globl u_cpp_648
        .type u_cpp_648, @function
u_cpp_648:
        movslq %esi,%rax
        cmp %rax,%rdi
        setl %al
        ret
        .size u_cpp_648, .-u_cpp_648
        .globl u_cpp_649
        .type u_cpp_649, @function
u_cpp_649:
        cmp %rsi,%rdi
        setl %al
        ret
        .size u_cpp_649, .-u_cpp_649
        .globl u_cpp_650
        .type u_cpp_650, @function
u_cpp_650:
        cmp %rsi,%rdi
        setb %al
        ret
        .size u_cpp_650, .-u_cpp_650
        .globl u_cpp_651
        .type u_cpp_651, @function
u_cpp_651:
        cvtsi2ss %rdi,%xmm1
        ucomiss %xmm1,%xmm0
        seta %al
        ret
        .size u_cpp_651, .-u_cpp_651
        .globl u_cpp_652
        .type u_cpp_652, @function
u_cpp_652:
        cvtsi2sd %rdi,%xmm1
        ucomisd %xmm1,%xmm0
        seta %al
        ret
        .size u_cpp_652, .-u_cpp_652
        .globl u_cpp_653
        .type u_cpp_653, @function
u_cpp_653:
        mov %esi,%eax
        cmp %rax,%rdi
        setl %al
        ret
        .size u_cpp_653, .-u_cpp_653
        .globl u_cpp_654
        .type u_cpp_654, @function
u_cpp_654:
        movslq %esi,%rax
        cmp %rax,%rdi
        setb %al
        ret
        .size u_cpp_654, .-u_cpp_654
        .globl u_cpp_655
        .type u_cpp_655, @function
u_cpp_655:
        cmp %rsi,%rdi
        setb %al
        ret
        .size u_cpp_655, .-u_cpp_655
        .globl u_cpp_656
        .type u_cpp_656, @function
u_cpp_656:
        cmp %rsi,%rdi
        setb %al
        ret
        .size u_cpp_656, .-u_cpp_656
        .globl u_cpp_659
        .type u_cpp_659, @function
u_cpp_659:
        test %rdi,%rdi
        sete %al
        and %sil,%al
        ret
        .size u_cpp_659, .-u_cpp_659
        .globl u_cpp_660
        .type u_cpp_660, @function
u_cpp_660:
        cvtsi2ss %edi,%xmm1
        ucomiss %xmm0,%xmm1
        seta %al
        ret
        .size u_cpp_660, .-u_cpp_660
        .globl u_cpp_661
        .type u_cpp_661, @function
u_cpp_661:
        cvtsi2ss %rdi,%xmm1
        ucomiss %xmm0,%xmm1
        seta %al
        ret
        .size u_cpp_661, .-u_cpp_661
        .globl u_cpp_663
        .type u_cpp_663, @function
u_cpp_663:
        ucomiss %xmm0,%xmm1
        seta %al
        ret
        .size u_cpp_663, .-u_cpp_663
        .globl u_cpp_664
        .type u_cpp_664, @function
u_cpp_664:
        cvtss2sd %xmm0,%xmm2
        ucomisd %xmm2,%xmm1
        seta %al
        ret
        .size u_cpp_664, .-u_cpp_664
        .globl u_cpp_665
        .type u_cpp_665, @function
u_cpp_665:
        cvtsi2ss %edi,%xmm1
        ucomiss %xmm0,%xmm1
        seta %al
        ret
        .size u_cpp_665, .-u_cpp_665
        .globl u_cpp_666
        .type u_cpp_666, @function
u_cpp_666:
        cvtsi2sd %edi,%xmm1
        ucomisd %xmm0,%xmm1
        seta %al
        ret
        .size u_cpp_666, .-u_cpp_666
        .globl u_cpp_667
        .type u_cpp_667, @function
u_cpp_667:
        cvtsi2sd %rdi,%xmm1
        ucomisd %xmm0,%xmm1
        seta %al
        ret
        .size u_cpp_667, .-u_cpp_667
        .globl u_cpp_669
        .type u_cpp_669, @function
u_cpp_669:
        cvtss2sd %xmm1,%xmm2
        ucomisd %xmm0,%xmm2
        seta %al
        ret
        .size u_cpp_669, .-u_cpp_669
        .globl u_cpp_670
        .type u_cpp_670, @function
u_cpp_670:
        ucomisd %xmm0,%xmm1
        seta %al
        ret
        .size u_cpp_670, .-u_cpp_670
        .globl u_cpp_671
        .type u_cpp_671, @function
u_cpp_671:
        cvtsi2sd %edi,%xmm1
        ucomisd %xmm0,%xmm1
        seta %al
        ret
        .size u_cpp_671, .-u_cpp_671
        .globl u_cpp_672
        .type u_cpp_672, @function
u_cpp_672:
        cmp %edi,%esi
        setg %al
        ret
        .size u_cpp_672, .-u_cpp_672
        .globl u_cpp_673
        .type u_cpp_673, @function
u_cpp_673:
        mov %edi,%eax
        cmp %rax,%rsi
        setg %al
        ret
        .size u_cpp_673, .-u_cpp_673
        .globl u_cpp_674
        .type u_cpp_674, @function
u_cpp_674:
        mov %edi,%eax
        cmp %rax,%rsi
        seta %al
        ret
        .size u_cpp_674, .-u_cpp_674
        .globl u_cpp_675
        .type u_cpp_675, @function
u_cpp_675:
        cvtsi2ss %edi,%xmm1
        ucomiss %xmm1,%xmm0
        seta %al
        ret
        .size u_cpp_675, .-u_cpp_675
        .globl u_cpp_676
        .type u_cpp_676, @function
u_cpp_676:
        cvtsi2sd %edi,%xmm1
        ucomisd %xmm1,%xmm0
        seta %al
        ret
        .size u_cpp_676, .-u_cpp_676
        .globl u_cpp_677
        .type u_cpp_677, @function
u_cpp_677:
        mov %edi,%eax
        xor $0x1,%al
        and %sil,%al
        ret
        .size u_cpp_677, .-u_cpp_677
        .globl u_cpp_678
        .type u_cpp_678, @function
u_cpp_678:
        mov %esi,%ecx
        mov %edi,%eax
        shl %cl,%eax
        ret
        .size u_cpp_678, .-u_cpp_678
        .globl u_cpp_679
        .type u_cpp_679, @function
u_cpp_679:
        mov %rsi,%rcx
        mov %edi,%eax
        shl %cl,%eax
        ret
        .size u_cpp_679, .-u_cpp_679
        .globl u_cpp_680
        .type u_cpp_680, @function
u_cpp_680:
        mov %rsi,%rcx
        mov %edi,%eax
        shl %cl,%eax
        ret
        .size u_cpp_680, .-u_cpp_680
        .globl u_cpp_683
        .type u_cpp_683, @function
u_cpp_683:
        mov %esi,%ecx
        mov %edi,%eax
        shl %cl,%eax
        ret
        .size u_cpp_683, .-u_cpp_683
        .globl u_cpp_684
        .type u_cpp_684, @function
u_cpp_684:
        mov %esi,%ecx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_cpp_684, .-u_cpp_684
        .globl u_cpp_685
        .type u_cpp_685, @function
u_cpp_685:
        mov %rsi,%rcx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_cpp_685, .-u_cpp_685
        .globl u_cpp_686
        .type u_cpp_686, @function
u_cpp_686:
        mov %rsi,%rcx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_cpp_686, .-u_cpp_686
        .globl u_cpp_689
        .type u_cpp_689, @function
u_cpp_689:
        mov %esi,%ecx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_cpp_689, .-u_cpp_689
        .globl u_cpp_690
        .type u_cpp_690, @function
u_cpp_690:
        mov %esi,%ecx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_cpp_690, .-u_cpp_690
        .globl u_cpp_691
        .type u_cpp_691, @function
u_cpp_691:
        mov %rsi,%rcx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_cpp_691, .-u_cpp_691
        .globl u_cpp_692
        .type u_cpp_692, @function
u_cpp_692:
        mov %rsi,%rcx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_cpp_692, .-u_cpp_692
        .globl u_cpp_695
        .type u_cpp_695, @function
u_cpp_695:
        mov %esi,%ecx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_cpp_695, .-u_cpp_695
        .globl u_cpp_708
        .type u_cpp_708, @function
u_cpp_708:
        mov %esi,%ecx
        mov %edi,%eax
        shl %cl,%eax
        ret
        .size u_cpp_708, .-u_cpp_708
        .globl u_cpp_709
        .type u_cpp_709, @function
u_cpp_709:
        mov %rsi,%rcx
        mov %edi,%eax
        shl %cl,%eax
        ret
        .size u_cpp_709, .-u_cpp_709
        .globl u_cpp_710
        .type u_cpp_710, @function
u_cpp_710:
        mov %rsi,%rcx
        mov %edi,%eax
        shl %cl,%eax
        ret
        .size u_cpp_710, .-u_cpp_710
        .globl u_cpp_713
        .type u_cpp_713, @function
u_cpp_713:
        mov %esi,%ecx
        mov %edi,%eax
        shl %cl,%eax
        ret
        .size u_cpp_713, .-u_cpp_713
        .globl u_cpp_714
        .type u_cpp_714, @function
u_cpp_714:
        mov %esi,%ecx
        mov %edi,%eax
        sar %cl,%eax
        ret
        .size u_cpp_714, .-u_cpp_714
        .globl u_cpp_715
        .type u_cpp_715, @function
u_cpp_715:
        mov %rsi,%rcx
        mov %edi,%eax
        sar %cl,%eax
        ret
        .size u_cpp_715, .-u_cpp_715
        .globl u_cpp_716
        .type u_cpp_716, @function
u_cpp_716:
        mov %rsi,%rcx
        mov %edi,%eax
        sar %cl,%eax
        ret
        .size u_cpp_716, .-u_cpp_716
        .globl u_cpp_719
        .type u_cpp_719, @function
u_cpp_719:
        mov %esi,%ecx
        mov %edi,%eax
        sar %cl,%eax
        ret
        .size u_cpp_719, .-u_cpp_719
        .globl u_cpp_720
        .type u_cpp_720, @function
u_cpp_720:
        mov %esi,%ecx
        mov %rdi,%rax
        sar %cl,%rax
        ret
        .size u_cpp_720, .-u_cpp_720
        .globl u_cpp_721
        .type u_cpp_721, @function
u_cpp_721:
        mov %rsi,%rcx
        mov %rdi,%rax
        sar %cl,%rax
        ret
        .size u_cpp_721, .-u_cpp_721
        .globl u_cpp_722
        .type u_cpp_722, @function
u_cpp_722:
        mov %rsi,%rcx
        mov %rdi,%rax
        sar %cl,%rax
        ret
        .size u_cpp_722, .-u_cpp_722
        .globl u_cpp_725
        .type u_cpp_725, @function
u_cpp_725:
        mov %esi,%ecx
        mov %rdi,%rax
        sar %cl,%rax
        ret
        .size u_cpp_725, .-u_cpp_725
        .globl u_cpp_726
        .type u_cpp_726, @function
u_cpp_726:
        mov %esi,%ecx
        mov %rdi,%rax
        shr %cl,%rax
        ret
        .size u_cpp_726, .-u_cpp_726
        .globl u_cpp_727
        .type u_cpp_727, @function
u_cpp_727:
        mov %rsi,%rcx
        mov %rdi,%rax
        shr %cl,%rax
        ret
        .size u_cpp_727, .-u_cpp_727
        .globl u_cpp_728
        .type u_cpp_728, @function
u_cpp_728:
        mov %rsi,%rcx
        mov %rdi,%rax
        shr %cl,%rax
        ret
        .size u_cpp_728, .-u_cpp_728
        .globl u_cpp_731
        .type u_cpp_731, @function
u_cpp_731:
        mov %esi,%ecx
        mov %rdi,%rax
        shr %cl,%rax
        ret
        .size u_cpp_731, .-u_cpp_731
        .globl u_cpp_744
        .type u_cpp_744, @function
u_cpp_744:
        mov %esi,%ecx
        mov %edi,%eax
        shr %cl,%eax
        ret
        .size u_cpp_744, .-u_cpp_744
        .globl u_cpp_745
        .type u_cpp_745, @function
u_cpp_745:
        mov %rsi,%rcx
        mov %edi,%eax
        shr %cl,%eax
        ret
        .size u_cpp_745, .-u_cpp_745
        .globl u_cpp_746
        .type u_cpp_746, @function
u_cpp_746:
        mov %rsi,%rcx
        mov %edi,%eax
        shr %cl,%eax
        ret
        .size u_cpp_746, .-u_cpp_746
        .globl u_cpp_749
        .type u_cpp_749, @function
u_cpp_749:
        mov %esi,%ecx
        mov %edi,%eax
        shr %cl,%eax
        ret
        .size u_cpp_749, .-u_cpp_749
        .globl u_cpp_750
        .type u_cpp_750, @function
u_cpp_750:
        cmp %esi,%edi
        setl %cl
        setg %al
        sub %cl,%al
        ret
        .size u_cpp_750, .-u_cpp_750
        .globl u_cpp_751
        .type u_cpp_751, @function
u_cpp_751:
        movslq %edi,%rax
        cmp %rsi,%rax
        setl %cl
        setg %al
        sub %cl,%al
        ret
        .size u_cpp_751, .-u_cpp_751
        .globl u_cpp_753
        .type u_cpp_753, @function
u_cpp_753:
        cvtsi2ss %edi,%xmm1
        ucomiss %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        add %cl,%cl
        ucomiss %xmm0,%xmm1
        movzbl %cl,%r10d
        mov $0x1,%ecx
        cmovbe %r10d,%ecx
        ucomiss %xmm1,%xmm0
        mov $0xff,%eax
        cmovbe %ecx,%eax
        ret
        .size u_cpp_753, .-u_cpp_753
        .globl u_cpp_754
        .type u_cpp_754, @function
u_cpp_754:
        cvtsi2sd %edi,%xmm1
        ucomisd %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        add %cl,%cl
        ucomisd %xmm0,%xmm1
        movzbl %cl,%r10d
        mov $0x1,%ecx
        cmovbe %r10d,%ecx
        ucomisd %xmm1,%xmm0
        mov $0xff,%eax
        cmovbe %ecx,%eax
        ret
        .size u_cpp_754, .-u_cpp_754
        .globl u_cpp_756
        .type u_cpp_756, @function
u_cpp_756:
        movslq %esi,%rax
        cmp %rax,%rdi
        setl %cl
        setg %al
        sub %cl,%al
        ret
        .size u_cpp_756, .-u_cpp_756
        .globl u_cpp_757
        .type u_cpp_757, @function
u_cpp_757:
        cmp %rsi,%rdi
        setl %cl
        setg %al
        sub %cl,%al
        ret
        .size u_cpp_757, .-u_cpp_757
        .globl u_cpp_759
        .type u_cpp_759, @function
u_cpp_759:
        cvtsi2ss %rdi,%xmm1
        ucomiss %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        add %cl,%cl
        ucomiss %xmm0,%xmm1
        movzbl %cl,%r10d
        mov $0x1,%ecx
        cmovbe %r10d,%ecx
        ucomiss %xmm1,%xmm0
        mov $0xff,%eax
        cmovbe %ecx,%eax
        ret
        .size u_cpp_759, .-u_cpp_759
        .globl u_cpp_760
        .type u_cpp_760, @function
u_cpp_760:
        cvtsi2sd %rdi,%xmm1
        ucomisd %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        add %cl,%cl
        ucomisd %xmm0,%xmm1
        movzbl %cl,%r10d
        mov $0x1,%ecx
        cmovbe %r10d,%ecx
        ucomisd %xmm1,%xmm0
        mov $0xff,%eax
        cmovbe %ecx,%eax
        ret
        .size u_cpp_760, .-u_cpp_760
        .globl u_cpp_764
        .type u_cpp_764, @function
u_cpp_764:
        cmp %rsi,%rdi
        seta %al
        sbb $0x0,%al
        ret
        .size u_cpp_764, .-u_cpp_764
        .globl u_cpp_768
        .type u_cpp_768, @function
u_cpp_768:
        cvtsi2ss %edi,%xmm1
        ucomiss %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        add %cl,%cl
        ucomiss %xmm1,%xmm0
        movzbl %cl,%r10d
        mov $0x1,%ecx
        cmovbe %r10d,%ecx
        ucomiss %xmm0,%xmm1
        mov $0xff,%eax
        cmovbe %ecx,%eax
        ret
        .size u_cpp_768, .-u_cpp_768
        .globl u_cpp_769
        .type u_cpp_769, @function
u_cpp_769:
        cvtsi2ss %rdi,%xmm1
        ucomiss %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        add %cl,%cl
        ucomiss %xmm1,%xmm0
        movzbl %cl,%r10d
        mov $0x1,%ecx
        cmovbe %r10d,%ecx
        ucomiss %xmm0,%xmm1
        mov $0xff,%eax
        cmovbe %ecx,%eax
        ret
        .size u_cpp_769, .-u_cpp_769
        .globl u_cpp_771
        .type u_cpp_771, @function
u_cpp_771:
        ucomiss %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        add %cl,%cl
        ucomiss %xmm1,%xmm0
        movzbl %cl,%r10d
        mov $0x1,%ecx
        cmovbe %r10d,%ecx
        ucomiss %xmm0,%xmm1
        mov $0xff,%eax
        cmovbe %ecx,%eax
        ret
        .size u_cpp_771, .-u_cpp_771
        .globl u_cpp_772
        .type u_cpp_772, @function
u_cpp_772:
        cvtss2sd %xmm0,%xmm2
        ucomisd %xmm2,%xmm1
        setp %r10b
        setne %cl
        or %r10b,%cl
        add %cl,%cl
        ucomisd %xmm1,%xmm2
        movzbl %cl,%r10d
        mov $0x1,%ecx
        cmovbe %r10d,%ecx
        ucomisd %xmm2,%xmm1
        mov $0xff,%eax
        cmovbe %ecx,%eax
        ret
        .size u_cpp_772, .-u_cpp_772
        .globl u_cpp_774
        .type u_cpp_774, @function
u_cpp_774:
        cvtsi2sd %edi,%xmm1
        ucomisd %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        add %cl,%cl
        ucomisd %xmm1,%xmm0
        movzbl %cl,%r10d
        mov $0x1,%ecx
        cmovbe %r10d,%ecx
        ucomisd %xmm0,%xmm1
        mov $0xff,%eax
        cmovbe %ecx,%eax
        ret
        .size u_cpp_774, .-u_cpp_774
        .globl u_cpp_775
        .type u_cpp_775, @function
u_cpp_775:
        cvtsi2sd %rdi,%xmm1
        ucomisd %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        add %cl,%cl
        ucomisd %xmm1,%xmm0
        movzbl %cl,%r10d
        mov $0x1,%ecx
        cmovbe %r10d,%ecx
        ucomisd %xmm0,%xmm1
        mov $0xff,%eax
        cmovbe %ecx,%eax
        ret
        .size u_cpp_775, .-u_cpp_775
        .globl u_cpp_777
        .type u_cpp_777, @function
u_cpp_777:
        cvtss2sd %xmm1,%xmm2
        ucomisd %xmm2,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        add %cl,%cl
        ucomisd %xmm2,%xmm0
        movzbl %cl,%r10d
        mov $0x1,%ecx
        cmovbe %r10d,%ecx
        ucomisd %xmm0,%xmm2
        mov $0xff,%eax
        cmovbe %ecx,%eax
        ret
        .size u_cpp_777, .-u_cpp_777
        .globl u_cpp_778
        .type u_cpp_778, @function
u_cpp_778:
        ucomisd %xmm1,%xmm0
        setp %r10b
        setne %cl
        or %r10b,%cl
        add %cl,%cl
        ucomisd %xmm1,%xmm0
        movzbl %cl,%r10d
        mov $0x1,%ecx
        cmovbe %r10d,%ecx
        ucomisd %xmm0,%xmm1
        mov $0xff,%eax
        cmovbe %ecx,%eax
        ret
        .size u_cpp_778, .-u_cpp_778
        .globl u_cpp_785
        .type u_cpp_785, @function
u_cpp_785:
        mov %edi,%r10d
        not %r10b
        and %sil,%r10b
        neg %r10b
        or $0x1,%r10b
        xor %ecx,%ecx
        xor %sil,%dil
        movzbl %r10b,%eax
        cmove %ecx,%eax
        ret
        .size u_cpp_785, .-u_cpp_785
        .globl u_cpp_786
        .type u_cpp_786, @function
u_cpp_786:
        or %esi,%edi
        setne %al
        ret
        .size u_cpp_786, .-u_cpp_786
        .globl u_cpp_787
        .type u_cpp_787, @function
u_cpp_787:
        test %edi,%edi
        setne %cl
        test %rsi,%rsi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_787, .-u_cpp_787
        .globl u_cpp_788
        .type u_cpp_788, @function
u_cpp_788:
        test %edi,%edi
        setne %cl
        test %rsi,%rsi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_788, .-u_cpp_788
        .globl u_cpp_789
        .type u_cpp_789, @function
u_cpp_789:
        test %edi,%edi
        setne %cl
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        or %cl,%al
        ret
        .size u_cpp_789, .-u_cpp_789
        .globl u_cpp_790
        .type u_cpp_790, @function
u_cpp_790:
        test %edi,%edi
        setne %cl
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        or %cl,%al
        ret
        .size u_cpp_790, .-u_cpp_790
        .globl u_cpp_791
        .type u_cpp_791, @function
u_cpp_791:
        test %edi,%edi
        setne %al
        or %sil,%al
        ret
        .size u_cpp_791, .-u_cpp_791
        .globl u_cpp_792
        .type u_cpp_792, @function
u_cpp_792:
        test %rdi,%rdi
        setne %cl
        test %esi,%esi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_792, .-u_cpp_792
        .globl u_cpp_793
        .type u_cpp_793, @function
u_cpp_793:
        or %rsi,%rdi
        setne %al
        ret
        .size u_cpp_793, .-u_cpp_793
        .globl u_cpp_794
        .type u_cpp_794, @function
u_cpp_794:
        or %rsi,%rdi
        setne %al
        ret
        .size u_cpp_794, .-u_cpp_794
        .globl u_cpp_795
        .type u_cpp_795, @function
u_cpp_795:
        test %rdi,%rdi
        setne %cl
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        or %cl,%al
        ret
        .size u_cpp_795, .-u_cpp_795
        .globl u_cpp_796
        .type u_cpp_796, @function
u_cpp_796:
        test %rdi,%rdi
        setne %cl
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        or %cl,%al
        ret
        .size u_cpp_796, .-u_cpp_796
        .globl u_cpp_797
        .type u_cpp_797, @function
u_cpp_797:
        test %rdi,%rdi
        setne %al
        or %sil,%al
        ret
        .size u_cpp_797, .-u_cpp_797
        .globl u_cpp_798
        .type u_cpp_798, @function
u_cpp_798:
        test %rdi,%rdi
        setne %cl
        test %esi,%esi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_798, .-u_cpp_798
        .globl u_cpp_799
        .type u_cpp_799, @function
u_cpp_799:
        or %rsi,%rdi
        setne %al
        ret
        .size u_cpp_799, .-u_cpp_799
        .globl u_cpp_800
        .type u_cpp_800, @function
u_cpp_800:
        or %rsi,%rdi
        setne %al
        ret
        .size u_cpp_800, .-u_cpp_800
        .globl u_cpp_801
        .type u_cpp_801, @function
u_cpp_801:
        test %rdi,%rdi
        setne %cl
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        or %cl,%al
        ret
        .size u_cpp_801, .-u_cpp_801
        .globl u_cpp_802
        .type u_cpp_802, @function
u_cpp_802:
        test %rdi,%rdi
        setne %cl
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        or %cl,%al
        ret
        .size u_cpp_802, .-u_cpp_802
        .globl u_cpp_803
        .type u_cpp_803, @function
u_cpp_803:
        test %rdi,%rdi
        setne %al
        or %sil,%al
        ret
        .size u_cpp_803, .-u_cpp_803
        .globl u_cpp_804
        .type u_cpp_804, @function
u_cpp_804:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %edi,%edi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_804, .-u_cpp_804
        .globl u_cpp_805
        .type u_cpp_805, @function
u_cpp_805:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %rdi,%rdi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_805, .-u_cpp_805
        .globl u_cpp_806
        .type u_cpp_806, @function
u_cpp_806:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %rdi,%rdi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_806, .-u_cpp_806
        .globl u_cpp_807
        .type u_cpp_807, @function
u_cpp_807:
        xorps %xmm2,%xmm2
        cmpneqss %xmm2,%xmm1
        cmpneqss %xmm2,%xmm0
        orps %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%al
        ret
        .size u_cpp_807, .-u_cpp_807
        .globl u_cpp_808
        .type u_cpp_808, @function
u_cpp_808:
        xorps %xmm2,%xmm2
        ucomiss %xmm2,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        xorps %xmm0,%xmm0
        ucomisd %xmm0,%xmm1
        setp %dl
        setne %al
        or %dl,%al
        or %cl,%al
        ret
        .size u_cpp_808, .-u_cpp_808
        .globl u_cpp_809
        .type u_cpp_809, @function
u_cpp_809:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %cl
        setne %al
        or %cl,%al
        or %dil,%al
        ret
        .size u_cpp_809, .-u_cpp_809
        .globl u_cpp_810
        .type u_cpp_810, @function
u_cpp_810:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %edi,%edi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_810, .-u_cpp_810
        .globl u_cpp_811
        .type u_cpp_811, @function
u_cpp_811:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %rdi,%rdi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_811, .-u_cpp_811
        .globl u_cpp_812
        .type u_cpp_812, @function
u_cpp_812:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %rdi,%rdi
        setne %al
        or %cl,%al
        ret
        .size u_cpp_812, .-u_cpp_812
        .globl u_cpp_813
        .type u_cpp_813, @function
u_cpp_813:
        xorpd %xmm2,%xmm2
        ucomisd %xmm2,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        xorpd %xmm0,%xmm0
        ucomiss %xmm0,%xmm1
        setp %dl
        setne %al
        or %dl,%al
        or %cl,%al
        ret
        .size u_cpp_813, .-u_cpp_813
        .globl u_cpp_814
        .type u_cpp_814, @function
u_cpp_814:
        xorpd %xmm2,%xmm2
        cmpneqsd %xmm2,%xmm1
        cmpneqsd %xmm2,%xmm0
        orpd %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%al
        ret
        .size u_cpp_814, .-u_cpp_814
        .globl u_cpp_815
        .type u_cpp_815, @function
u_cpp_815:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %cl
        setne %al
        or %cl,%al
        or %dil,%al
        ret
        .size u_cpp_815, .-u_cpp_815
        .globl u_cpp_816
        .type u_cpp_816, @function
u_cpp_816:
        test %esi,%esi
        setne %al
        or %dil,%al
        ret
        .size u_cpp_816, .-u_cpp_816
        .globl u_cpp_817
        .type u_cpp_817, @function
u_cpp_817:
        test %rsi,%rsi
        setne %al
        or %dil,%al
        ret
        .size u_cpp_817, .-u_cpp_817
        .globl u_cpp_818
        .type u_cpp_818, @function
u_cpp_818:
        test %rsi,%rsi
        setne %al
        or %dil,%al
        ret
        .size u_cpp_818, .-u_cpp_818
        .globl u_cpp_819
        .type u_cpp_819, @function
u_cpp_819:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %cl
        setne %al
        or %cl,%al
        or %dil,%al
        ret
        .size u_cpp_819, .-u_cpp_819
        .globl u_cpp_820
        .type u_cpp_820, @function
u_cpp_820:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %cl
        setne %al
        or %cl,%al
        or %dil,%al
        ret
        .size u_cpp_820, .-u_cpp_820
        .globl u_cpp_821
        .type u_cpp_821, @function
u_cpp_821:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_cpp_821, .-u_cpp_821
        .globl u_cpp_822
        .type u_cpp_822, @function
u_cpp_822:
        test %edi,%edi
        setne %cl
        test %esi,%esi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_822, .-u_cpp_822
        .globl u_cpp_823
        .type u_cpp_823, @function
u_cpp_823:
        test %edi,%edi
        setne %cl
        test %rsi,%rsi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_823, .-u_cpp_823
        .globl u_cpp_824
        .type u_cpp_824, @function
u_cpp_824:
        test %edi,%edi
        setne %cl
        test %rsi,%rsi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_824, .-u_cpp_824
        .globl u_cpp_825
        .type u_cpp_825, @function
u_cpp_825:
        test %edi,%edi
        setne %cl
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        and %cl,%al
        ret
        .size u_cpp_825, .-u_cpp_825
        .globl u_cpp_826
        .type u_cpp_826, @function
u_cpp_826:
        test %edi,%edi
        setne %cl
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        and %cl,%al
        ret
        .size u_cpp_826, .-u_cpp_826
        .globl u_cpp_827
        .type u_cpp_827, @function
u_cpp_827:
        test %edi,%edi
        setne %al
        and %sil,%al
        ret
        .size u_cpp_827, .-u_cpp_827
        .globl u_cpp_828
        .type u_cpp_828, @function
u_cpp_828:
        test %rdi,%rdi
        setne %cl
        test %esi,%esi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_828, .-u_cpp_828
        .globl u_cpp_829
        .type u_cpp_829, @function
u_cpp_829:
        test %rdi,%rdi
        setne %cl
        test %rsi,%rsi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_829, .-u_cpp_829
        .globl u_cpp_830
        .type u_cpp_830, @function
u_cpp_830:
        test %rdi,%rdi
        setne %cl
        test %rsi,%rsi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_830, .-u_cpp_830
        .globl u_cpp_831
        .type u_cpp_831, @function
u_cpp_831:
        test %rdi,%rdi
        setne %cl
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        and %cl,%al
        ret
        .size u_cpp_831, .-u_cpp_831
        .globl u_cpp_832
        .type u_cpp_832, @function
u_cpp_832:
        test %rdi,%rdi
        setne %cl
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        and %cl,%al
        ret
        .size u_cpp_832, .-u_cpp_832
        .globl u_cpp_833
        .type u_cpp_833, @function
u_cpp_833:
        test %rdi,%rdi
        setne %al
        and %sil,%al
        ret
        .size u_cpp_833, .-u_cpp_833
        .globl u_cpp_834
        .type u_cpp_834, @function
u_cpp_834:
        test %rdi,%rdi
        setne %cl
        test %esi,%esi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_834, .-u_cpp_834
        .globl u_cpp_835
        .type u_cpp_835, @function
u_cpp_835:
        test %rdi,%rdi
        setne %cl
        test %rsi,%rsi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_835, .-u_cpp_835
        .globl u_cpp_836
        .type u_cpp_836, @function
u_cpp_836:
        test %rdi,%rdi
        setne %cl
        test %rsi,%rsi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_836, .-u_cpp_836
        .globl u_cpp_837
        .type u_cpp_837, @function
u_cpp_837:
        test %rdi,%rdi
        setne %cl
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        and %cl,%al
        ret
        .size u_cpp_837, .-u_cpp_837
        .globl u_cpp_838
        .type u_cpp_838, @function
u_cpp_838:
        test %rdi,%rdi
        setne %cl
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %dl
        setne %al
        or %dl,%al
        and %cl,%al
        ret
        .size u_cpp_838, .-u_cpp_838
        .globl u_cpp_839
        .type u_cpp_839, @function
u_cpp_839:
        test %rdi,%rdi
        setne %al
        and %sil,%al
        ret
        .size u_cpp_839, .-u_cpp_839
        .globl u_cpp_840
        .type u_cpp_840, @function
u_cpp_840:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %edi,%edi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_840, .-u_cpp_840
        .globl u_cpp_841
        .type u_cpp_841, @function
u_cpp_841:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %rdi,%rdi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_841, .-u_cpp_841
        .globl u_cpp_842
        .type u_cpp_842, @function
u_cpp_842:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %rdi,%rdi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_842, .-u_cpp_842
        .globl u_cpp_843
        .type u_cpp_843, @function
u_cpp_843:
        xorps %xmm2,%xmm2
        cmpneqss %xmm2,%xmm1
        cmpneqss %xmm2,%xmm0
        andps %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%al
        ret
        .size u_cpp_843, .-u_cpp_843
        .globl u_cpp_844
        .type u_cpp_844, @function
u_cpp_844:
        xorps %xmm2,%xmm2
        ucomiss %xmm2,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        xorps %xmm0,%xmm0
        ucomisd %xmm0,%xmm1
        setp %dl
        setne %al
        or %dl,%al
        and %cl,%al
        ret
        .size u_cpp_844, .-u_cpp_844
        .globl u_cpp_845
        .type u_cpp_845, @function
u_cpp_845:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %cl
        setne %al
        or %cl,%al
        and %dil,%al
        ret
        .size u_cpp_845, .-u_cpp_845
        .globl u_cpp_846
        .type u_cpp_846, @function
u_cpp_846:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %edi,%edi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_846, .-u_cpp_846
        .globl u_cpp_847
        .type u_cpp_847, @function
u_cpp_847:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %rdi,%rdi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_847, .-u_cpp_847
        .globl u_cpp_848
        .type u_cpp_848, @function
u_cpp_848:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        test %rdi,%rdi
        setne %al
        and %cl,%al
        ret
        .size u_cpp_848, .-u_cpp_848
        .globl u_cpp_849
        .type u_cpp_849, @function
u_cpp_849:
        xorpd %xmm2,%xmm2
        ucomisd %xmm2,%xmm0
        setp %al
        setne %cl
        or %al,%cl
        xorpd %xmm0,%xmm0
        ucomiss %xmm0,%xmm1
        setp %dl
        setne %al
        or %dl,%al
        and %cl,%al
        ret
        .size u_cpp_849, .-u_cpp_849
        .globl u_cpp_850
        .type u_cpp_850, @function
u_cpp_850:
        xorpd %xmm2,%xmm2
        cmpneqsd %xmm2,%xmm1
        cmpneqsd %xmm2,%xmm0
        andpd %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%al
        ret
        .size u_cpp_850, .-u_cpp_850
        .globl u_cpp_851
        .type u_cpp_851, @function
u_cpp_851:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %cl
        setne %al
        or %cl,%al
        and %dil,%al
        ret
        .size u_cpp_851, .-u_cpp_851
        .globl u_cpp_852
        .type u_cpp_852, @function
u_cpp_852:
        test %esi,%esi
        setne %al
        and %dil,%al
        ret
        .size u_cpp_852, .-u_cpp_852
        .globl u_cpp_853
        .type u_cpp_853, @function
u_cpp_853:
        test %rsi,%rsi
        setne %al
        and %dil,%al
        ret
        .size u_cpp_853, .-u_cpp_853
        .globl u_cpp_854
        .type u_cpp_854, @function
u_cpp_854:
        test %rsi,%rsi
        setne %al
        and %dil,%al
        ret
        .size u_cpp_854, .-u_cpp_854
        .globl u_cpp_855
        .type u_cpp_855, @function
u_cpp_855:
        xorps %xmm1,%xmm1
        ucomiss %xmm1,%xmm0
        setp %cl
        setne %al
        or %cl,%al
        and %dil,%al
        ret
        .size u_cpp_855, .-u_cpp_855
        .globl u_cpp_856
        .type u_cpp_856, @function
u_cpp_856:
        xorpd %xmm1,%xmm1
        ucomisd %xmm1,%xmm0
        setp %cl
        setne %al
        or %cl,%al
        and %dil,%al
        ret
        .size u_cpp_856, .-u_cpp_856
        .globl u_cpp_857
        .type u_cpp_857, @function
u_cpp_857:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_cpp_857, .-u_cpp_857
        .globl u_cpp_858
        .type u_cpp_858, @function
u_cpp_858:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_cpp_858, .-u_cpp_858
        .globl u_cpp_859
        .type u_cpp_859, @function
u_cpp_859:
        movslq %edi,%rax
        or %rsi,%rax
        ret
        .size u_cpp_859, .-u_cpp_859
        .globl u_cpp_860
        .type u_cpp_860, @function
u_cpp_860:
        movslq %edi,%rax
        or %rsi,%rax
        ret
        .size u_cpp_860, .-u_cpp_860
        .globl u_cpp_863
        .type u_cpp_863, @function
u_cpp_863:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_cpp_863, .-u_cpp_863
        .globl u_cpp_864
        .type u_cpp_864, @function
u_cpp_864:
        movslq %esi,%rax
        or %rdi,%rax
        ret
        .size u_cpp_864, .-u_cpp_864
        .globl u_cpp_865
        .type u_cpp_865, @function
u_cpp_865:
        mov %rdi,%rax
        or %rsi,%rax
        ret
        .size u_cpp_865, .-u_cpp_865
        .globl u_cpp_866
        .type u_cpp_866, @function
u_cpp_866:
        mov %rdi,%rax
        or %rsi,%rax
        ret
        .size u_cpp_866, .-u_cpp_866
        .globl u_cpp_869
        .type u_cpp_869, @function
u_cpp_869:
        mov %esi,%eax
        or %rdi,%rax
        ret
        .size u_cpp_869, .-u_cpp_869
        .globl u_cpp_870
        .type u_cpp_870, @function
u_cpp_870:
        movslq %esi,%rax
        or %rdi,%rax
        ret
        .size u_cpp_870, .-u_cpp_870
        .globl u_cpp_871
        .type u_cpp_871, @function
u_cpp_871:
        mov %rdi,%rax
        or %rsi,%rax
        ret
        .size u_cpp_871, .-u_cpp_871
        .globl u_cpp_872
        .type u_cpp_872, @function
u_cpp_872:
        mov %rdi,%rax
        or %rsi,%rax
        ret
        .size u_cpp_872, .-u_cpp_872
        .globl u_cpp_875
        .type u_cpp_875, @function
u_cpp_875:
        mov %esi,%eax
        or %rdi,%rax
        ret
        .size u_cpp_875, .-u_cpp_875
        .globl u_cpp_888
        .type u_cpp_888, @function
u_cpp_888:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_cpp_888, .-u_cpp_888
        .globl u_cpp_889
        .type u_cpp_889, @function
u_cpp_889:
        mov %edi,%eax
        or %rsi,%rax
        ret
        .size u_cpp_889, .-u_cpp_889
        .globl u_cpp_890
        .type u_cpp_890, @function
u_cpp_890:
        mov %edi,%eax
        or %rsi,%rax
        ret
        .size u_cpp_890, .-u_cpp_890
        .globl u_cpp_893
        .type u_cpp_893, @function
u_cpp_893:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_cpp_893, .-u_cpp_893
        .globl u_cpp_894
        .type u_cpp_894, @function
u_cpp_894:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_cpp_894, .-u_cpp_894
        .globl u_cpp_895
        .type u_cpp_895, @function
u_cpp_895:
        movslq %edi,%rax
        xor %rsi,%rax
        ret
        .size u_cpp_895, .-u_cpp_895
        .globl u_cpp_896
        .type u_cpp_896, @function
u_cpp_896:
        movslq %edi,%rax
        xor %rsi,%rax
        ret
        .size u_cpp_896, .-u_cpp_896
        .globl u_cpp_899
        .type u_cpp_899, @function
u_cpp_899:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_cpp_899, .-u_cpp_899
        .globl u_cpp_900
        .type u_cpp_900, @function
u_cpp_900:
        movslq %esi,%rax
        xor %rdi,%rax
        ret
        .size u_cpp_900, .-u_cpp_900
        .globl u_cpp_901
        .type u_cpp_901, @function
u_cpp_901:
        mov %rdi,%rax
        xor %rsi,%rax
        ret
        .size u_cpp_901, .-u_cpp_901
        .globl u_cpp_902
        .type u_cpp_902, @function
u_cpp_902:
        mov %rdi,%rax
        xor %rsi,%rax
        ret
        .size u_cpp_902, .-u_cpp_902
        .globl u_cpp_905
        .type u_cpp_905, @function
u_cpp_905:
        mov %esi,%eax
        xor %rdi,%rax
        ret
        .size u_cpp_905, .-u_cpp_905
        .globl u_cpp_906
        .type u_cpp_906, @function
u_cpp_906:
        movslq %esi,%rax
        xor %rdi,%rax
        ret
        .size u_cpp_906, .-u_cpp_906
        .globl u_cpp_907
        .type u_cpp_907, @function
u_cpp_907:
        mov %rdi,%rax
        xor %rsi,%rax
        ret
        .size u_cpp_907, .-u_cpp_907
        .globl u_cpp_908
        .type u_cpp_908, @function
u_cpp_908:
        mov %rdi,%rax
        xor %rsi,%rax
        ret
        .size u_cpp_908, .-u_cpp_908
        .globl u_cpp_911
        .type u_cpp_911, @function
u_cpp_911:
        mov %esi,%eax
        xor %rdi,%rax
        ret
        .size u_cpp_911, .-u_cpp_911
        .globl u_cpp_924
        .type u_cpp_924, @function
u_cpp_924:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_cpp_924, .-u_cpp_924
        .globl u_cpp_925
        .type u_cpp_925, @function
u_cpp_925:
        mov %edi,%eax
        xor %rsi,%rax
        ret
        .size u_cpp_925, .-u_cpp_925
        .globl u_cpp_926
        .type u_cpp_926, @function
u_cpp_926:
        mov %edi,%eax
        xor %rsi,%rax
        ret
        .size u_cpp_926, .-u_cpp_926
        .globl u_cpp_929
        .type u_cpp_929, @function
u_cpp_929:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_cpp_929, .-u_cpp_929
        .globl u_cpp_930
        .type u_cpp_930, @function
u_cpp_930:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_cpp_930, .-u_cpp_930
        .globl u_cpp_931
        .type u_cpp_931, @function
u_cpp_931:
        movslq %edi,%rax
        and %rsi,%rax
        ret
        .size u_cpp_931, .-u_cpp_931
        .globl u_cpp_932
        .type u_cpp_932, @function
u_cpp_932:
        movslq %edi,%rax
        and %rsi,%rax
        ret
        .size u_cpp_932, .-u_cpp_932
        .globl u_cpp_935
        .type u_cpp_935, @function
u_cpp_935:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_cpp_935, .-u_cpp_935
        .globl u_cpp_936
        .type u_cpp_936, @function
u_cpp_936:
        movslq %esi,%rax
        and %rdi,%rax
        ret
        .size u_cpp_936, .-u_cpp_936
        .globl u_cpp_937
        .type u_cpp_937, @function
u_cpp_937:
        mov %rdi,%rax
        and %rsi,%rax
        ret
        .size u_cpp_937, .-u_cpp_937
        .globl u_cpp_938
        .type u_cpp_938, @function
u_cpp_938:
        mov %rdi,%rax
        and %rsi,%rax
        ret
        .size u_cpp_938, .-u_cpp_938
        .globl u_cpp_941
        .type u_cpp_941, @function
u_cpp_941:
        mov %rdi,%rax
        and %esi,%eax
        ret
        .size u_cpp_941, .-u_cpp_941
        .globl u_cpp_942
        .type u_cpp_942, @function
u_cpp_942:
        movslq %esi,%rax
        and %rdi,%rax
        ret
        .size u_cpp_942, .-u_cpp_942
        .globl u_cpp_943
        .type u_cpp_943, @function
u_cpp_943:
        mov %rdi,%rax
        and %rsi,%rax
        ret
        .size u_cpp_943, .-u_cpp_943
        .globl u_cpp_944
        .type u_cpp_944, @function
u_cpp_944:
        mov %rdi,%rax
        and %rsi,%rax
        ret
        .size u_cpp_944, .-u_cpp_944
        .globl u_cpp_947
        .type u_cpp_947, @function
u_cpp_947:
        mov %rdi,%rax
        and %esi,%eax
        ret
        .size u_cpp_947, .-u_cpp_947
        .globl u_cpp_960
        .type u_cpp_960, @function
u_cpp_960:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_cpp_960, .-u_cpp_960
        .globl u_cpp_961
        .type u_cpp_961, @function
u_cpp_961:
        mov %rsi,%rax
        and %edi,%eax
        ret
        .size u_cpp_961, .-u_cpp_961
        .globl u_cpp_962
        .type u_cpp_962, @function
u_cpp_962:
        mov %rsi,%rax
        and %edi,%eax
        ret
        .size u_cpp_962, .-u_cpp_962
        .globl u_cpp_965
        .type u_cpp_965, @function
u_cpp_965:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_cpp_965, .-u_cpp_965
        .globl u_cpp_966
        .type u_cpp_966, @function
u_cpp_966:
        cmp %esi,%edi
        setne %al
        ret
        .size u_cpp_966, .-u_cpp_966
        .globl u_cpp_967
        .type u_cpp_967, @function
u_cpp_967:
        movslq %edi,%rax
        cmp %rax,%rsi
        setne %al
        ret
        .size u_cpp_967, .-u_cpp_967
        .globl u_cpp_968
        .type u_cpp_968, @function
u_cpp_968:
        movslq %edi,%rax
        cmp %rax,%rsi
        setne %al
        ret
        .size u_cpp_968, .-u_cpp_968
        .globl u_cpp_969
        .type u_cpp_969, @function
u_cpp_969:
        cvtsi2ss %edi,%xmm1
        cmpneqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_969, .-u_cpp_969
        .globl u_cpp_970
        .type u_cpp_970, @function
u_cpp_970:
        cvtsi2sd %edi,%xmm1
        cmpneqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_970, .-u_cpp_970
        .globl u_cpp_971
        .type u_cpp_971, @function
u_cpp_971:
        cmp %esi,%edi
        setne %al
        ret
        .size u_cpp_971, .-u_cpp_971
        .globl u_cpp_972
        .type u_cpp_972, @function
u_cpp_972:
        movslq %esi,%rax
        cmp %rax,%rdi
        setne %al
        ret
        .size u_cpp_972, .-u_cpp_972
        .globl u_cpp_973
        .type u_cpp_973, @function
u_cpp_973:
        cmp %rsi,%rdi
        setne %al
        ret
        .size u_cpp_973, .-u_cpp_973
        .globl u_cpp_974
        .type u_cpp_974, @function
u_cpp_974:
        cmp %rsi,%rdi
        setne %al
        ret
        .size u_cpp_974, .-u_cpp_974
        .globl u_cpp_975
        .type u_cpp_975, @function
u_cpp_975:
        cvtsi2ss %rdi,%xmm1
        cmpneqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_975, .-u_cpp_975
        .globl u_cpp_976
        .type u_cpp_976, @function
u_cpp_976:
        cvtsi2sd %rdi,%xmm1
        cmpneqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_976, .-u_cpp_976
        .globl u_cpp_977
        .type u_cpp_977, @function
u_cpp_977:
        mov %esi,%eax
        cmp %rax,%rdi
        setne %al
        ret
        .size u_cpp_977, .-u_cpp_977
        .globl u_cpp_978
        .type u_cpp_978, @function
u_cpp_978:
        movslq %esi,%rax
        cmp %rax,%rdi
        setne %al
        ret
        .size u_cpp_978, .-u_cpp_978
        .globl u_cpp_979
        .type u_cpp_979, @function
u_cpp_979:
        cmp %rsi,%rdi
        setne %al
        ret
        .size u_cpp_979, .-u_cpp_979
        .globl u_cpp_980
        .type u_cpp_980, @function
u_cpp_980:
        cmp %rsi,%rdi
        setne %al
        ret
        .size u_cpp_980, .-u_cpp_980
        .globl u_cpp_983
        .type u_cpp_983, @function
u_cpp_983:
        mov %esi,%eax
        cmp %rax,%rdi
        setne %al
        ret
        .size u_cpp_983, .-u_cpp_983
        .globl u_cpp_984
        .type u_cpp_984, @function
u_cpp_984:
        cvtsi2ss %edi,%xmm1
        cmpneqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_984, .-u_cpp_984
        .globl u_cpp_985
        .type u_cpp_985, @function
u_cpp_985:
        cvtsi2ss %rdi,%xmm1
        cmpneqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_985, .-u_cpp_985
        .globl u_cpp_987
        .type u_cpp_987, @function
u_cpp_987:
        cmpneqss %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%eax
        ret
        .size u_cpp_987, .-u_cpp_987
        .globl u_cpp_988
        .type u_cpp_988, @function
u_cpp_988:
        cvtss2sd %xmm0,%xmm2
        cmpneqsd %xmm1,%xmm2
        movq %xmm2,%rax
        and $0x1,%eax
        ret
        .size u_cpp_988, .-u_cpp_988
        .globl u_cpp_989
        .type u_cpp_989, @function
u_cpp_989:
        cvtsi2ss %edi,%xmm1
        cmpneqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_989, .-u_cpp_989
        .globl u_cpp_990
        .type u_cpp_990, @function
u_cpp_990:
        cvtsi2sd %edi,%xmm1
        cmpneqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_990, .-u_cpp_990
        .globl u_cpp_991
        .type u_cpp_991, @function
u_cpp_991:
        cvtsi2sd %rdi,%xmm1
        cmpneqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_991, .-u_cpp_991
        .globl u_cpp_993
        .type u_cpp_993, @function
u_cpp_993:
        cvtss2sd %xmm1,%xmm2
        cmpneqsd %xmm0,%xmm2
        movq %xmm2,%rax
        and $0x1,%eax
        ret
        .size u_cpp_993, .-u_cpp_993
        .globl u_cpp_994
        .type u_cpp_994, @function
u_cpp_994:
        cmpneqsd %xmm1,%xmm0
        movq %xmm0,%rax
        and $0x1,%eax
        ret
        .size u_cpp_994, .-u_cpp_994
        .globl u_cpp_995
        .type u_cpp_995, @function
u_cpp_995:
        cvtsi2sd %edi,%xmm1
        cmpneqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_995, .-u_cpp_995
        .globl u_cpp_996
        .type u_cpp_996, @function
u_cpp_996:
        cmp %edi,%esi
        setne %al
        ret
        .size u_cpp_996, .-u_cpp_996
        .globl u_cpp_997
        .type u_cpp_997, @function
u_cpp_997:
        mov %edi,%eax
        cmp %rax,%rsi
        setne %al
        ret
        .size u_cpp_997, .-u_cpp_997
        .globl u_cpp_998
        .type u_cpp_998, @function
u_cpp_998:
        mov %edi,%eax
        cmp %rax,%rsi
        setne %al
        ret
        .size u_cpp_998, .-u_cpp_998
        .globl u_cpp_999
        .type u_cpp_999, @function
u_cpp_999:
        cvtsi2ss %edi,%xmm1
        cmpneqss %xmm0,%xmm1
        movd %xmm1,%eax
        and $0x1,%eax
        ret
        .size u_cpp_999, .-u_cpp_999
        .globl u_cpp_1000
        .type u_cpp_1000, @function
u_cpp_1000:
        cvtsi2sd %edi,%xmm1
        cmpneqsd %xmm0,%xmm1
        movq %xmm1,%rax
        and $0x1,%eax
        ret
        .size u_cpp_1000, .-u_cpp_1000
        .globl u_cpp_1001
        .type u_cpp_1001, @function
u_cpp_1001:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_cpp_1001, .-u_cpp_1001
        .globl u_go_0
        .type u_go_0, @function
u_go_0:
        ret
        .size u_go_0, .-u_go_0
        .globl u_go_1
        .type u_go_1, @function
u_go_1:
        ret
        .size u_go_1, .-u_go_1
        .globl u_go_2
        .type u_go_2, @function
u_go_2:
        ret
        .size u_go_2, .-u_go_2
        .globl u_go_3
        .type u_go_3, @function
u_go_3:
        ret
        .size u_go_3, .-u_go_3
        .globl u_go_4
        .type u_go_4, @function
u_go_4:
        ret
        .size u_go_4, .-u_go_4
        .globl u_go_81
        .type u_go_81, @function
u_go_81:
        mulss %xmm1,%xmm0
        ret
        .size u_go_81, .-u_go_81
        .globl u_go_88
        .type u_go_88, @function
u_go_88:
        mulsd %xmm1,%xmm0
        ret
        .size u_go_88, .-u_go_88
        .globl u_go_117
        .type u_go_117, @function
u_go_117:
        divss %xmm1,%xmm0
        ret
        .size u_go_117, .-u_go_117
        .globl u_go_124
        .type u_go_124, @function
u_go_124:
        divsd %xmm1,%xmm0
        ret
        .size u_go_124, .-u_go_124
        .globl u_go_333
        .type u_go_333, @function
u_go_333:
        addss %xmm1,%xmm0
        ret
        .size u_go_333, .-u_go_333
        .globl u_go_340
        .type u_go_340, @function
u_go_340:
        addsd %xmm1,%xmm0
        ret
        .size u_go_340, .-u_go_340
        .globl u_go_369
        .type u_go_369, @function
u_go_369:
        subss %xmm1,%xmm0
        ret
        .size u_go_369, .-u_go_369
        .globl u_go_376
        .type u_go_376, @function
u_go_376:
        subsd %xmm1,%xmm0
        ret
        .size u_go_376, .-u_go_376
        .globl u_go_456
        .type u_go_456, @function
u_go_456:
        cmp %edi,%esi
        sete %al
        ret
        .size u_go_456, .-u_go_456
        .globl u_go_463
        .type u_go_463, @function
u_go_463:
        cmp %rdi,%rsi
        sete %al
        ret
        .size u_go_463, .-u_go_463
        .globl u_go_470
        .type u_go_470, @function
u_go_470:
        cmp %rdi,%rsi
        sete %al
        ret
        .size u_go_470, .-u_go_470
        .globl u_go_477
        .type u_go_477, @function
u_go_477:
        ucomiss %xmm1,%xmm0
        sete %al
        setnp %cl
        and %ecx,%eax
        ret
        .size u_go_477, .-u_go_477
        .globl u_go_484
        .type u_go_484, @function
u_go_484:
        ucomisd %xmm1,%xmm0
        sete %al
        setnp %cl
        and %ecx,%eax
        ret
        .size u_go_484, .-u_go_484
        .globl u_go_491
        .type u_go_491, @function
u_go_491:
        cmp %dil,%sil
        sete %al
        ret
        .size u_go_491, .-u_go_491
        .globl u_go_492
        .type u_go_492, @function
u_go_492:
        cmp %edi,%esi
        setne %al
        ret
        .size u_go_492, .-u_go_492
        .globl u_go_499
        .type u_go_499, @function
u_go_499:
        cmp %rdi,%rsi
        setne %al
        ret
        .size u_go_499, .-u_go_499
        .globl u_go_506
        .type u_go_506, @function
u_go_506:
        cmp %rdi,%rsi
        setne %al
        ret
        .size u_go_506, .-u_go_506
        .globl u_go_513
        .type u_go_513, @function
u_go_513:
        ucomiss %xmm1,%xmm0
        setne %al
        setp %cl
        or %ecx,%eax
        ret
        .size u_go_513, .-u_go_513
        .globl u_go_520
        .type u_go_520, @function
u_go_520:
        ucomisd %xmm1,%xmm0
        setne %al
        setp %cl
        or %ecx,%eax
        ret
        .size u_go_520, .-u_go_520
        .globl u_go_527
        .type u_go_527, @function
u_go_527:
        cmp %dil,%sil
        setne %al
        ret
        .size u_go_527, .-u_go_527
        .globl u_go_528
        .type u_go_528, @function
u_go_528:
        cmp %edi,%esi
        setg %al
        ret
        .size u_go_528, .-u_go_528
        .globl u_go_535
        .type u_go_535, @function
u_go_535:
        cmp %rdi,%rsi
        setg %al
        ret
        .size u_go_535, .-u_go_535
        .globl u_go_542
        .type u_go_542, @function
u_go_542:
        cmp %rdi,%rsi
        seta %al
        ret
        .size u_go_542, .-u_go_542
        .globl u_go_549
        .type u_go_549, @function
u_go_549:
        ucomiss %xmm0,%xmm1
        seta %al
        ret
        .size u_go_549, .-u_go_549
        .globl u_go_556
        .type u_go_556, @function
u_go_556:
        ucomisd %xmm0,%xmm1
        seta %al
        ret
        .size u_go_556, .-u_go_556
        .globl u_go_564
        .type u_go_564, @function
u_go_564:
        cmp %edi,%esi
        setge %al
        ret
        .size u_go_564, .-u_go_564
        .globl u_go_571
        .type u_go_571, @function
u_go_571:
        cmp %rdi,%rsi
        setge %al
        ret
        .size u_go_571, .-u_go_571
        .globl u_go_578
        .type u_go_578, @function
u_go_578:
        cmp %rdi,%rsi
        setae %al
        ret
        .size u_go_578, .-u_go_578
        .globl u_go_585
        .type u_go_585, @function
u_go_585:
        ucomiss %xmm0,%xmm1
        setae %al
        ret
        .size u_go_585, .-u_go_585
        .globl u_go_592
        .type u_go_592, @function
u_go_592:
        ucomisd %xmm0,%xmm1
        setae %al
        ret
        .size u_go_592, .-u_go_592
        .globl u_go_600
        .type u_go_600, @function
u_go_600:
        cmp %edi,%esi
        setl %al
        ret
        .size u_go_600, .-u_go_600
        .globl u_go_607
        .type u_go_607, @function
u_go_607:
        cmp %rdi,%rsi
        setl %al
        ret
        .size u_go_607, .-u_go_607
        .globl u_go_614
        .type u_go_614, @function
u_go_614:
        cmp %rdi,%rsi
        setb %al
        ret
        .size u_go_614, .-u_go_614
        .globl u_go_621
        .type u_go_621, @function
u_go_621:
        ucomiss %xmm1,%xmm0
        seta %al
        ret
        .size u_go_621, .-u_go_621
        .globl u_go_628
        .type u_go_628, @function
u_go_628:
        ucomisd %xmm1,%xmm0
        seta %al
        ret
        .size u_go_628, .-u_go_628
        .globl u_go_636
        .type u_go_636, @function
u_go_636:
        cmp %edi,%esi
        setle %al
        ret
        .size u_go_636, .-u_go_636
        .globl u_go_643
        .type u_go_643, @function
u_go_643:
        cmp %rdi,%rsi
        setle %al
        ret
        .size u_go_643, .-u_go_643
        .globl u_go_650
        .type u_go_650, @function
u_go_650:
        cmp %rdi,%rsi
        setbe %al
        ret
        .size u_go_650, .-u_go_650
        .globl u_go_657
        .type u_go_657, @function
u_go_657:
        ucomiss %xmm1,%xmm0
        setae %al
        ret
        .size u_go_657, .-u_go_657
        .globl u_go_664
        .type u_go_664, @function
u_go_664:
        ucomisd %xmm1,%xmm0
        setae %al
        ret
        .size u_go_664, .-u_go_664
        .globl u_rust_0
        .type u_rust_0, @function
u_rust_0:
        mov %edi,%eax
        neg %eax
        ret
        .size u_rust_0, .-u_rust_0
        .globl u_rust_1
        .type u_rust_1, @function
u_rust_1:
        mov %rdi,%rax
        neg %rax
        ret
        .size u_rust_1, .-u_rust_1
        .globl u_rust_12
        .type u_rust_12, @function
u_rust_12:
        mov %edi,%eax
        not %eax
        ret
        .size u_rust_12, .-u_rust_12
        .globl u_rust_13
        .type u_rust_13, @function
u_rust_13:
        mov %rdi,%rax
        not %rax
        ret
        .size u_rust_13, .-u_rust_13
        .globl u_rust_14
        .type u_rust_14, @function
u_rust_14:
        mov %rdi,%rax
        not %rax
        ret
        .size u_rust_14, .-u_rust_14
        .globl u_rust_17
        .type u_rust_17, @function
u_rust_17:
        mov %edi,%eax
        xor $0x1,%al
        ret
        .size u_rust_17, .-u_rust_17
        .globl u_rust_36
        .type u_rust_36, @function
u_rust_36:
        mov %edi,%eax
        ret
        .size u_rust_36, .-u_rust_36
        .globl u_rust_37
        .type u_rust_37, @function
u_rust_37:
        mov %rdi,%rax
        ret
        .size u_rust_37, .-u_rust_37
        .globl u_rust_38
        .type u_rust_38, @function
u_rust_38:
        mov %rdi,%rax
        ret
        .size u_rust_38, .-u_rust_38
        .globl u_rust_39
        .type u_rust_39, @function
u_rust_39:
        ret
        .size u_rust_39, .-u_rust_39
        .globl u_rust_40
        .type u_rust_40, @function
u_rust_40:
        ret
        .size u_rust_40, .-u_rust_40
        .globl u_rust_41
        .type u_rust_41, @function
u_rust_41:
        mov %edi,%eax
        ret
        .size u_rust_41, .-u_rust_41
        .globl u_rust_42
        .type u_rust_42, @function
u_rust_42:
        mov %edi,%eax
        ret
        .size u_rust_42, .-u_rust_42
        .globl u_rust_43
        .type u_rust_43, @function
u_rust_43:
        mov %rdi,%rax
        ret
        .size u_rust_43, .-u_rust_43
        .globl u_rust_44
        .type u_rust_44, @function
u_rust_44:
        mov %rdi,%rax
        ret
        .size u_rust_44, .-u_rust_44
        .globl u_rust_45
        .type u_rust_45, @function
u_rust_45:
        ret
        .size u_rust_45, .-u_rust_45
        .globl u_rust_46
        .type u_rust_46, @function
u_rust_46:
        ret
        .size u_rust_46, .-u_rust_46
        .globl u_rust_47
        .type u_rust_47, @function
u_rust_47:
        mov %edi,%eax
        ret
        .size u_rust_47, .-u_rust_47
        .globl u_rust_101
        .type u_rust_101, @function
u_rust_101:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_rust_101, .-u_rust_101
        .globl u_rust_137
        .type u_rust_137, @function
u_rust_137:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_rust_137, .-u_rust_137
        .globl u_rust_138
        .type u_rust_138, @function
u_rust_138:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_rust_138, .-u_rust_138
        .globl u_rust_145
        .type u_rust_145, @function
u_rust_145:
        mov %rdi,%rax
        and %rsi,%rax
        ret
        .size u_rust_145, .-u_rust_145
        .globl u_rust_152
        .type u_rust_152, @function
u_rust_152:
        mov %rdi,%rax
        and %rsi,%rax
        ret
        .size u_rust_152, .-u_rust_152
        .globl u_rust_173
        .type u_rust_173, @function
u_rust_173:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_rust_173, .-u_rust_173
        .globl u_rust_174
        .type u_rust_174, @function
u_rust_174:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_rust_174, .-u_rust_174
        .globl u_rust_181
        .type u_rust_181, @function
u_rust_181:
        mov %rdi,%rax
        or %rsi,%rax
        ret
        .size u_rust_181, .-u_rust_181
        .globl u_rust_188
        .type u_rust_188, @function
u_rust_188:
        mov %rdi,%rax
        or %rsi,%rax
        ret
        .size u_rust_188, .-u_rust_188
        .globl u_rust_209
        .type u_rust_209, @function
u_rust_209:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_rust_209, .-u_rust_209
        .globl u_rust_210
        .type u_rust_210, @function
u_rust_210:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_rust_210, .-u_rust_210
        .globl u_rust_217
        .type u_rust_217, @function
u_rust_217:
        mov %rdi,%rax
        xor %rsi,%rax
        ret
        .size u_rust_217, .-u_rust_217
        .globl u_rust_224
        .type u_rust_224, @function
u_rust_224:
        mov %rdi,%rax
        xor %rsi,%rax
        ret
        .size u_rust_224, .-u_rust_224
        .globl u_rust_245
        .type u_rust_245, @function
u_rust_245:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_rust_245, .-u_rust_245
        .globl u_rust_246
        .type u_rust_246, @function
u_rust_246:
        cmp %esi,%edi
        sete %al
        ret
        .size u_rust_246, .-u_rust_246
        .globl u_rust_253
        .type u_rust_253, @function
u_rust_253:
        cmp %rsi,%rdi
        sete %al
        ret
        .size u_rust_253, .-u_rust_253
        .globl u_rust_260
        .type u_rust_260, @function
u_rust_260:
        cmp %rsi,%rdi
        sete %al
        ret
        .size u_rust_260, .-u_rust_260
        .globl u_rust_267
        .type u_rust_267, @function
u_rust_267:
        cmpeqss %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%eax
        ret
        .size u_rust_267, .-u_rust_267
        .globl u_rust_274
        .type u_rust_274, @function
u_rust_274:
        cmpeqsd %xmm1,%xmm0
        movq %xmm0,%rax
        and $0x1,%eax
        ret
        .size u_rust_274, .-u_rust_274
        .globl u_rust_281
        .type u_rust_281, @function
u_rust_281:
        mov %edi,%eax
        xor %esi,%eax
        xor $0x1,%al
        ret
        .size u_rust_281, .-u_rust_281
        .globl u_rust_282
        .type u_rust_282, @function
u_rust_282:
        cmp %esi,%edi
        setne %al
        ret
        .size u_rust_282, .-u_rust_282
        .globl u_rust_289
        .type u_rust_289, @function
u_rust_289:
        cmp %rsi,%rdi
        setne %al
        ret
        .size u_rust_289, .-u_rust_289
        .globl u_rust_296
        .type u_rust_296, @function
u_rust_296:
        cmp %rsi,%rdi
        setne %al
        ret
        .size u_rust_296, .-u_rust_296
        .globl u_rust_303
        .type u_rust_303, @function
u_rust_303:
        cmpneqss %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%eax
        ret
        .size u_rust_303, .-u_rust_303
        .globl u_rust_310
        .type u_rust_310, @function
u_rust_310:
        cmpneqsd %xmm1,%xmm0
        movq %xmm0,%rax
        and $0x1,%eax
        ret
        .size u_rust_310, .-u_rust_310
        .globl u_rust_317
        .type u_rust_317, @function
u_rust_317:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_rust_317, .-u_rust_317
        .globl u_rust_318
        .type u_rust_318, @function
u_rust_318:
        cmp %esi,%edi
        setl %al
        ret
        .size u_rust_318, .-u_rust_318
        .globl u_rust_325
        .type u_rust_325, @function
u_rust_325:
        cmp %rsi,%rdi
        setl %al
        ret
        .size u_rust_325, .-u_rust_325
        .globl u_rust_332
        .type u_rust_332, @function
u_rust_332:
        cmp %rsi,%rdi
        setb %al
        ret
        .size u_rust_332, .-u_rust_332
        .globl u_rust_339
        .type u_rust_339, @function
u_rust_339:
        ucomiss %xmm0,%xmm1
        seta %al
        ret
        .size u_rust_339, .-u_rust_339
        .globl u_rust_346
        .type u_rust_346, @function
u_rust_346:
        ucomisd %xmm0,%xmm1
        seta %al
        ret
        .size u_rust_346, .-u_rust_346
        .globl u_rust_353
        .type u_rust_353, @function
u_rust_353:
        mov %edi,%eax
        xor $0x1,%al
        and %sil,%al
        ret
        .size u_rust_353, .-u_rust_353
        .globl u_rust_354
        .type u_rust_354, @function
u_rust_354:
        cmp %esi,%edi
        setle %al
        ret
        .size u_rust_354, .-u_rust_354
        .globl u_rust_361
        .type u_rust_361, @function
u_rust_361:
        cmp %rsi,%rdi
        setle %al
        ret
        .size u_rust_361, .-u_rust_361
        .globl u_rust_368
        .type u_rust_368, @function
u_rust_368:
        cmp %rsi,%rdi
        setbe %al
        ret
        .size u_rust_368, .-u_rust_368
        .globl u_rust_375
        .type u_rust_375, @function
u_rust_375:
        ucomiss %xmm0,%xmm1
        setae %al
        ret
        .size u_rust_375, .-u_rust_375
        .globl u_rust_382
        .type u_rust_382, @function
u_rust_382:
        ucomisd %xmm0,%xmm1
        setae %al
        ret
        .size u_rust_382, .-u_rust_382
        .globl u_rust_389
        .type u_rust_389, @function
u_rust_389:
        mov %edi,%eax
        xor $0x1,%al
        or %sil,%al
        ret
        .size u_rust_389, .-u_rust_389
        .globl u_rust_390
        .type u_rust_390, @function
u_rust_390:
        cmp %esi,%edi
        setg %al
        ret
        .size u_rust_390, .-u_rust_390
        .globl u_rust_397
        .type u_rust_397, @function
u_rust_397:
        cmp %rsi,%rdi
        setg %al
        ret
        .size u_rust_397, .-u_rust_397
        .globl u_rust_404
        .type u_rust_404, @function
u_rust_404:
        cmp %rsi,%rdi
        seta %al
        ret
        .size u_rust_404, .-u_rust_404
        .globl u_rust_411
        .type u_rust_411, @function
u_rust_411:
        ucomiss %xmm1,%xmm0
        seta %al
        ret
        .size u_rust_411, .-u_rust_411
        .globl u_rust_418
        .type u_rust_418, @function
u_rust_418:
        ucomisd %xmm1,%xmm0
        seta %al
        ret
        .size u_rust_418, .-u_rust_418
        .globl u_rust_425
        .type u_rust_425, @function
u_rust_425:
        mov %esi,%eax
        xor $0x1,%al
        and %dil,%al
        ret
        .size u_rust_425, .-u_rust_425
        .globl u_rust_426
        .type u_rust_426, @function
u_rust_426:
        cmp %esi,%edi
        setge %al
        ret
        .size u_rust_426, .-u_rust_426
        .globl u_rust_433
        .type u_rust_433, @function
u_rust_433:
        cmp %rsi,%rdi
        setge %al
        ret
        .size u_rust_433, .-u_rust_433
        .globl u_rust_440
        .type u_rust_440, @function
u_rust_440:
        cmp %rsi,%rdi
        setae %al
        ret
        .size u_rust_440, .-u_rust_440
        .globl u_rust_447
        .type u_rust_447, @function
u_rust_447:
        ucomiss %xmm1,%xmm0
        setae %al
        ret
        .size u_rust_447, .-u_rust_447
        .globl u_rust_454
        .type u_rust_454, @function
u_rust_454:
        ucomisd %xmm1,%xmm0
        setae %al
        ret
        .size u_rust_454, .-u_rust_454
        .globl u_rust_461
        .type u_rust_461, @function
u_rust_461:
        mov %esi,%eax
        xor $0x1,%al
        or %dil,%al
        ret
        .size u_rust_461, .-u_rust_461
        .globl u_rust_462
        .type u_rust_462, @function
u_rust_462:
        mov %esi,%ecx
        mov %edi,%eax
        shl %cl,%eax
        ret
        .size u_rust_462, .-u_rust_462
        .globl u_rust_463
        .type u_rust_463, @function
u_rust_463:
        mov %rsi,%rcx
        mov %edi,%eax
        shl %cl,%eax
        ret
        .size u_rust_463, .-u_rust_463
        .globl u_rust_464
        .type u_rust_464, @function
u_rust_464:
        mov %rsi,%rcx
        mov %edi,%eax
        shl %cl,%eax
        ret
        .size u_rust_464, .-u_rust_464
        .globl u_rust_468
        .type u_rust_468, @function
u_rust_468:
        mov %esi,%ecx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_rust_468, .-u_rust_468
        .globl u_rust_469
        .type u_rust_469, @function
u_rust_469:
        mov %rsi,%rcx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_rust_469, .-u_rust_469
        .globl u_rust_470
        .type u_rust_470, @function
u_rust_470:
        mov %rsi,%rcx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_rust_470, .-u_rust_470
        .globl u_rust_474
        .type u_rust_474, @function
u_rust_474:
        mov %esi,%ecx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_rust_474, .-u_rust_474
        .globl u_rust_475
        .type u_rust_475, @function
u_rust_475:
        mov %rsi,%rcx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_rust_475, .-u_rust_475
        .globl u_rust_476
        .type u_rust_476, @function
u_rust_476:
        mov %rsi,%rcx
        mov %rdi,%rax
        shl %cl,%rax
        ret
        .size u_rust_476, .-u_rust_476
        .globl u_rust_498
        .type u_rust_498, @function
u_rust_498:
        mov %esi,%ecx
        mov %edi,%eax
        sar %cl,%eax
        ret
        .size u_rust_498, .-u_rust_498
        .globl u_rust_499
        .type u_rust_499, @function
u_rust_499:
        mov %rsi,%rcx
        mov %edi,%eax
        sar %cl,%eax
        ret
        .size u_rust_499, .-u_rust_499
        .globl u_rust_500
        .type u_rust_500, @function
u_rust_500:
        mov %rsi,%rcx
        mov %edi,%eax
        sar %cl,%eax
        ret
        .size u_rust_500, .-u_rust_500
        .globl u_rust_504
        .type u_rust_504, @function
u_rust_504:
        mov %esi,%ecx
        mov %rdi,%rax
        sar %cl,%rax
        ret
        .size u_rust_504, .-u_rust_504
        .globl u_rust_505
        .type u_rust_505, @function
u_rust_505:
        mov %rsi,%rcx
        mov %rdi,%rax
        sar %cl,%rax
        ret
        .size u_rust_505, .-u_rust_505
        .globl u_rust_506
        .type u_rust_506, @function
u_rust_506:
        mov %rsi,%rcx
        mov %rdi,%rax
        sar %cl,%rax
        ret
        .size u_rust_506, .-u_rust_506
        .globl u_rust_510
        .type u_rust_510, @function
u_rust_510:
        mov %esi,%ecx
        mov %rdi,%rax
        shr %cl,%rax
        ret
        .size u_rust_510, .-u_rust_510
        .globl u_rust_511
        .type u_rust_511, @function
u_rust_511:
        mov %rsi,%rcx
        mov %rdi,%rax
        shr %cl,%rax
        ret
        .size u_rust_511, .-u_rust_511
        .globl u_rust_512
        .type u_rust_512, @function
u_rust_512:
        mov %rsi,%rcx
        mov %rdi,%rax
        shr %cl,%rax
        ret
        .size u_rust_512, .-u_rust_512
        .globl u_rust_534
        .type u_rust_534, @function
u_rust_534:
        lea (%rdi,%rsi,1),%eax
        ret
        .size u_rust_534, .-u_rust_534
        .globl u_rust_541
        .type u_rust_541, @function
u_rust_541:
        lea (%rdi,%rsi,1),%rax
        ret
        .size u_rust_541, .-u_rust_541
        .globl u_rust_548
        .type u_rust_548, @function
u_rust_548:
        lea (%rdi,%rsi,1),%rax
        ret
        .size u_rust_548, .-u_rust_548
        .globl u_rust_555
        .type u_rust_555, @function
u_rust_555:
        addss %xmm1,%xmm0
        ret
        .size u_rust_555, .-u_rust_555
        .globl u_rust_562
        .type u_rust_562, @function
u_rust_562:
        addsd %xmm1,%xmm0
        ret
        .size u_rust_562, .-u_rust_562
        .globl u_rust_570
        .type u_rust_570, @function
u_rust_570:
        mov %edi,%eax
        sub %esi,%eax
        ret
        .size u_rust_570, .-u_rust_570
        .globl u_rust_577
        .type u_rust_577, @function
u_rust_577:
        mov %rdi,%rax
        sub %rsi,%rax
        ret
        .size u_rust_577, .-u_rust_577
        .globl u_rust_584
        .type u_rust_584, @function
u_rust_584:
        mov %rdi,%rax
        sub %rsi,%rax
        ret
        .size u_rust_584, .-u_rust_584
        .globl u_rust_591
        .type u_rust_591, @function
u_rust_591:
        subss %xmm1,%xmm0
        ret
        .size u_rust_591, .-u_rust_591
        .globl u_rust_598
        .type u_rust_598, @function
u_rust_598:
        subsd %xmm1,%xmm0
        ret
        .size u_rust_598, .-u_rust_598
        .globl u_rust_606
        .type u_rust_606, @function
u_rust_606:
        mov %edi,%eax
        imul %esi,%eax
        ret
        .size u_rust_606, .-u_rust_606
        .globl u_rust_613
        .type u_rust_613, @function
u_rust_613:
        mov %rdi,%rax
        imul %rsi,%rax
        ret
        .size u_rust_613, .-u_rust_613
        .globl u_rust_620
        .type u_rust_620, @function
u_rust_620:
        mov %rdi,%rax
        imul %rsi,%rax
        ret
        .size u_rust_620, .-u_rust_620
        .globl u_rust_627
        .type u_rust_627, @function
u_rust_627:
        mulss %xmm1,%xmm0
        ret
        .size u_rust_627, .-u_rust_627
        .globl u_rust_634
        .type u_rust_634, @function
u_rust_634:
        mulsd %xmm1,%xmm0
        ret
        .size u_rust_634, .-u_rust_634
        .globl u_rust_663
        .type u_rust_663, @function
u_rust_663:
        divss %xmm1,%xmm0
        ret
        .size u_rust_663, .-u_rust_663
        .globl u_rust_670
        .type u_rust_670, @function
u_rust_670:
        divsd %xmm1,%xmm0
        ret
        .size u_rust_670, .-u_rust_670
        .globl u_rust_714
        .type u_rust_714, @function
u_rust_714:
        mov %esi,%edx
        mov %edi,%eax
        ret
        .size u_rust_714, .-u_rust_714
        .globl u_rust_721
        .type u_rust_721, @function
u_rust_721:
        mov %rsi,%rdx
        mov %rdi,%rax
        ret
        .size u_rust_721, .-u_rust_721
        .globl u_rust_728
        .type u_rust_728, @function
u_rust_728:
        mov %rsi,%rdx
        mov %rdi,%rax
        ret
        .size u_rust_728, .-u_rust_728
        .globl u_rust_735
        .type u_rust_735, @function
u_rust_735:
        ret
        .size u_rust_735, .-u_rust_735
        .globl u_rust_742
        .type u_rust_742, @function
u_rust_742:
        ret
        .size u_rust_742, .-u_rust_742
        .globl u_rust_749
        .type u_rust_749, @function
u_rust_749:
        mov %esi,%edx
        mov %edi,%eax
        ret
        .size u_rust_749, .-u_rust_749
        .globl u_rust_786
        .type u_rust_786, @function
u_rust_786:
        mov %rdi,%rax
        mov %esi,(%rdi)
        mov %edx,0x4(%rdi)
        movb $0x0,0x8(%rdi)
        ret
        .size u_rust_786, .-u_rust_786
        .globl u_rust_793
        .type u_rust_793, @function
u_rust_793:
        mov %rdi,%rax
        mov %rsi,(%rdi)
        mov %rdx,0x8(%rdi)
        movb $0x0,0x10(%rdi)
        ret
        .size u_rust_793, .-u_rust_793
        .globl u_rust_800
        .type u_rust_800, @function
u_rust_800:
        mov %rdi,%rax
        mov %rsi,(%rdi)
        mov %rdx,0x8(%rdi)
        movb $0x0,0x10(%rdi)
        ret
        .size u_rust_800, .-u_rust_800
        .globl u_rust_807
        .type u_rust_807, @function
u_rust_807:
        mov %rdi,%rax
        movss %xmm0,(%rdi)
        movss %xmm1,0x4(%rdi)
        movb $0x0,0x8(%rdi)
        ret
        .size u_rust_807, .-u_rust_807
        .globl u_rust_814
        .type u_rust_814, @function
u_rust_814:
        mov %rdi,%rax
        movsd %xmm0,(%rdi)
        movsd %xmm1,0x8(%rdi)
        movb $0x0,0x10(%rdi)
        ret
        .size u_rust_814, .-u_rust_814
        .globl u_rust_821
        .type u_rust_821, @function
u_rust_821:
        shl $0x8,%esi
        lea (%rsi,%rdi,1),%eax
        ret
        .size u_rust_821, .-u_rust_821
        .globl u_swift_18
        .type u_swift_18, @function
u_swift_18:
        mov %edi,%eax
        ret
        .size u_swift_18, .-u_swift_18
        .globl u_swift_19
        .type u_swift_19, @function
u_swift_19:
        mov %rdi,%rax
        ret
        .size u_swift_19, .-u_swift_19
        .globl u_swift_20
        .type u_swift_20, @function
u_swift_20:
        mov %rdi,%rax
        ret
        .size u_swift_20, .-u_swift_20
        .globl u_swift_21
        .type u_swift_21, @function
u_swift_21:
        ret
        .size u_swift_21, .-u_swift_21
        .globl u_swift_22
        .type u_swift_22, @function
u_swift_22:
        ret
        .size u_swift_22, .-u_swift_22
        .globl u_swift_29
        .type u_swift_29, @function
u_swift_29:
        mov %edi,%eax
        xor $0x1,%al
        ret
        .size u_swift_29, .-u_swift_29
        .globl u_swift_36
        .type u_swift_36, @function
u_swift_36:
        mov %edi,%eax
        not %eax
        ret
        .size u_swift_36, .-u_swift_36
        .globl u_swift_37
        .type u_swift_37, @function
u_swift_37:
        mov %rdi,%rax
        not %rax
        ret
        .size u_swift_37, .-u_swift_37
        .globl u_swift_38
        .type u_swift_38, @function
u_swift_38:
        mov %rdi,%rax
        not %rax
        ret
        .size u_swift_38, .-u_swift_38
        .globl u_swift_42
        .type u_swift_42, @function
u_swift_42:
        mov %edi,%eax
        ret
        .size u_swift_42, .-u_swift_42
        .globl u_swift_43
        .type u_swift_43, @function
u_swift_43:
        mov %rdi,%rax
        ret
        .size u_swift_43, .-u_swift_43
        .globl u_swift_44
        .type u_swift_44, @function
u_swift_44:
        mov %rdi,%rax
        ret
        .size u_swift_44, .-u_swift_44
        .globl u_swift_45
        .type u_swift_45, @function
u_swift_45:
        ret
        .size u_swift_45, .-u_swift_45
        .globl u_swift_46
        .type u_swift_46, @function
u_swift_46:
        ret
        .size u_swift_46, .-u_swift_46
        .globl u_swift_47
        .type u_swift_47, @function
u_swift_47:
        mov %edi,%eax
        ret
        .size u_swift_47, .-u_swift_47
        .globl u_swift_54
        .type u_swift_54, @function
u_swift_54:
        mov %edi,%eax
        ret
        .size u_swift_54, .-u_swift_54
        .globl u_swift_55
        .type u_swift_55, @function
u_swift_55:
        mov %rdi,%rax
        ret
        .size u_swift_55, .-u_swift_55
        .globl u_swift_56
        .type u_swift_56, @function
u_swift_56:
        mov %rdi,%rax
        ret
        .size u_swift_56, .-u_swift_56
        .globl u_swift_57
        .type u_swift_57, @function
u_swift_57:
        ret
        .size u_swift_57, .-u_swift_57
        .globl u_swift_58
        .type u_swift_58, @function
u_swift_58:
        ret
        .size u_swift_58, .-u_swift_58
        .globl u_swift_59
        .type u_swift_59, @function
u_swift_59:
        mov %edi,%eax
        ret
        .size u_swift_59, .-u_swift_59
        .globl u_swift_66
        .type u_swift_66, @function
u_swift_66:
        mov %edi,%eax
        ret
        .size u_swift_66, .-u_swift_66
        .globl u_swift_67
        .type u_swift_67, @function
u_swift_67:
        mov %rdi,%rax
        ret
        .size u_swift_67, .-u_swift_67
        .globl u_swift_68
        .type u_swift_68, @function
u_swift_68:
        mov %rdi,%rax
        ret
        .size u_swift_68, .-u_swift_68
        .globl u_swift_69
        .type u_swift_69, @function
u_swift_69:
        ret
        .size u_swift_69, .-u_swift_69
        .globl u_swift_70
        .type u_swift_70, @function
u_swift_70:
        ret
        .size u_swift_70, .-u_swift_70
        .globl u_swift_71
        .type u_swift_71, @function
u_swift_71:
        mov %edi,%eax
        ret
        .size u_swift_71, .-u_swift_71
        .globl u_swift_135
        .type u_swift_135, @function
u_swift_135:
        mulss %xmm1,%xmm0
        ret
        .size u_swift_135, .-u_swift_135
        .globl u_swift_142
        .type u_swift_142, @function
u_swift_142:
        mulsd %xmm1,%xmm0
        ret
        .size u_swift_142, .-u_swift_142
        .globl u_swift_171
        .type u_swift_171, @function
u_swift_171:
        divss %xmm1,%xmm0
        ret
        .size u_swift_171, .-u_swift_171
        .globl u_swift_178
        .type u_swift_178, @function
u_swift_178:
        divsd %xmm1,%xmm0
        ret
        .size u_swift_178, .-u_swift_178
        .globl u_swift_243
        .type u_swift_243, @function
u_swift_243:
        addss %xmm1,%xmm0
        ret
        .size u_swift_243, .-u_swift_243
        .globl u_swift_250
        .type u_swift_250, @function
u_swift_250:
        addsd %xmm1,%xmm0
        ret
        .size u_swift_250, .-u_swift_250
        .globl u_swift_279
        .type u_swift_279, @function
u_swift_279:
        subss %xmm1,%xmm0
        ret
        .size u_swift_279, .-u_swift_279
        .globl u_swift_286
        .type u_swift_286, @function
u_swift_286:
        subsd %xmm1,%xmm0
        ret
        .size u_swift_286, .-u_swift_286
        .globl u_swift_294
        .type u_swift_294, @function
u_swift_294:
        cmp %esi,%edi
        setl %al
        ret
        .size u_swift_294, .-u_swift_294
        .globl u_swift_295
        .type u_swift_295, @function
u_swift_295:
        movslq %edi,%rax
        cmp %rsi,%rax
        setl %al
        ret
        .size u_swift_295, .-u_swift_295
        .globl u_swift_296
        .type u_swift_296, @function
u_swift_296:
        test %edi,%edi
        sets %cl
        movslq %edi,%rax
        cmp %rsi,%rax
        setb %al
        or %cl,%al
        ret
        .size u_swift_296, .-u_swift_296
        .globl u_swift_300
        .type u_swift_300, @function
u_swift_300:
        movslq %esi,%rax
        cmp %rdi,%rax
        setg %al
        ret
        .size u_swift_300, .-u_swift_300
        .globl u_swift_301
        .type u_swift_301, @function
u_swift_301:
        cmp %rsi,%rdi
        setl %al
        ret
        .size u_swift_301, .-u_swift_301
        .globl u_swift_302
        .type u_swift_302, @function
u_swift_302:
        test %rdi,%rdi
        sets %cl
        cmp %rsi,%rdi
        setb %al
        or %cl,%al
        ret
        .size u_swift_302, .-u_swift_302
        .globl u_swift_306
        .type u_swift_306, @function
u_swift_306:
        test %esi,%esi
        setg %cl
        movslq %esi,%rax
        cmp %rdi,%rax
        seta %al
        and %cl,%al
        ret
        .size u_swift_306, .-u_swift_306
        .globl u_swift_307
        .type u_swift_307, @function
u_swift_307:
        test %rsi,%rsi
        setg %cl
        cmp %rsi,%rdi
        setb %al
        and %cl,%al
        ret
        .size u_swift_307, .-u_swift_307
        .globl u_swift_308
        .type u_swift_308, @function
u_swift_308:
        cmp %rsi,%rdi
        setb %al
        ret
        .size u_swift_308, .-u_swift_308
        .globl u_swift_315
        .type u_swift_315, @function
u_swift_315:
        ucomiss %xmm0,%xmm1
        seta %al
        ret
        .size u_swift_315, .-u_swift_315
        .globl u_swift_322
        .type u_swift_322, @function
u_swift_322:
        ucomisd %xmm0,%xmm1
        seta %al
        ret
        .size u_swift_322, .-u_swift_322
        .globl u_swift_330
        .type u_swift_330, @function
u_swift_330:
        cmp %edi,%esi
        setl %al
        ret
        .size u_swift_330, .-u_swift_330
        .globl u_swift_331
        .type u_swift_331, @function
u_swift_331:
        movslq %edi,%rax
        cmp %rsi,%rax
        setg %al
        ret
        .size u_swift_331, .-u_swift_331
        .globl u_swift_332
        .type u_swift_332, @function
u_swift_332:
        test %edi,%edi
        setg %cl
        movslq %edi,%rax
        cmp %rsi,%rax
        seta %al
        and %cl,%al
        ret
        .size u_swift_332, .-u_swift_332
        .globl u_swift_336
        .type u_swift_336, @function
u_swift_336:
        movslq %esi,%rax
        cmp %rdi,%rax
        setl %al
        ret
        .size u_swift_336, .-u_swift_336
        .globl u_swift_337
        .type u_swift_337, @function
u_swift_337:
        cmp %rdi,%rsi
        setl %al
        ret
        .size u_swift_337, .-u_swift_337
        .globl u_swift_338
        .type u_swift_338, @function
u_swift_338:
        test %rdi,%rdi
        setg %cl
        cmp %rdi,%rsi
        setb %al
        and %cl,%al
        ret
        .size u_swift_338, .-u_swift_338
        .globl u_swift_342
        .type u_swift_342, @function
u_swift_342:
        test %esi,%esi
        sets %cl
        movslq %esi,%rax
        cmp %rdi,%rax
        setb %al
        or %cl,%al
        ret
        .size u_swift_342, .-u_swift_342
        .globl u_swift_343
        .type u_swift_343, @function
u_swift_343:
        test %rsi,%rsi
        sets %cl
        cmp %rdi,%rsi
        setb %al
        or %cl,%al
        ret
        .size u_swift_343, .-u_swift_343
        .globl u_swift_344
        .type u_swift_344, @function
u_swift_344:
        cmp %rdi,%rsi
        setb %al
        ret
        .size u_swift_344, .-u_swift_344
        .globl u_swift_351
        .type u_swift_351, @function
u_swift_351:
        ucomiss %xmm1,%xmm0
        seta %al
        ret
        .size u_swift_351, .-u_swift_351
        .globl u_swift_358
        .type u_swift_358, @function
u_swift_358:
        ucomisd %xmm1,%xmm0
        seta %al
        ret
        .size u_swift_358, .-u_swift_358
        .globl u_swift_366
        .type u_swift_366, @function
u_swift_366:
        cmp %edi,%esi
        setge %al
        ret
        .size u_swift_366, .-u_swift_366
        .globl u_swift_367
        .type u_swift_367, @function
u_swift_367:
        movslq %edi,%rax
        cmp %rsi,%rax
        setle %al
        ret
        .size u_swift_367, .-u_swift_367
        .globl u_swift_368
        .type u_swift_368, @function
u_swift_368:
        test %edi,%edi
        setle %cl
        movslq %edi,%rax
        cmp %rsi,%rax
        setbe %al
        or %cl,%al
        ret
        .size u_swift_368, .-u_swift_368
        .globl u_swift_372
        .type u_swift_372, @function
u_swift_372:
        movslq %esi,%rax
        cmp %rdi,%rax
        setge %al
        ret
        .size u_swift_372, .-u_swift_372
        .globl u_swift_373
        .type u_swift_373, @function
u_swift_373:
        cmp %rdi,%rsi
        setge %al
        ret
        .size u_swift_373, .-u_swift_373
        .globl u_swift_374
        .type u_swift_374, @function
u_swift_374:
        test %rdi,%rdi
        setle %cl
        cmp %rdi,%rsi
        setae %al
        or %cl,%al
        ret
        .size u_swift_374, .-u_swift_374
        .globl u_swift_378
        .type u_swift_378, @function
u_swift_378:
        test %esi,%esi
        setns %cl
        movslq %esi,%rax
        cmp %rdi,%rax
        setae %al
        and %cl,%al
        ret
        .size u_swift_378, .-u_swift_378
        .globl u_swift_379
        .type u_swift_379, @function
u_swift_379:
        test %rsi,%rsi
        setns %cl
        cmp %rdi,%rsi
        setae %al
        and %cl,%al
        ret
        .size u_swift_379, .-u_swift_379
        .globl u_swift_380
        .type u_swift_380, @function
u_swift_380:
        cmp %rdi,%rsi
        setae %al
        ret
        .size u_swift_380, .-u_swift_380
        .globl u_swift_387
        .type u_swift_387, @function
u_swift_387:
        ucomiss %xmm0,%xmm1
        setae %al
        ret
        .size u_swift_387, .-u_swift_387
        .globl u_swift_394
        .type u_swift_394, @function
u_swift_394:
        ucomisd %xmm0,%xmm1
        setae %al
        ret
        .size u_swift_394, .-u_swift_394
        .globl u_swift_402
        .type u_swift_402, @function
u_swift_402:
        cmp %esi,%edi
        setge %al
        ret
        .size u_swift_402, .-u_swift_402
        .globl u_swift_403
        .type u_swift_403, @function
u_swift_403:
        movslq %edi,%rax
        cmp %rsi,%rax
        setge %al
        ret
        .size u_swift_403, .-u_swift_403
        .globl u_swift_404
        .type u_swift_404, @function
u_swift_404:
        test %edi,%edi
        setns %cl
        movslq %edi,%rax
        cmp %rsi,%rax
        setae %al
        and %cl,%al
        ret
        .size u_swift_404, .-u_swift_404
        .globl u_swift_408
        .type u_swift_408, @function
u_swift_408:
        movslq %esi,%rax
        cmp %rdi,%rax
        setle %al
        ret
        .size u_swift_408, .-u_swift_408
        .globl u_swift_409
        .type u_swift_409, @function
u_swift_409:
        cmp %rsi,%rdi
        setge %al
        ret
        .size u_swift_409, .-u_swift_409
        .globl u_swift_410
        .type u_swift_410, @function
u_swift_410:
        test %rdi,%rdi
        setns %cl
        cmp %rsi,%rdi
        setae %al
        and %cl,%al
        ret
        .size u_swift_410, .-u_swift_410
        .globl u_swift_414
        .type u_swift_414, @function
u_swift_414:
        test %esi,%esi
        setle %cl
        movslq %esi,%rax
        cmp %rdi,%rax
        setbe %al
        or %cl,%al
        ret
        .size u_swift_414, .-u_swift_414
        .globl u_swift_415
        .type u_swift_415, @function
u_swift_415:
        test %rsi,%rsi
        setle %cl
        cmp %rsi,%rdi
        setae %al
        or %cl,%al
        ret
        .size u_swift_415, .-u_swift_415
        .globl u_swift_416
        .type u_swift_416, @function
u_swift_416:
        cmp %rsi,%rdi
        setae %al
        ret
        .size u_swift_416, .-u_swift_416
        .globl u_swift_423
        .type u_swift_423, @function
u_swift_423:
        ucomiss %xmm1,%xmm0
        setae %al
        ret
        .size u_swift_423, .-u_swift_423
        .globl u_swift_430
        .type u_swift_430, @function
u_swift_430:
        ucomisd %xmm1,%xmm0
        setae %al
        ret
        .size u_swift_430, .-u_swift_430
        .globl u_swift_438
        .type u_swift_438, @function
u_swift_438:
        cmp %esi,%edi
        setne %al
        ret
        .size u_swift_438, .-u_swift_438
        .globl u_swift_439
        .type u_swift_439, @function
u_swift_439:
        movslq %edi,%rax
        cmp %rsi,%rax
        setne %al
        ret
        .size u_swift_439, .-u_swift_439
        .globl u_swift_440
        .type u_swift_440, @function
u_swift_440:
        test %edi,%edi
        sets %cl
        movslq %edi,%rax
        cmp %rsi,%rax
        setne %al
        or %cl,%al
        ret
        .size u_swift_440, .-u_swift_440
        .globl u_swift_444
        .type u_swift_444, @function
u_swift_444:
        movslq %esi,%rax
        cmp %rdi,%rax
        setne %al
        ret
        .size u_swift_444, .-u_swift_444
        .globl u_swift_445
        .type u_swift_445, @function
u_swift_445:
        cmp %rsi,%rdi
        setne %al
        ret
        .size u_swift_445, .-u_swift_445
        .globl u_swift_446
        .type u_swift_446, @function
u_swift_446:
        test %rdi,%rdi
        sets %cl
        cmp %rsi,%rdi
        setne %al
        or %cl,%al
        ret
        .size u_swift_446, .-u_swift_446
        .globl u_swift_450
        .type u_swift_450, @function
u_swift_450:
        test %esi,%esi
        sets %cl
        movslq %esi,%rax
        cmp %rdi,%rax
        setne %al
        or %cl,%al
        ret
        .size u_swift_450, .-u_swift_450
        .globl u_swift_451
        .type u_swift_451, @function
u_swift_451:
        test %rsi,%rsi
        sets %cl
        cmp %rsi,%rdi
        setne %al
        or %cl,%al
        ret
        .size u_swift_451, .-u_swift_451
        .globl u_swift_452
        .type u_swift_452, @function
u_swift_452:
        cmp %rsi,%rdi
        setne %al
        ret
        .size u_swift_452, .-u_swift_452
        .globl u_swift_459
        .type u_swift_459, @function
u_swift_459:
        cmpneqss %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%eax
        ret
        .size u_swift_459, .-u_swift_459
        .globl u_swift_466
        .type u_swift_466, @function
u_swift_466:
        cmpneqsd %xmm1,%xmm0
        movq %xmm0,%rax
        and $0x1,%eax
        ret
        .size u_swift_466, .-u_swift_466
        .globl u_swift_473
        .type u_swift_473, @function
u_swift_473:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_swift_473, .-u_swift_473
        .globl u_swift_510
        .type u_swift_510, @function
u_swift_510:
        cmp %esi,%edi
        sete %al
        ret
        .size u_swift_510, .-u_swift_510
        .globl u_swift_511
        .type u_swift_511, @function
u_swift_511:
        movslq %edi,%rax
        cmp %rsi,%rax
        sete %al
        ret
        .size u_swift_511, .-u_swift_511
        .globl u_swift_512
        .type u_swift_512, @function
u_swift_512:
        test %edi,%edi
        setns %cl
        movslq %edi,%rax
        cmp %rsi,%rax
        sete %al
        and %cl,%al
        ret
        .size u_swift_512, .-u_swift_512
        .globl u_swift_516
        .type u_swift_516, @function
u_swift_516:
        movslq %esi,%rax
        cmp %rdi,%rax
        sete %al
        ret
        .size u_swift_516, .-u_swift_516
        .globl u_swift_517
        .type u_swift_517, @function
u_swift_517:
        cmp %rsi,%rdi
        sete %al
        ret
        .size u_swift_517, .-u_swift_517
        .globl u_swift_518
        .type u_swift_518, @function
u_swift_518:
        test %rdi,%rdi
        setns %cl
        cmp %rsi,%rdi
        sete %al
        and %cl,%al
        ret
        .size u_swift_518, .-u_swift_518
        .globl u_swift_522
        .type u_swift_522, @function
u_swift_522:
        test %esi,%esi
        setns %cl
        movslq %esi,%rax
        cmp %rdi,%rax
        sete %al
        and %cl,%al
        ret
        .size u_swift_522, .-u_swift_522
        .globl u_swift_523
        .type u_swift_523, @function
u_swift_523:
        test %rsi,%rsi
        setns %cl
        cmp %rsi,%rdi
        sete %al
        and %cl,%al
        ret
        .size u_swift_523, .-u_swift_523
        .globl u_swift_524
        .type u_swift_524, @function
u_swift_524:
        cmp %rsi,%rdi
        sete %al
        ret
        .size u_swift_524, .-u_swift_524
        .globl u_swift_531
        .type u_swift_531, @function
u_swift_531:
        cmpeqss %xmm1,%xmm0
        movd %xmm0,%eax
        and $0x1,%eax
        ret
        .size u_swift_531, .-u_swift_531
        .globl u_swift_538
        .type u_swift_538, @function
u_swift_538:
        cmpeqsd %xmm1,%xmm0
        movq %xmm0,%rax
        and $0x1,%eax
        ret
        .size u_swift_538, .-u_swift_538
        .globl u_swift_545
        .type u_swift_545, @function
u_swift_545:
        mov %edi,%eax
        xor %esi,%eax
        xor $0x1,%al
        ret
        .size u_swift_545, .-u_swift_545
        .globl u_swift_582
        .type u_swift_582, @function
u_swift_582:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_swift_582, .-u_swift_582
        .globl u_swift_589
        .type u_swift_589, @function
u_swift_589:
        mov %rdi,%rax
        and %rsi,%rax
        ret
        .size u_swift_589, .-u_swift_589
        .globl u_swift_596
        .type u_swift_596, @function
u_swift_596:
        mov %rdi,%rax
        and %rsi,%rax
        ret
        .size u_swift_596, .-u_swift_596
        .globl u_swift_618
        .type u_swift_618, @function
u_swift_618:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_swift_618, .-u_swift_618
        .globl u_swift_625
        .type u_swift_625, @function
u_swift_625:
        mov %rdi,%rax
        or %rsi,%rax
        ret
        .size u_swift_625, .-u_swift_625
        .globl u_swift_632
        .type u_swift_632, @function
u_swift_632:
        mov %rdi,%rax
        or %rsi,%rax
        ret
        .size u_swift_632, .-u_swift_632
        .globl u_swift_654
        .type u_swift_654, @function
u_swift_654:
        mov %edi,%eax
        xor %esi,%eax
        ret
        .size u_swift_654, .-u_swift_654
        .globl u_swift_661
        .type u_swift_661, @function
u_swift_661:
        mov %rdi,%rax
        xor %rsi,%rax
        ret
        .size u_swift_661, .-u_swift_661
        .globl u_swift_668
        .type u_swift_668, @function
u_swift_668:
        mov %rdi,%rax
        xor %rsi,%rax
        ret
        .size u_swift_668, .-u_swift_668
        .globl u_swift_704
        .type u_swift_704, @function
u_swift_704:
        mov %rsi,%rcx
        shl %cl,%rdi
        xor %eax,%eax
        cmp $0x40,%rsi
        cmovb %rdi,%rax
        ret
        .size u_swift_704, .-u_swift_704
        .globl u_swift_740
        .type u_swift_740, @function
u_swift_740:
        mov %rsi,%rcx
        shr %cl,%rdi
        xor %eax,%eax
        cmp $0x40,%rsi
        cmovb %rdi,%rax
        ret
        .size u_swift_740, .-u_swift_740
        .globl u_swift_797
        .type u_swift_797, @function
u_swift_797:
        mov %edi,%eax
        and %esi,%eax
        ret
        .size u_swift_797, .-u_swift_797
        .globl u_swift_833
        .type u_swift_833, @function
u_swift_833:
        mov %edi,%eax
        or %esi,%eax
        ret
        .size u_swift_833, .-u_swift_833
        .globl u_swift_834
        .type u_swift_834, @function
u_swift_834:
        mov %edi,%eax
        ret
        .size u_swift_834, .-u_swift_834
        .globl u_swift_841
        .type u_swift_841, @function
u_swift_841:
        mov %rdi,%rax
        ret
        .size u_swift_841, .-u_swift_841
        .globl u_swift_848
        .type u_swift_848, @function
u_swift_848:
        mov %rdi,%rax
        ret
        .size u_swift_848, .-u_swift_848
        .globl u_swift_855
        .type u_swift_855, @function
u_swift_855:
        ret
        .size u_swift_855, .-u_swift_855
        .globl u_swift_862
        .type u_swift_862, @function
u_swift_862:
        ret
        .size u_swift_862, .-u_swift_862
        .globl u_swift_869
        .type u_swift_869, @function
u_swift_869:
        mov %edi,%eax
        ret
        .size u_swift_869, .-u_swift_869
