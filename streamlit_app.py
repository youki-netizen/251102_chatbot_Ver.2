import streamlit as st
import google.generativeai as genai

# Show title and description.
st.title("📄 Document question answering (Gemini 2.5 Flash)")
st.write(
    "Upload a document below and ask a question about it – Gemini will answer! "
    "To use this app, you need to provide a Google API key for Generative AI, which you can get [here](https://aistudio.google.com/app/apikey). "
)

# Ask user for their Google API key via `st.text_input`.
api_key = st.text_input("Google Generative AI API Key", type="password")
if not api_key:
    st.info("Please add your Google Gemini API key to continue.", icon="🗝️")
else:
    genai.configure(api_key=api_key)

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:
        document = uploaded_file.read().decode()
        prompt = f"Here's a document:\n{document}\n\n---\n\n{question}"

        # Create model instance for Gemini 2.5 Flash
        model = genai.GenerativeModel("gemini-1.5-flash")  # "gemini-2.5-flash" is not public as of 2024/06

        # Generate answer
        response = model.generate_content(prompt)

        # Output answer
        st.markdown("### Answer")
        st.write(response.text if hasattr(response, "text") else response.candidates[0]['content']['parts'][0]['text'])
