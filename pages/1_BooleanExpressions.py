import streamlit as st
import pandas as pd
from sympy import symbols, simplify_logic
from sympy.logic.boolalg import And, Or, Not
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application
)
from itertools import product
from graphviz import Digraph
import re
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
st.title("🔢 Boolean Expression Evaluator with Gate Diagram")

st.markdown("""
**Example input:**  
- `A & (B | C)` → **A AND (B OR C)**  
- `~A | B` → **NOT A OR B**

✅ **Use:**  
- `&` for **AND**  
- `|` for **OR**  
- `~` for **NOT**  
- ⚠️ Always put an operator between variables and parentheses!  
- ✅ But don’t worry — this app will auto-fix `B(` → `B & (` when needed!
""")

expr_input = st.text_input("Expression (infix, e.g., A & (B | C))")
vars_input = st.text_input("Variables (comma-separated, e.g., A,B,C)")

def auto_fix_missing_and(expression):
    """
    Inserts '&' if a variable is directly followed by '('.
    E.g., turns 'A&B(~B&C)' → 'A & B & (~B & C)'
    """
    expression = expression.replace(" ", "")
    # Add '&' if a letter/number/underscore is immediately followed by '('
    fixed = re.sub(r'([A-Za-z0-9_])\(', r'\1 & (', expression)
    return fixed

if expr_input and vars_input:
    if expr_input.count("(") != expr_input.count(")"):
        st.error("❌ Error: Unmatched parentheses! Please check your expression.")
    else:
        try:
            vars_list = [v.strip() for v in vars_input.split(",")]
            vars_sym = symbols(vars_list)

            local_dict = {name: sym for name, sym in zip(vars_list, vars_sym)}

            transformations = standard_transformations + (implicit_multiplication_application,)

            # Auto-fix missing &
            expr_input_fixed = auto_fix_missing_and(expr_input)
            if expr_input != expr_input_fixed:
                st.info(f"🔧 Auto-fixed expression: `{expr_input_fixed}`")

            expr = parse_expr(expr_input_fixed, local_dict, transformations=transformations)
            simplified = simplify_logic(expr)

            st.write(f"**Original:** `{expr}`")
            st.write(f"**Simplified:** `{simplified}`")

            # Truth Table
            rows = []
            for values in product([0, 1], repeat=len(vars_list)):
                assignment = dict(zip(vars_sym, values))
                result = int(bool(expr.subs(assignment)))
                row = list(values) + [result]
                rows.append(row)

            df = pd.DataFrame(rows, columns=[str(v) for v in vars_sym] + ["Output"])
            st.subheader("Truth Table")
            st.dataframe(df)

            st.subheader("Logic Gate Diagram (Simplified Expression)")

            dot = Digraph(comment='Logic Circuit')

            counter = [0]

            def add_gate(node):
                node_str = str(node)
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
                    var_id = f"{node_str}_{counter[0]}"
                    dot.node(var_id, node_str)
                    counter[0] += 1
                    return var_id

            add_gate(simplified)

            st.graphviz_chart(dot)

        except Exception as e:
            st.error(f"❌ Error: {e}")
