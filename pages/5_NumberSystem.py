import streamlit as st
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
st.title("🔢 Number System Module")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "Base Converter",
        "Binary Arithmetic",
        "Signed Representation",
        "BCD",
        "Gray Code",
        "BCD Addition",
        "Gray Code Addition"
    ]
)

# -------------------------------
# Tab 1: Base Converter
# -------------------------------
with tab1:
    st.subheader("Flexible Base Converter")

    number = st.text_input("Enter Number to Convert:")
    from_base = st.selectbox("From Base:", ["Decimal", "Binary", "Octal", "Hexadecimal"])
    to_base = st.selectbox(
        "To Base:",
        ["Decimal", "Binary", "Octal", "Hexadecimal"]
    )

    if number:
        try:
            if from_base == "Decimal":
                dec = int(number)
            elif from_base == "Binary":
                dec = int(number, 2)
            elif from_base == "Octal":
                dec = int(number, 8)
            elif from_base == "Hexadecimal":
                dec = int(number, 16)

            if to_base == "Decimal":
                result = str(dec)
            elif to_base == "Binary":
                result = bin(dec)[2:]
            elif to_base == "Octal":
                result = oct(dec)[2:]
            elif to_base == "Hexadecimal":
                result = hex(dec)[2:].upper()

            st.write(f"**Converted Result:** {result}")

        except:
            st.error("Invalid input for the chosen base.")

# -------------------------------
# Tab 2: Binary Arithmetic
# -------------------------------
with tab2:
    st.subheader("Binary Arithmetic")
    num1 = st.text_input("First Binary Number:", key="bin1")
    num2 = st.text_input("Second Binary Number:", key="bin2")
    operation = st.selectbox("Operation:", ["Addition", "Subtraction", "Multiplication", "Division"])

    if num1 and num2:
        try:
            a = int(num1, 2)
            b = int(num2, 2)

            if operation == "Addition":
                result = bin(a + b)[2:]
            elif operation == "Subtraction":
                result = bin(abs(a - b))[2:]
            elif operation == "Multiplication":
                result = bin(a * b)[2:]
            elif operation == "Division":
                result = bin(a // b)[2:] if b != 0 else "Undefined (division by zero)"

            st.write(f"**Result:** {result}")

        except:
            st.error("Invalid binary numbers.")

# -------------------------------
# Tab 3: Signed Representation
# -------------------------------
with tab3:
    st.subheader("Signed Number Representation")
    number = st.number_input("Enter Decimal Number:", step=1)
    bits = st.slider("Bit Length", min_value=4, max_value=16, value=8)

    if number:
        n = int(number)

        sign_mag = f"{0 if n >=0 else 1}{bin(abs(n))[2:].zfill(bits-1)}"
        ones_comp = ''.join('1' if b == '0' else '0' for b in bin(abs(n))[2:].zfill(bits)) if n < 0 else bin(n)[2:].zfill(bits)
        twos_comp = bin((1 << bits) + n)[2:] if n < 0 else bin(n)[2:].zfill(bits)

        st.write(f"**Sign Magnitude ({bits}-bit):** {sign_mag}")
        st.write(f"**1's Complement ({bits}-bit):** {ones_comp}")
        st.write(f"**2's Complement ({bits}-bit):** {twos_comp}")

# -------------------------------
# Tab 4: BCD Converter
# -------------------------------
with tab4:
    st.subheader("BCD Converter")
    dec = st.number_input("Enter Decimal Number:", step=1, key="bcd")
    if dec >= 0:
        bcd = ' '.join([bin(int(d))[2:].zfill(4) for d in str(int(dec))])
        st.write(f"**BCD Code:** {bcd}")

# -------------------------------
# Tab 5: Gray Code Converter
# -------------------------------
with tab5:
    st.subheader("Gray Code Converter")
    binary = st.text_input("Enter Binary Number:", key="gray_input")
    if binary:
        try:
            n = int(binary, 2)
            gray = n ^ (n >> 1)
            st.write(f"**Gray Code:** {bin(gray)[2:]}")

            gray_input = st.text_input("Enter Gray Code to convert to Binary:", key="gray_to_bin")
            if gray_input:
                gray_n = int(gray_input, 2)
                mask = gray_n
                result = 0
                while mask:
                    result ^= mask
                    mask >>= 1
                st.write(f"**Binary:** {bin(result)[2:]}")
        except:
            st.error("Invalid binary input.")

# -------------------------------
# Tab 6: BCD Addition
# -------------------------------
with tab6:
    st.subheader("BCD Addition")
    dec1 = st.number_input("First Decimal Number:", step=1, key="bcd1")
    dec2 = st.number_input("Second Decimal Number:", step=1, key="bcd2")

    if dec1 >= 0 and dec2 >= 0:
        sum_dec = int(dec1) + int(dec2)
        bcd1 = ' '.join([bin(int(d))[2:].zfill(4) for d in str(int(dec1))])
        bcd2 = ' '.join([bin(int(d))[2:].zfill(4) for d in str(int(dec2))])
        bcd_sum = ' '.join([bin(int(d))[2:].zfill(4) for d in str(sum_dec)])

        st.write(f"**First Number BCD:** {bcd1}")
        st.write(f"**Second Number BCD:** {bcd2}")
        st.write(f"**Sum in Decimal:** {sum_dec}")
        st.write(f"**Sum in BCD:** {bcd_sum}")

# -------------------------------
# Tab 7: Gray Code Addition
# -------------------------------
with tab7:
    st.subheader("Gray Code Addition")
    gray1 = st.text_input("First Gray Code:", key="gray_add1")
    gray2 = st.text_input("Second Gray Code:", key="gray_add2")

    if gray1 and gray2:
        try:
            def gray_to_binary(gray):
                num = int(gray, 2)
                mask = num
                result = 0
                while mask:
                    result ^= mask
                    mask >>= 1
                return result

            def binary_to_gray(n):
                return n ^ (n >> 1)

            bin1 = gray_to_binary(gray1)
            bin2 = gray_to_binary(gray2)
            sum_bin = bin1 + bin2
            sum_gray = binary_to_gray(sum_bin)

            st.write(f"**First Gray ➜ Binary:** {bin(bin1)[2:]}")
            st.write(f"**Second Gray ➜ Binary:** {bin(bin2)[2:]}")
            st.write(f"**Sum in Binary:** {bin(sum_bin)[2:]}")
            st.write(f"**Sum in Gray Code:** {bin(sum_gray)[2:]}")

        except:
            st.error("Invalid Gray code input.")
