import streamlite as st
import math

def planckian_xy_approx(T):
    """
    Approximation polynomiale (4000..25000 K) pour T -> (x, y) CIE 1931.
    """
    invT = 1.0 / T
    invT2 = invT * invT
    invT3 = invT2 * invT

    # Polynôme x
    x = -3.0258469e9 * invT3 + 2.1070379e6 * invT2 + 0.2226347e3 * invT + 0.240390
    # Relation y
    y = -3.0*(x**2) + 2.87*x - 0.275

    return (x, y)
  
  def xy_to_uv1976(x, y):
    """
    (x, y) CIE 1931 -> (u′, v′) CIE 1976.
    """
    denom = -2*x + 12*y + 3
    if abs(denom) < 1e-15:
        return (0.0, 0.0)
    u_prime = 4*x / denom
    v_prime = 9*y / denom
    return (u_prime, v_prime)

def uv1976_to_xy(u_prime, v_prime):
    """
    (u′, v′) CIE 1976 -> (x, y) CIE 1931.
    """
    denom = 6*u_prime - 16*v_prime + 12
    if abs(denom) < 1e-15:
        return (0.0, 0.0)
    x = 9*u_prime / denom
    y = 4*v_prime / denom
    return (x, y)
