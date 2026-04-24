"""Streamlit frontend for the safe calculator.

Run:
    streamlit run app.py
"""
import streamlit as st
from calculator import eval_expr

# ── Page config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Safe Calculator",
    page_icon="🧭",
    layout="centered",
)

# ── Styles ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .block-container { max-width: 640px; padding-top: 2rem; }
    .result-box {
        background: #1e1e2e;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        font-size: 2rem;
        font-weight: 700;
        color: #cdd6f4;
        text-align: center;
        margin-top: 0.5rem;
        letter-spacing: 0.03em;
    }
    .error-box {
        background: #3b1e1e;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        font-size: 1rem;
        color: #f38ba8;
        text-align: center;
        margin-top: 0.5rem;
    }
    .hist-row {
        display: flex;
        justify-content: space-between;
        padding: 0.3rem 0;
        border-bottom: 1px solid #313244;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session state ──────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []   # list of (expr, result_str)

# ── Header ───────────────────────────────────────────────────────────────
st.title("🧭 Safe Calculator")
st.caption(
    "Supports `+  -  *  /  //  %  **` and math functions: "
    "`sin` `cos` `tan` `sqrt` `log` `log10` `exp` `pow` — plus constants `pi` and `e`."
)
st.divider()

# ── Input ───────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])
with col_input:
    expr = st.text_input(
        label="Expression",
        placeholder="e.g. sqrt(2) * pi",
        label_visibility="collapsed",
        key="expr_input",
    )
with col_btn:
    evaluate = st.button("=", use_container_width=True, type="primary")

# ── Evaluate ─────────────────────────────────────────────────────────────────
if evaluate or expr:
    if expr.strip():
        try:
            result = eval_expr(expr.strip())
            if isinstance(result, float) and result.is_integer():
                display = str(int(result))
            else:
                display = f"{result:.10g}"
            st.markdown(f'<div class="result-box">{display}</div>', unsafe_allow_html=True)
            entry = (expr.strip(), display)
            if not st.session_state.history or st.session_state.history[0] != entry:
                st.session_state.history.insert(0, entry)
                st.session_state.history = st.session_state.history[:50]
        except ZeroDivisionError:
            st.markdown('<div class="error-box">⚠️ Division by zero</div>', unsafe_allow_html=True)
        except SyntaxError as exc:
            st.markdown(f'<div class="error-box">⚠️ Syntax error: {exc.msg}</div>', unsafe_allow_html=True)
        except ValueError as exc:
            st.markdown(f'<div class="error-box">⚠️ {exc}</div>', unsafe_allow_html=True)
        except Exception as exc:
            st.markdown(f'<div class="error-box">⚠️ {exc}</div>', unsafe_allow_html=True)

# ── Quick examples ──────────────────────────────────────────────────────────
st.divider()
st.subheader("Examples", divider=False)
examples = [
    "2 + 3 * 4",
    "sqrt(144)",
    "sin(pi / 2)",
    "log10(1000)",
    "2 ** 10",
    "(3 + 4) ** 2 - 1",
]
cols = st.columns(3)
for i, ex in enumerate(examples):
    with cols[i % 3]:
        if st.button(ex, key=f"ex_{i}", use_container_width=True):
            try:
                result = eval_expr(ex)
                if isinstance(result, float) and result.is_integer():
                    display = str(int(result))
                else:
                    display = f"{result:.10g}"
                st.session_state.history.insert(0, (ex, display))
                st.session_state.history = st.session_state.history[:50]
                st.info(f"{ex} = **{display}**")
            except Exception as exc:
                st.error(str(exc))

# ── History ───────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.divider()
    col_h, col_clr = st.columns([5, 1])
    with col_h:
        st.subheader("History")
    with col_clr:
        if st.button("Clear", key="clear_history"):
            st.session_state.history = []
            st.rerun()
    for expr_h, res_h in st.session_state.history:
        st.markdown(
            f'<div class="hist-row"><span>{expr_h}</span><strong>{res_h}</strong></div>',
            unsafe_allow_html=True,
        )

# ── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.caption("Powered by a safe AST-based evaluator — no `eval()` involved.")
