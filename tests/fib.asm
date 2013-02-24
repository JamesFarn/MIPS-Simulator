
fib.o:     file format elf32-bigmips


Disassembly of section .text:

00000000 <main>:
 * an integer, and we return 0 to indicate successful completion of the 
 * program.
 */

int main ()
{
   //0:	27bdffe0 	addiu	sp,sp,-32
   0: 27bdffe0  addiu sp,sp,32
   4:	afbe001c 	sw	s8,28(sp)
   8:	03a0f021 	move	s8,sp
  /* Notice that we need to declare our variables, and their type */

  int n = 50; // 10
   c:	24020032 	li	v0,50
  10:	afc2000c 	sw	v0,12(s8)
  int a = 0;
  14:	afc00000 	sw	zero,0(s8)
  int b = 1;
  18:	24020001 	li	v0,1
  1c:	afc20004 	sw	v0,4(s8)
  
  /**
   * Here is the standard for loop. This will step through, performing the code
   * inside the braces until i is equal to n.
   */
  for ( i = 0; i < n; i++)			
  20:	afc00008 	sw	zero,8(s8)
  24:	0800001a 	j	68 <main+0x68>
  28:	00000000 	nop
  {							 
    //printf("a: %u, b: %u, ", a, b);
    sum = a + b;
  2c:	8fc30000 	lw	v1,0(s8)
  30:	8fc20004 	lw	v0,4(s8)
  34:	00000000 	nop
  38:	00621021 	addu	v0,v1,v0
  3c:	afc20010 	sw	v0,16(s8)
    //printf("sum: %u\n", sum);
    a = b;
  40:	8fc20004 	lw	v0,4(s8)
  44:	00000000 	nop
  48:	afc20000 	sw	v0,0(s8)
    b = sum;
  4c:	8fc20010 	lw	v0,16(s8)
  50:	00000000 	nop
  54:	afc20004 	sw	v0,4(s8)
  
  /**
   * Here is the standard for loop. This will step through, performing the code
   * inside the braces until i is equal to n.
   */
  for ( i = 0; i < n; i++)			
  58:	8fc20008 	lw	v0,8(s8)
  5c:	00000000 	nop
  60:	24420001 	addiu	v0,v0,1
  64:	afc20008 	sw	v0,8(s8)
  68:	8fc30008 	lw	v1,8(s8)
  6c:	8fc2000c 	lw	v0,12(s8)
  70:	00000000 	nop
  74:	0062102a 	slt	v0,v1,v0
  78: 00000000  nop
  7c:	1440ffec 	bnez	v0,2c <main+0x2c>
  80:	00000000 	nop
    //printf("a: %d, b: %d, sum: %d\n", a, b, sum);
  }

  /* Finally, return 0 */

  return 0;
  84:	00001021 	move	v0,zero
}
  88:	03c0e821 	move	sp,s8
  8c:	8fbe001c 	lw	s8,28(sp)
  90:	27bd0020 	addiu	sp,sp,32
 // 94:	03e00008 	jr	ra
  98:	00000000 	nop
