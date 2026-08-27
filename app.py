import streamlit as st
import traceback
from datetime import datetime

from pdf_processor import (
    extract_text_from_pdf
)

from text_processor import (
    clean_text,
    extract_keywords,
    chunk_text
)

from notes_generator import (
    generate_notes
)

from quiz_generator import (
    generate_quiz
)

from pdf_generator import (
    markdown_to_pdf
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Learning Material Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for elegant black formal UI
st.markdown("""
<style>
    /* Main theme - Elegant black and white */
    .stApp {
        background: linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%);
        color: #ffffff;
    }
    
    /* Sidebar styling - Clean white */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
        border-right: 1px solid #e0e0e0;
    }
    
    [data-testid="stSidebar"] * {
        color: #000000 !important;
    }
    
    /* Headers - Gold accent for elegance */
    h1 {
        color: #ffffff !important;
        font-weight: 300 !important;
        letter-spacing: 2px;
        font-family: 'Georgia', serif;
        border-bottom: 2px solid #d4af37;
        padding-bottom: 10px;
    }
    
    h2 {
        color: #f0f0f0 !important;
        font-weight: 400 !important;
        letter-spacing: 1px;
        margin-top: 1.5rem;
    }
    
    h3 {
        color: #d0d0d0 !important;
        font-weight: 500 !important;
    }
    
    /* Buttons - Minimalist black with gold hover */
    .stButton>button {
        background-color: #000000;
        color: #ffffff;
        border: 2px solid #d4af37;
        padding: 0.75rem 2.5rem;
        font-size: 1rem;
        font-weight: 500;
        letter-spacing: 1px;
        border-radius: 0px;
        transition: all 0.3s ease;
        text-transform: uppercase;
    }
    
    .stButton>button:hover {
        background-color: #d4af37;
        color: #000000;
        border-color: #d4af37;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
    }
    
    /* Download buttons - White variant */
    .stDownloadButton>button {
        background-color: #ffffff;
        color: #000000;
        border: 2px solid #000000;
        padding: 0.6rem 2rem;
        font-size: 0.95rem;
        font-weight: 500;
        letter-spacing: 0.5px;
        border-radius: 0px;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton>button:hover {
        background-color: #000000;
        color: #ffffff;
        border-color: #d4af37;
    }
    
    /* Metrics - Gold accents */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        color: #d4af37;
        font-weight: 300;
    }
    
    [data-testid="stMetricLabel"] {
        color: #cccccc !important;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Tabs - Minimalist design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: transparent;
        border-bottom: 1px solid #333333;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #888888;
        border: none;
        padding: 1rem 2rem;
        font-weight: 500;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-size: 0.9rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        color: #d4af37;
        border-bottom: 3px solid #d4af37;
    }
    
    /* File uploader - Elegant box */
    [data-testid="stFileUploader"] {
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 0px;
        padding: 2.5rem;
        border: 2px dashed #444444;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #d4af37;
        background-color: rgba(212, 175, 55, 0.05);
    }
    
    /* Expander - Clean design */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 0px;
        border-left: 3px solid #d4af37;
        font-weight: 500;
        color: #ffffff !important;
        letter-spacing: 0.5px;
    }
    
    /* Text content - High readability */
    p, li, span {
        color: #e0e0e0 !important;
        line-height: 1.7;
    }
    
    /* Success/Error boxes - Refined */
    .stSuccess {
        background-color: rgba(76, 175, 80, 0.1);
        border-left: 4px solid #4caf50;
        color: #ffffff !important;
        border-radius: 0px;
    }
    
    .stError {
        background-color: rgba(244, 67, 54, 0.1);
        border-left: 4px solid #f44336;
        color: #ffffff !important;
        border-radius: 0px;
    }
    
    .stWarning {
        background-color: rgba(255, 193, 7, 0.1);
        border-left: 4px solid #ffc107;
        color: #ffffff !important;
        border-radius: 0px;
    }
    
    /* Info box - Gold accent */
    .stInfo {
        background-color: rgba(212, 175, 55, 0.1);
        border-left: 4px solid #d4af37;
        color: #ffffff !important;
        border-radius: 0px;
    }
    
    /* Input fields */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.05);
        color: #ffffff;
        border: 1px solid #444444;
        border-radius: 0px;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #d4af37;
        box-shadow: 0 0 0 1px #d4af37;
    }
    
    /* Selectbox */
    .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.05);
        color: #ffffff;
        border: 1px solid #444444;
        border-radius: 0px;
    }
    
    /* Slider */
    .stSlider>div>div>div>div {
        background-color: #d4af37;
    }
    
    /* Markdown content styling */
    .element-container code {
        background-color: rgba(255, 255, 255, 0.08);
        color: #d4af37;
        padding: 2px 6px;
        border-radius: 3px;
        font-family: 'Courier New', monospace;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #444444;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #d4af37;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title(
    "📚 AI Learning Material Generator"
)

st.markdown(
    "<p style='font-size: 1.1rem; color: #cccccc; margin-top: -10px;'>"
    "Transform your study materials into comprehensive notes with diagrams, flowcharts, and level-appropriate content."
    "</p>",
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header(
    "⚙️ Learning Preferences"
)

learning_level = st.sidebar.selectbox(
    "Learning Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

# Show level-specific features
level_features = {
    "Beginner": "✓ Simple language\n✓ Basic concepts\n✓ Clear examples\n✓ Foundational knowledge",
    "Intermediate": "✓ Technical terms\n✓ Practical applications\n✓ Connected concepts\n✓ Detailed examples",
    "Advanced": "✓ Advanced theory\n✓ Complex analysis\n✓ In-depth coverage\n✓ Edge cases"
}

with st.sidebar.expander("📊 Level Features"):
    st.markdown(level_features[learning_level])

study_mode = st.sidebar.selectbox(
    "Study Mode",
    [
        "Quick Revision",
        "Exam Preparation",
        "Detailed Study"
    ]
)

# Show mode-specific features
mode_features = {
    "Quick Revision": "✓ Concise bullet points\n✓ Key facts\n✓ Quick reference\n✓ Memory aids",
    "Exam Preparation": "✓ Exam-focused\n✓ Sample questions\n✓ Common topics\n✓ Tips & tricks",
    "Detailed Study": "✓ In-depth explanations\n✓ Background context\n✓ Extended examples\n✓ Additional insights"
}

with st.sidebar.expander("🎯 Mode Features"):
    st.markdown(mode_features[study_mode])

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ About")
st.sidebar.info(
    "**AI Learning Material Generator**\n\n"
    "Transform your PDFs into:\n"
    "• Comprehensive study notes\n"
    "• Visual diagrams & flowcharts\n"
    "• Practice quizzes\n"
    "• Level-appropriate content\n\n"
    "Powered by Gemini AI"
)


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "📄 Upload your study material",
    type=["pdf"],
    help="Upload a PDF document containing your study material"
)


# --------------------------------------------------
# PROCESS PDF
# --------------------------------------------------

if uploaded_file:

    # Check whether this is a new file
    file_id = (
        uploaded_file.name,
        uploaded_file.size
    )

    if (
        "file_id"
        not in st.session_state
        or st.session_state.file_id
        != file_id
    ):

        try:
            with st.spinner(
                "Processing your study material..."
            ):

                # 1. Extract text
                raw_text = (
                    extract_text_from_pdf(
                        uploaded_file
                    )
                )

                if not raw_text.strip():
                    st.error("❌ Could not extract text from PDF. Please ensure the PDF contains readable text.")
                    st.stop()

                # 2. Clean text
                cleaned_text = clean_text(
                    raw_text
                )

                # 3. Extract keywords
                keywords = extract_keywords(
                    cleaned_text
                )

                # 4. Create chunks
                chunks = chunk_text(
                    cleaned_text
                )

                if not chunks:
                    st.error("❌ Failed to create text chunks. Please try a different PDF.")
                    st.stop()

                # Embeddings disabled for cloud deployment
                # embeddings = generate_embeddings(chunks)
                # index = create_vector_store(embeddings)
                embeddings = None
                index = None

                # Store everything
                st.session_state.file_id = file_id

                st.session_state.raw_text = (
                    raw_text
                )

                st.session_state.cleaned_text = (
                    cleaned_text
                )

                st.session_state.keywords = (
                    keywords
                )

                st.session_state.chunks = (
                    chunks
                )

                st.session_state.index = (
                    index
                )

            st.success(
                "✅ Study material processed successfully!"
            )

        except Exception as e:
            st.error(f"❌ Error processing PDF: {str(e)}")
            st.error("Please try uploading a different PDF or check the error log.")
            with st.expander("See error details"):
                st.code(traceback.format_exc())
            st.stop()


# --------------------------------------------------
# SHOW DOCUMENT INFORMATION
# --------------------------------------------------

if (
    "chunks"
    in st.session_state
):

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Characters",
            len(
                st.session_state.cleaned_text
            )
        )

    with col2:

        st.metric(
            "Chunks",
            len(
                st.session_state.chunks
            )
        )

    with col3:

        st.metric(
            "Keywords",
            len(
                st.session_state.keywords
            )
        )


    # --------------------------------------------------
    # KEYWORDS
    # --------------------------------------------------

    with st.expander(
        "🔑 Important Keywords"
    ):

        st.write(
            ", ".join(
                st.session_state.keywords
            )
        )


    # --------------------------------------------------
    # THREE MAIN FEATURES
    # --------------------------------------------------

    tab1, tab2, tab3 = st.tabs(
        [
            "📝 Smart Notes",
            "🧠 Quiz Generator",
            "💬 Ask AI"
        ]
    )


    # ==================================================
    # FEATURE 1: SMART NOTES
    # ==================================================

    with tab1:

        st.header(
            "📝 Professional Study Notes"
        )

        st.markdown(
            "<p style='color: #cccccc;'>Generate comprehensive, level-appropriate notes with diagrams, flowcharts, and visual aids.</p>",
            unsafe_allow_html=True
        )
        
        # Add note format options
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            generate_btn = st.button(
                "Generate Smart Notes",
                key="notes_button",
                use_container_width=True
            )
        
        if generate_btn:

            # Use chunks as context
            context = "\n\n".join(
                st.session_state.chunks
            )

            try:
                with st.spinner(
                    "✨ Generating your personalized notes with diagrams and flowcharts..."
                ):

                    notes = generate_notes(
                        context,
                        st.session_state.keywords,
                        learning_level,
                        study_mode
                    )
                    
                    # Store notes in session state
                    st.session_state.generated_notes = notes

                st.success("✅ Notes generated successfully!")
                
            except Exception as e:
                st.error(f"❌ Error generating notes: {str(e)}")
        
        # Display and download options if notes exist
        if 'generated_notes' in st.session_state:
            
            st.markdown("---")
            st.markdown("### 📄 Generated Notes")
            
            # Display the notes
            st.markdown(st.session_state.generated_notes)
            
            st.markdown("---")
            st.markdown("### 💾 Download Options")
            
            col_dl1, col_dl2 = st.columns(2)
            
            with col_dl1:
                # Markdown download
                st.download_button(
                    label="📥 Download as Markdown",
                    data=st.session_state.generated_notes,
                    file_name=f"notes_{uploaded_file.name.replace('.pdf', '')}_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            with col_dl2:
                # PDF download
                try:
                    pdf_data = markdown_to_pdf(st.session_state.generated_notes)
                    st.download_button(
                        label="📥 Download as PDF",
                        data=pdf_data,
                        file_name=f"notes_{uploaded_file.name.replace('.pdf', '')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.warning(f"PDF generation currently unavailable: {str(e)}")


    # ==================================================
    # FEATURE 2: QUIZ
    # ==================================================

    with tab2:

        st.header(
            "🧠 Quiz & MCQ Generator"
        )

        difficulty = st.selectbox(
            "Select Difficulty",
            [
                "Easy",
                "Medium",
                "Hard"
            ],
            key="quiz_difficulty"
        )

        number_of_questions = st.slider(
            "Number of Questions",
            min_value=3,
            max_value=10,
            value=5
        )

        if st.button(
            "Generate Quiz",
            key="quiz_button"
        ):

            context = "\n\n".join(
                st.session_state.chunks
            )

            try:
                with st.spinner(
                    "Generating questions..."
                ):

                    quiz = generate_quiz(
                        context,
                        difficulty,
                        number_of_questions
                    )

                st.markdown(quiz)
                
                # Download button
                st.download_button(
                    label="📥 Download Quiz",
                    data=quiz,
                    file_name=f"quiz_{uploaded_file.name.replace('.pdf', '')}.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"❌ Error generating quiz: {str(e)}")


    # ==================================================
    # FEATURE 3: AI STUDY ASSISTANT
    # ==================================================

    with tab3:

        st.header(
            "💬 AI Study Assistant"
        )

        st.write(
            "Ask questions from your uploaded "
            "study material."
        )

        question = st.text_input(
            "Ask your question:",
            placeholder=(
                "Example: What is "
                "Reinforcement Learning?"
            )
        )

        if st.button(
            "Ask AI",
            key="ask_button"
        ):

            if not question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                try:
                    # RAG disabled for cloud deployment
                    st.warning("⚠️ Q&A feature requires advanced dependencies not available in free cloud deployment. Notes and Quiz features work perfectly!")
                    answer = "This feature requires sentence-transformers and FAISS which are too large for free Streamlit Cloud. Please use Notes or Quiz features instead!"
                    sources = []
                    
                    # Original code (disabled):
                    # with st.spinner("Searching your study material..."):
                    #     answer, sources = ask_question(
                    #         question,
                    #         st.session_state.index,
                    #         st.session_state.chunks
                    #     )

                    st.subheader(
                        "🤖 Answer"
                    )

                    st.write(answer)

                    # Show retrieved chunks
                    with st.expander(
                        "🔎 View Retrieved Material"
                    ):

                        for i, source in enumerate(
                            sources,
                            start=1
                        ):

                            st.markdown(
                                f"**Source Chunk {i}** (Relevance Score: {source['score']:.4f})"
                            )

                            st.write(
                                source["text"]
                            )

                            st.divider()
                            
                except Exception as e:
                    st.error(f"❌ Error answering question: {str(e)}")


else:
    # Show instructions when no file is uploaded
    st.info(
        "👆 Please upload a PDF document to get started. "
        "The app will automatically extract text, generate embeddings, "
        "and enable all features."
    )
    
    with st.expander("ℹ️ How to use this app"):
        st.markdown("""
        ### Step-by-step guide:
        
        1. **Upload PDF**: Click the upload button and select your study material
        2. **Wait for processing**: The app will extract text and prepare the content
        3. **Set preferences**: Choose your learning level and study mode in the sidebar
        4. **Use features**:
           - **Smart Notes**: Generate summarized notes
           - **Quiz Generator**: Create practice questions
           - **Ask AI**: Get answers to specific questions
        
        ### Tips:
        - Use clear, well-formatted PDFs for best results
        - Adjust learning preferences to match your needs
        - The AI uses only your uploaded material (no external information)
        - You can download generated notes and quizzes
        """)