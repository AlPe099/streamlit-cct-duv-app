import streamlite as st
import math

def planckian_xy_approx(T):
  """
  Approximation polynomiale (4000..25000 K) pour T -> (x, y) CIE 1931.
  """
  invT = 1.0 / T
  invT2 = invT * invT
  invT3 = invT2 * invT

  #Polynôme x
  x = -3.0258469e9 * invT3 + 2.10
