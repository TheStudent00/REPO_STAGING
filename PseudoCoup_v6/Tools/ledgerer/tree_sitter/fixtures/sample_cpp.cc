// Pinned census fixture: representative C++ constructs (the shapes
// LLVM encoder ingress meets: switch, bit arithmetic, classes,
// member calls, increments). Do not edit.
#include <cstdint>

class Emitter {
  uint8_t buf[16];
  int cur = 0;

 public:
  void emitByte(uint8_t b) { buf[cur++] = b; }

  uint8_t modRM(unsigned mod, unsigned reg, unsigned rm) {
    return static_cast<uint8_t>(mod << 6 | (reg & 7) << 3 | (rm & 7));
  }

  void encode(int form) {
    switch (form) {
      case 0:
        emitByte(0x40 | 1 << 3);
        break;
      case 1:
        emitByte(modRM(3, 2, 5));
        break;
      default:
        break;
    }
  }
};

int main() {
  Emitter e;
  for (int i = 0; i < 2; i++) e.encode(i);
  return 0;
}
