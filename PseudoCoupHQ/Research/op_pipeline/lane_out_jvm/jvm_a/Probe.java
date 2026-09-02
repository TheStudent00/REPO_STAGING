public class Probe {
    static int af(int a, int b) {
        return a + b;
    }
    static int af2(int a, int b) {
        return a / b;
    }
    static int sink;
    public static void main(String[] args) {
        int n = Integer.parseInt(args[0]);
        long t0 = System.nanoTime();
        int acc = 0;
        int i = 0;
        while (i < n) {
            acc = af(acc, 1);
            i = i + 1;
        }
        int acc2 = 0;
        int j = 1;
        while (j < n) {
            acc2 = af2(j, 3);
            j = j + 1;
        }
        long t1 = System.nanoTime();
        sink = acc + acc2;
        long ms = (t1 - t0) / 1000000L;
        System.out.println("WARMED n=" + n + " acc=" + acc
                           + " acc2=" + acc2 + " ms=" + ms);
    }
}
