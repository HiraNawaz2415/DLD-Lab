import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Error Detection & Correction Codes")
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
# ---------- UTILS ----------
def calc_parity(bits, parity_type="even"):
    count = bits.count('1')
    if parity_type == "even":
        return '0' if count % 2 == 0 else '1'
    elif parity_type == "odd":
        return '1' if count % 2 == 0 else '0'
    else:
        return '?'

def xor(a, b):
    result = []
    for i in range(1, len(b)):
        result.append(str(int(a[i]) ^ int(b[i])))
    return ''.join(result)

def mod2div(dividend, divisor):
    pick = len(divisor)
    tmp = dividend[0:pick]
    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + dividend[pick]
        else:
            tmp = xor('0'*pick, tmp) + dividend[pick]
        pick += 1
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*pick, tmp)
    return tmp

def hamming74_encode(data_bits):
    d = [int(b) for b in data_bits]
    p1 = d[0] ^ d[1] ^ d[3]
    p2 = d[0] ^ d[2] ^ d[3]
    p3 = d[1] ^ d[2] ^ d[3]
    code = f"{p1}{p2}{d[0]}{p3}{d[1]}{d[2]}{d[3]}"
    return code

def hamming74_decode(code_bits):
    c = [int(b) for b in code_bits]
    p1 = c[0]
    p2 = c[1]
    d1 = c[2]
    p3 = c[3]
    d2 = c[4]
    d3 = c[5]
    d4 = c[6]

    s1 = p1 ^ d1 ^ d2 ^ d4
    s2 = p2 ^ d1 ^ d3 ^ d4
    s3 = p3 ^ d2 ^ d3 ^ d4

    error_position = s3*4 + s2*2 + s1*1

    corrected = list(c)
    if error_position != 0:
        corrected[error_position - 1] ^= 1  # Flip the bit

    decoded = f"{corrected[2]}{corrected[4]}{corrected[5]}{corrected[6]}"
    return error_position, decoded

def checksum_16bit(data):
    blocks = [data[i:i+16] for i in range(0, len(data), 16)]
    sum_int = sum(int(block, 2) for block in blocks)
    sum_bin = bin(sum_int)[2:]
    if len(sum_bin) > 16:
        carry = int(sum_bin[:-16], 2)
        sum_int = int(sum_bin[-16:], 2) + carry
    checksum = bin(~sum_int & 0xFFFF)[2:].zfill(16)
    return checksum

def make_download_button(content, filename):
    b = BytesIO()
    b.write(content.encode())
    b.seek(0)
    return b

# ---------- APP ----------
st.title("🛡️ Error Detection & Correction Codes")

st.markdown("""
### ✅ Covered:
- Parity Bit
- CRC
- Hamming [7,4]
- Simple 16-bit Checksum
- Download your output!
""")

# --- 1) Parity Bit ---
st.header("1️⃣ Parity Bit")

data_bits = st.text_input("Data Bits for Parity (e.g., 1010110)")
parity_type = st.selectbox("Parity Type", ["even", "odd"], key="parity")

if data_bits:
    parity = calc_parity(data_bits, parity_type)
    full_word = data_bits + parity
    st.write(f"Parity Bit: **{parity}** → Full Word: `{full_word}`")
    st.download_button("⬇️ Download Parity Word", data=make_download_button(full_word, "parity.txt"), file_name="parity_word.txt")

# --- 2) CRC ---
st.header("2️⃣ CRC Generator")

crc_data = st.text_input("Data Bits for CRC (e.g., 100100)")
crc_key = st.text_input("Generator Polynomial (Key) (e.g., 1101)")

if crc_data and crc_key:
    appended_data = crc_data + '0'*(len(crc_key)-1)
    remainder = mod2div(appended_data, crc_key)
    crc_code = crc_data + remainder
    st.write(f"Remainder: `{remainder}` → Transmitted Word: `{crc_code}`")
    st.download_button("⬇️ Download CRC Word", data=make_download_button(crc_code, "crc.txt"), file_name="crc_word.txt")

# --- 3) Hamming [7,4] ---
st.header("3️⃣ Hamming [7,4] Encoder/Decoder")

hamming_input = st.text_input("4-bit Data to Encode (e.g., 1011)")

if hamming_input and len(hamming_input) == 4:
    encoded = hamming74_encode(hamming_input)
    st.write(f"Encoded [7,4]: `{encoded}`")
    st.download_button("⬇️ Download Encoded", data=make_download_button(encoded, "hamming.txt"), file_name="hamming_encoded.txt")

hamming_decode = st.text_input("7-bit Code to Decode (e.g., 0110011)")

if hamming_decode and len(hamming_decode) == 7:
    error_pos, decoded = hamming74_decode(hamming_decode)
    if error_pos == 0:
        st.success(f"No Error! Decoded Data: `{decoded}`")
    else:
        st.warning(f"Error at position: {error_pos} → Corrected Data: `{decoded}`")
    st.download_button("⬇️ Download Decoded", data=make_download_button(decoded, "hamming_decoded.txt"), file_name="hamming_decoded.txt")

# --- 4) Simple Checksum ---
st.header("4️⃣ Simple 16-bit Checksum")

checksum_input = st.text_input("Data Bits (multiple of 16 recommended, e.g., 1010100010101010)")

if checksum_input and len(checksum_input) >= 16:
    cs = checksum_16bit(checksum_input)
    st.write(f"Checksum: `{cs}`")
    st.download_button("⬇️ Download Checksum", data=make_download_button(cs, "checksum.txt"), file_name="checksum.txt")

st.markdown("---\n✅ Made with ❤️ for your Digital Logic Design Lab.")
