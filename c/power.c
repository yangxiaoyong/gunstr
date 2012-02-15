#include <stdio.h>

int power(int m, int n); /* 函数原型, 如果函数的定义，用法与函数原型不一致，将出现错误*/

main() {
    int i;
    for (i=0; i<10; ++i) {
        printf("%d %d %d\n", i, power(2, i), power(-3, i));
    }
}

int power(int base, int n) {
    int i, p;
    p = 1;
    for (i=1; i<=n; ++i) {
        p = p * base;
    }
    return p;
}
