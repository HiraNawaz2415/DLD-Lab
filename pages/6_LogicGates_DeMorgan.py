import streamlit as st
import pandas as pd
from sympy import symbols, simplify_logic, Not, And, Or
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application
)
from itertools import product
from graphviz import Digraph
st.markdown(
    """
    <style>
    /* Make sidebar background gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2027, #203a43, #2c5364);
        color: white;
    }

    /* Optional: make sidebar text white */
    [data-testid="stSidebar"] .css-1v3fvcr {
        color: white;
    }

    /* Optional: style sidebar headings and text */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("🔄 DeMorgan’s Laws & Logic Gates")

# --- Pick how many variables
st.sidebar.markdown("## ⚙️ Settings")
num_vars = st.sidebar.slider("Number of Variables (for Gates Table)", min_value=1, max_value=4, value=2)

# Create variable symbols dynamically
vars_sym = symbols([chr(65 + i) for i in range(num_vars)])  # A, B, C, D...
vars_list = [str(v) for v in vars_sym]

st.markdown(f"""
### 🟢 Basic Logic Gates

- **AND ( & )**
- **OR ( | )**
- **NOT ( ~ )**
- **NAND = NOT(AND)**
- **NOR = NOT(OR)**
- **XOR = A ⊕ B**
- **XNOR = NOT(XOR)**

✅ Using variables: {', '.join(vars_list)}
""")

# Define gates based on 1st two variables for binary gates
A = vars_sym[0]
B = vars_sym[1] if num_vars > 1 else A  # fallback for single var

gates = {
    f"{A} AND {B}": And(A, B),
    f"{A} OR {B}": Or(A, B),
    f"NOT {A}": Not(A),
    f"{A} NAND {B}": Not(And(A, B)),
    f"{A} NOR {B}": Not(Or(A, B)),
    f"{A} XOR {B}": A ^ B,
    f"{A} XNOR {B}": Not(A ^ B)
}

# Truth table for gates
rows = []
for combo in product([0, 1], repeat=num_vars):
    row = list(combo)
    subs = dict(zip(vars_sym, combo))
    for g in gates.values():
        row.append(int(bool(g.subs(subs))))
    rows.append(row)

df = pd.DataFrame(rows, columns=vars_list + list(gates.keys()))
st.subheader("Basic Gates Truth Table")
st.dataframe(df)

# --- DeMorgan’s Laws ---
st.markdown("""
---

### 🔄 DeMorgan’s Laws

1️⃣ `NOT (A AND B)`  =  `(~A) OR (~B)`  
2️⃣ `NOT (A OR B)`   =  `(~A) AND (~B)`
""")

# Always show example with A,B
demorgan_1 = simplify_logic(Not(And(A, B)))
demorgan_2 = simplify_logic(Not(Or(A, B)))

st.info(f"**NOT({A} AND {B}):** `{demorgan_1}` → `~{A} | ~{B}`")
st.info(f"**NOT({A} OR {B}):** `{demorgan_2}` → `~{A} & ~{B}`")

# --- DeMorgan Evaluator ---
st.markdown("""
---

### ✏️ DeMorgan Evaluator

✅ Use:
- `&` for AND
- `|` for OR
- `~` for NOT

**Example:** `~(A & B)` or `~(A | B)`
""")

expr_input = st.text_input("Expression (e.g., ~(A & B) )")
vars_input = st.text_input("Variables (comma-separated, e.g., A,B)")

if expr_input and vars_input:
    try:
        # Auto-correct brackets
        open_brackets = expr_input.count("(")
        close_brackets = expr_input.count(")")
        expr_fixed = expr_input + (")" * (open_brackets - close_brackets)) if open_brackets > close_brackets else expr_input
        if open_brackets > close_brackets:
            st.warning(f"✅ Auto-corrected: `{expr_fixed}` (added {open_brackets - close_brackets} `)` )")

        vars_list = [v.strip() for v in vars_input.split(",")]
        vars_sym = symbols(vars_list)

        local_dict = {name: sym for name, sym in zip(vars_list, vars_sym)}
        transformations = standard_transformations + (implicit_multiplication_application,)

        expr = parse_expr(expr_fixed, local_dict, transformations=transformations)
        simplified = simplify_logic(expr)

        st.write(f"**Original:** `{expr}`")
        st.write(f"**Simplified:** `{simplified}`")

        rows = []
        for combo in product([0, 1], repeat=len(vars_list)):
            subs = dict(zip(vars_sym, combo))
            out = int(bool(expr.subs(subs)))
            rows.append(list(combo) + [out])
        df2 = pd.DataFrame(rows, columns=vars_list + ["Output"])
        st.subheader("Truth Table")
        st.dataframe(df2)

        st.subheader("Gate Diagram (Simplified)")
        dot = Digraph()
        counter = [0]

        def add_gate(node):
            if isinstance(node, And):
                gate_id = f"And_{counter[0]}"
                dot.node(gate_id, "AND")
                counter[0] += 1
                for arg in node.args:
                    child_id = add_gate(arg)
                    dot.edge(child_id, gate_id)
                return gate_id
            elif isinstance(node, Or):
                gate_id = f"Or_{counter[0]}"
                dot.node(gate_id, "OR")
                counter[0] += 1
                for arg in node.args:
                    child_id = add_gate(arg)
                    dot.edge(child_id, gate_id)
                return gate_id
            elif isinstance(node, Not):
                gate_id = f"Not_{counter[0]}"
                dot.node(gate_id, "NOT")
                counter[0] += 1
                child_id = add_gate(node.args[0])
                dot.edge(child_id, gate_id)
                return gate_id
            else:
                var_id = f"{str(node)}_{counter[0]}"
                dot.node(var_id, str(node))
                counter[0] += 1
                return var_id

        add_gate(simplified)
        st.graphviz_chart(dot)

    except Exception as e:
        st.error(f"❌ Error: {e}")
