import streamlit as st
import json
from src.pipeline import GrammarPipeline
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

st.set_page_config(
    page_title="Grammar Enhancer — Capstone AI",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Grammar Enhancer — Capstone AI")
st.markdown("### Correct your sentences instantly (Phases 6–10)")

# Input box
text_input = st.text_area(
    "✍️ Enter your text here:",
    height=180,
    placeholder="Example: She go to store yesterday, she buy apple."
)

# Run button
if st.button("🚀 Enhance Grammar"):
    if text_input.strip():
        st.info("Running Grammar Enhancer... please wait ⏳")
        try:
            # Initialize pipeline
            pipeline = GrammarPipeline()
            result = pipeline.run(text_input)

            corrected_text = result.get("corrected_text", "No output generated.")
            trace = result.get("trace", {})

            st.success("✅ Grammar Enhancement Complete!")
            st.subheader("📝 Corrected Output:")
            st.write(corrected_text)

            # Phase-by-phase details
            with st.expander("🔍 View Phase-by-Phase Details"):
                for phase, correction in trace.items():
                    st.markdown(f"**{phase}** → {correction}")

            # Save JSON result
            output_path = "outputs/result.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)

            st.download_button(
                label="📥 Download JSON Result",
                data=json.dumps(result, indent=4),
                file_name="grammar_result.json",
                mime="application/json"
            )

        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Please enter some text before running.")

# Footer
st.markdown("---")
st.caption("© 2025 Grammar Enhancer | Built by Jagadish 🚀")
