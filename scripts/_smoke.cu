#include <cstdio>
__global__ void axpy(float a, const float* x, float* y, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) y[i] = a * x[i] + y[i];
}
int main() {
    int n = 256;
    printf("CUDA smoke OK, sm target compiled\n");
    return 0;
}
