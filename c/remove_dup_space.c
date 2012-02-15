#include <stdio.h>

main()
{
	int c, newstr, is_space_flag, space_count;

	is_space_flag = 0;
	space_count = 0;

	while ((c = getchar()) != EOF) {
		if ( c == ' ') {
			if ( is_space_flag == 1) {
				++space_count;
			} else {
				is_space_flag = 1;
				++space_count;
			}
		} else {
			is_space_flag = 0;
		}
	}
}
