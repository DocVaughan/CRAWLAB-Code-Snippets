
/* ----------------------------------------------------------------------------

circular_buffer.c

Basic circular buffer implementation, with both empty and overflow conditions

Code derived from: 
  http://embedjournal.com/implementing-circular-buffer-embedded-c/

Created: 01/15/16
   - Joshua Vaughan
   - joshua.vaughan@louisiana.edu
   - http://www.ucs.louisiana.edu/~jev9637

 Modified:
   *

---------------------------------------------------------------------------- */

#include <stdio.h>
#include <inttypes.h>

typedef struct
{
    uint8_t * const buffer;
    int head;
    int tail;
    const int maxLen;
}circBuf_t;


int circBufPush(circBuf_t *c, uint8_t data)
{
    int next = c->head + 1;
    if (next >= c->maxLen)
        next = 0;
 
    // Cicular buffer is full
    if (next == c->tail)
        return -1;  // quit with an error
 
    c->buffer[c->head] = data;
    c->head = next;
    return 0;
}
 

int circBufPop(circBuf_t *c, uint8_t *data)
{
    // if the head isn't ahead of the tail, we don't have any characters
    if (c->head == c->tail)
        return -1;  // quit with an error
 
    *data = c->buffer[c->tail];
    c->buffer[c->tail] = 0;  // clear the data (optional)
 
    int next = c->tail + 1;
    if(next >= c->maxLen)
        next = 0;
 
    c->tail = next;
 
    return 0;
}

#define CIRCBUF_DEF(x,y) uint8_t x##_space[y]; circBuf_t x = { x##_space,0,0,y}


int main(int argc, char *argv[]) {
	int i;
	uint8_t data;
	
	CIRCBUF_DEF(cb, 32);
	
	i = 1;
	
	// This for loop should result in an empty buffer
	// We are reading more times that we are writing
	for(uint8_t counter = 1; counter <= 100; counter++) {
		printf("\nWriting %d \n", counter);
		
		if (circBufPush(&cb, counter)) {
            printf("Out of space in CB\n");
		    break;
        }

		// Pop a value each time through the loop
		if (counter % 1 == 0) {
			if (circBufPop(&cb, &data)) {
	            printf("CB is empty\n");
	        }
	
			printf("Mod(1) read %d \n", data);
		}

		// Pop a value every other time through the loop
		if (counter % 2 == 0) {
			if (circBufPop(&cb, &data)) {
	            printf("CB is empty\n");
	        }
	
			printf("Mod(2) read %d \n", data);
		}
		
		// Pop a value every 6th time through the loop
		if (counter % 6 == 0) {
			if (circBufPop(&cb, &data)) {
	            printf("CB is empty\n");
	        }
	
			printf("Mod(6) read %d \n", data);
		}
		
	}
	
	printf("\n \n");
	
	
	// This for loop should result in an full buffer
	// We are writing more times that we are reading
	for(uint8_t counter = 1; counter <= 100; counter++) {
		
		printf("\nWriting %d \n", counter);
		
		if (circBufPush(&cb, counter)) {
            printf("Out of space in CB\n");
		    break;
        }

		// P a value every other time through the loop
		if (counter % 2 == 0) {
			if (circBufPop(&cb, &data)) {
	            printf("CB is empty\n");
	        }
	
			printf("Mod(2) read %d \n", data);
		}
		
	}
	
}