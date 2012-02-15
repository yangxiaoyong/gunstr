#include <stdio.h>

/* copy input to output; 1st version */

main()
{
	/* 整形也可以用于存储字符数据 */
	int c;

	while ((c = getchar()) != EOF) {
		putchar(c);
	}
	putchar(EOF);
}
