#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_NUM	(1000000)
#define MAX_SUB	(10)

prn_float(float *f, int max)
{
	int i;
	for(i=0; i<max; i++)
		printf("%3.1f ", f[i]);
	printf("\n");
}

	float A[MAX_NUM][MAX_SUB];
main()
{
	//float **A=0;
	float	sum[MAX_SUB];
	float	sum2[MAX_SUB];
	float	avg[MAX_SUB];
	float	dev[MAX_SUB];
	int	i,j;

	memset (sum, 0,  sizeof(sum));
	memset (sum2, 0,  sizeof(sum2));
	memset (avg, 0,  sizeof(avg));
	memset (dev, 0,  sizeof(dev));

	//A = (float **)calloc(MAX_NUM, MAX_SUB*sizeof(float));
	printf ("%X\n", A);
	fflush(stdout);
	srand(time(0));

	for(i=0; i<MAX_NUM; i++)
		for(j=0; j<MAX_SUB; j++)
			A[i][j] = rand()%100 + 1;

	for(i=0; i<MAX_NUM; i++)
		for(j=0; j<MAX_SUB; j++) {
			float v;
			v = A[i][j]+(float)j*0.7;
			sum[j] += v;
			sum2[j] += v*v;
		}

	prn_float(sum, MAX_SUB);
	prn_float(sum2, MAX_SUB);

	for(j=0; j<MAX_SUB; j++) {
		avg[j] = sum[j] / MAX_NUM;
		dev[j] = sum2[j] / MAX_NUM;
	}

	prn_float(avg, MAX_SUB);
	prn_float(dev, MAX_SUB);
}
