import streamlit as st
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

def cct_duv_to_xy_1976(T, Duv):
    """
    Calcule (x, y) en CIE 1931 pour :
      - T (Kelvin)
      - Duv (CIE 1976)
    en faisant :
      1) planckian_xy_approx(T) -> (x0, y0)
      2) (u'0, v'0)
      3) planckian_xy_approx(T+0.01) -> tangente
      4) applique Duv en 1976
      5) convertit en (x, y)
    """
    # (x0, y0)
    x0, y0 = planckian_xy_approx(T)
    u0, v0 = xy_to_uv1976(x0, y0)

    # (x1, y1)
    x1, y1 = planckian_xy_approx(T + 0.01)
    u1, v1 = xy_to_uv1976(x1, y1)

    # Tangente
    du_tang = u1 - u0
    dv_tang = v1 - v0
    length_tang = math.sqrt(du_tang**2 + dv_tang**2)
    if length_tang < 1e-15:
        return (x0, y0)

    # Normal unitaire
    nx = -dv_tang / length_tang
    ny =  du_tang / length_tang

    # Décalage Duv (1976)
    u = u0 + Duv * nx
    v = v0 + Duv * ny

    # Retour en (x, y)
    return uv1976_to_xy(u, v)

def main():
    st.title("CCT + Duv (1976) → (x, y) en CIE 1931")

    st.write("Entrez la température de couleur (Kelvin) et le Duv (CIE 1976).")
    
    T = st.number_input("CCT (K)", min_value=1000.0, max_value=30000.0, value=6500.0)
    Duv = st.number_input("Duv (1976)", min_value=-0.1, max_value=0.1, value=0.0, format="%.5f")

    if st.button("Calculer"):
        x_val, y_val = cct_duv_to_xy_1976(T, Duv)
        st.success(f"Résultat : (x, y) = ({x_val:.4f}, {y_val:.4f})")

if __name__ == "__main__":
    main()
