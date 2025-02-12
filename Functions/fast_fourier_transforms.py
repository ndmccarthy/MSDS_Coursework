# Fast Fourier Transforms and Related Functions

import numpy as np

def polynomial_multiply(a_coeff_list, b_coeff_list):
    # This function uses DFT and IDFT to quickly multiply polynomials (via a list of their coefficients).

    # STEP 1: Pad lists to be equal to the combined lengths of A and B - 1.
    a_len = len(a_coeff_list)
    b_len = len(b_coeff_list)
    a_coeff_list = np.pad(a_coeff_list, (0,b_len-1), mode='constant')
    b_coeff_list = np.pad(b_coeff_list, (0,a_len-1), mode='constant')

    # STEP 2: Turn the coefficient lists into matrices of point-value representations of the coefficients.
    # This turns the coefficients into complex numbers (a + bj) that are represented as vector points (a, b).
    a_pt_value_pairs = np.fft.fft(a_coeff_list)
    b_pt_value_pairs = np.fft.fft(b_coeff_list)

    # STEP 3: Multiply the matrices.
    # Make sure to do element wise multiplication (*) rather than matrix multiplication (@) due to constraints of np.fft/ifft.
    c_pt_value_pairs = a_pt_value_pairs * b_pt_value_pairs

    # STEP 4: Reverse the resulting point-value matrix to a list of coefficients using IDFT.
    c_coeff_list = np.fft.ifft(c_pt_value_pairs)

    # STEP 5: Convert c_coeff_list from complex numbers to real numbers. (Imaginary part is 0.)
    c_coeff_list = np.real(c_coeff_list)

    return c_coeff_list