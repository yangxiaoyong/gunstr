#include <stdio.h>
/* 每个单词换行打印 */

main() {
	int c;
	while ((c = getchar()) != EOF) {
		putchar(c);
		if (c == '\t' || c == ' ') {
			printf("\n");
		}
	}
}
