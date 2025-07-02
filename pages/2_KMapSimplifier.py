import streamlit as st
from sympy import symbols, SOPform, POSform, simplify_logic
from sympy.parsing.sympy_parser import parse_expr
import pandas as pd

# 🎨 Sidebar style
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🟩 K-Map Simplifier")

st.write("**2-variable or 3-variable K-Map Simplifier with Don't Care & SOP, POS, Quine–McCluskey**")

num_vars = st.selectbox("Select Number of Variables", [2, 3])

if num_vars == 2:
    st.write("**2-Variable K-Map: Enter outputs for minterms 0–3**")
    labels = ["00", "01", "10", "11"]
    variables = ['A', 'B']
elif num_vars == 3:
    st.write("**3-Variable K-Map: Enter outputs for minterms 0–7**")
    labels = ["000", "001", "010", "011", "100", "101", "110", "111"]
    variables = ['A', 'B', 'C']

outputs = []
dont_cares = []
for label in labels:
    val = st.selectbox(f"f({label})", ["0", "1", "X (Don't Care)"], key=f"kmap_{label}")
    if val == "1":
        outputs.append(1)
        dont_cares.append(0)
    elif val == "X (Don't Care)":
        outputs.append(0)
        dont_cares.append(1)
    else:
        outputs.append(0)
        dont_cares.append(0)

if st.button("Simplify & Convert"):
    minterms = [i for i, v in enumerate(outputs) if v == 1]
    dc_terms = [i for i, v in enumerate(dont_cares) if v == 1]
    maxterms = [i for i, v in enumerate(outputs) if v == 0 and not dont_cares[i]]

    # ✅ Check overlap
    overlap = set(minterms).intersection(dc_terms)
    if overlap:
        st.error(f"❌ Error: These terms are in both minterms and don't cares: {list(overlap)}. Please fix your input.")
    else:
        st.write(f"**Minterms:** {minterms}")
        st.write(f"**Maxterms:** {maxterms}")
        st.write(f"**Don't Cares:** {dc_terms}")

        vars_sym = symbols(variables)

        if minterms:
            sop = SOPform(vars_sym, minterms, dc_terms)
            st.write(f"**SOP (Sum of Products):** `{sop}`")

            qm = simplify_logic(sop, form='dnf')
            st.write(f"**Quine–McCluskey Minimized SOP:** `{qm}`")

        if maxterms:
            pos = POSform(vars_sym, maxterms, dc_terms)
            st.write(f"**POS (Product of Sums):** `{pos}`")

        if not minterms and not dc_terms:
            st.info("Output is always 0.")
        elif not maxterms and not dc_terms:
            st.info("Output is always 1.")

        # ✅ K-Map visualization
        st.subheader("🗺️ K-Map Table")
        if num_vars == 2:
            kmap_grid = pd.DataFrame(
                [[outputs[0], outputs[1]],
                 [outputs[2], outputs[3]]],
                index=["A=0", "A=1"],
                columns=["B=0", "B=1"]
            )
        else:
            kmap_grid = pd.DataFrame(
                [[outputs[0], outputs[1], outputs[3], outputs[2]],
                 [outputs[4], outputs[5], outputs[7], outputs[6]]],
                index=["A=0", "A=1"],
                columns=["BC=00", "BC=01", "BC=11", "BC=10"]
            )
        st.table(kmap_grid)

st.divider()

st.subheader("📐 Expression ➜ Minterm, Maxterm & Quine–McCluskey")

expr_input = st.text_input("Enter Boolean Expression (Example: A & B | ~C )")

if expr_input:
    try:
        vars_sym = symbols(variables)
        expr = parse_expr(expr_input, evaluate=False)
        minterms_expr = simplify_logic(expr, form='dnf')
        maxterms_expr = simplify_logic(expr, form='cnf')
        qm_expr = simplify_logic(expr)

        st.write(f"**Simplified SOP (DNF):** `{minterms_expr}`")
        st.write(f"**Simplified POS (CNF):** `{maxterms_expr}`")
        st.write(f"**Quine–McCluskey Minimized:** `{qm_expr}`")

    except Exception as e:
        st.error(f"❌ Error parsing expression: {e}")
