#include <stdio.h>

#define IN 1
#define OUT 0

main()
{
    int c, word, state, word_counts;

    word_counts = 0;
    while ((c = getchar()) != EOF ) {
        if (c != ' ') {
            state = IN;
            putchar(c);
            ++word_counts;
        } else {
            state = OUT;
        }
        if (state == OUT) {
            int i;
            printf(" %d: ", word_counts);
            for (i=0; i<word_counts; i++) {
                printf("|");
            }
            word_counts = 0;
            printf("\n");
        }
    }
    int i;
    printf(" %d: ", word_counts);
    for (i=0; i<word_counts; i++) {
        printf("|");
    }
    word_counts = 0;
    printf("\n");
}
