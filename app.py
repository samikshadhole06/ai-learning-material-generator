import streamlit as st
import traceback
from datetime import datetime
import json

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

# Custom CSS for professional black study website
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Merriweather:wght@300;400;700&display=swap');
    
    /* Professional black background */
    .stApp {
        background: #0a0a0a;
        font-family: 'Inter', sans-serif;
    }
    
    /* Main content area */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Elegant sidebar */
    [data-testid="stSidebar"] {
        background: #1a1a1a;
        border-right: 1px solid #2a2a2a;
    }
    
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    
    /* Professional headers */
    h1 {
        color: #ffffff !important;
        font-family: 'Merriweather', serif !important;
        font-weight: 300 !important;
        font-size: 2.8rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.5px;
        border-bottom: 2px solid #333;
        padding-bottom: 1rem;
    }
    
    h2 {
        color: #f5f5f5 !important;
        font-weight: 400 !important;
        font-size: 1.8rem !important;
        margin-top: 2.5rem !important;
        margin-bottom: 1rem !important;
        letter-spacing: -0.3px;
    }
    
    h3 {
        color: #e0e0e0 !important;
        font-weight: 500 !important;
        font-size: 1.3rem !important;
        margin-top: 1.5rem !important;
    }
    
    /* Refined buttons */
    .stButton>button {
        background: #ffffff;
        color: #0a0a0a;
        border: none;
        padding: 0.875rem 2.5rem;
        font-size: 0.95rem;
        font-weight: 600;
        border-radius: 2px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        transition: all 0.2s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        background: #f0f0f0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.4);
        transform: translateY(-1px);
    }
    
    /* Download buttons */
    .stDownloadButton>button {
        background: transparent;
        color: #ffffff;
        border: 1px solid #404040;
        padding: 0.75rem 2rem;
        font-size: 0.9rem;
        font-weight: 500;
        border-radius: 2px;
        transition: all 0.2s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stDownloadButton>button:hover {
        background: #1a1a1a;
        border-color: #ffffff;
    }
    
    /* Metrics - minimal cards */
    [data-testid="stMetric"] {
        background: #1a1a1a;
        padding: 1.5rem;
        border-radius: 2px;
        border: 1px solid #2a2a2a;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        color: #ffffff !important;
        font-weight: 300 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #888 !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
    }
    
    /* Clean tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 1px solid #2a2a2a;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #888;
        border-radius: 0;
        padding: 1rem 2rem;
        font-weight: 500;
        border: none;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.85rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent;
        color: #ffffff;
        border-bottom: 2px solid #ffffff;
    }
    
    /* File uploader - professional */
    [data-testid="stFileUploader"] {
        background: #1a1a1a;
        border-radius: 2px;
        padding: 3rem;
        border: 2px dashed #333;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #555;
        background: #1f1f1f;
    }
    
    [data-testid="stFileUploader"] label {
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
    }
    
    /* Expander - minimal */
    .streamlit-expanderHeader {
        background: #1a1a1a;
        border-radius: 2px;
        font-weight: 500;
        color: #ffffff !important;
        padding: 1rem;
        border: 1px solid #2a2a2a;
    }
    
    .streamlit-expanderHeader:hover {
        background: #1f1f1f;
    }
    
    /* Messages - clean and professional */
    .stSuccess, .stError, .stWarning, .stInfo {
        background: #1a1a1a;
        border-radius: 2px;
        padding: 1rem 1.5rem;
        border-left: 3px solid;
        color: #ffffff !important;
        font-size: 0.95rem;
    }
    
    .stSuccess {
        border-left-color: #4caf50;
    }
    
    .stError {
        border-left-color: #f44336;
    }
    
    .stWarning {
        border-left-color: #ff9800;
    }
    
    .stInfo {
        border-left-color: #2196f3;
    }
    
    /* Text styling */
    p, li, span, div {
        color: #d0d0d0;
        line-height: 1.7;
    }
    
    /* Input fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background: #1a1a1a;
        color: #ffffff;
        border: 1px solid #333;
        border-radius: 2px;
        padding: 0.75rem;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #ffffff;
        box-shadow: 0 0 0 1px #ffffff;
    }
    
    /* Radio buttons */
    .stRadio > label {
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stRadio > div {
        background: transparent !important;
    }
    
    .stRadio label[data-baseweb="radio"] {
        background: transparent !important;
        color: #d0d0d0 !important;
        padding: 0.5rem 0 !important;
    }
    
    /* Slider */
    .stSlider>div>div>div>div {
        background: #ffffff;
    }
    
    .stSlider>div>div>div {
        background: #333;
    }
    
    /* Flashcard styling - professional */
    .flashcard {
        background: #1a1a1a;
        border-radius: 2px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid #2a2a2a;
        transition: all 0.2s ease;
    }
    
    .flashcard:hover {
        border-color: #404040;
        background: #1f1f1f;
    }
    
    .flashcard-front {
        font-size: 1.1rem;
        font-weight: 400;
        color: #ffffff;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    
    /* Content cards - study material */
    .content-card {
        background: #1a1a1a;
        border-radius: 2px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        border: 1px solid #2a2a2a;
        color: #d0d0d0 !important;
    }
    
    .content-card * {
        color: #d0d0d0 !important;
    }
    
    .content-card h1, .content-card h2, .content-card h3 {
        color: #ffffff !important;
        border-bottom: 1px solid #2a2a2a;
        padding-bottom: 0.5rem;
        margin-top: 2rem !important;
    }
    
    .content-card code {
        background: #0a0a0a;
        color: #ffffff;
        padding: 0.2rem 0.5rem;
        border-radius: 2px;
        font-size: 0.9em;
    }
    
    .content-card pre {
        background: #0a0a0a;
        padding: 1rem;
        border-radius: 2px;
        border: 1px solid #2a2a2a;
        overflow-x: auto;
    }
    
    /* Scrollbar - minimal dark */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #404040;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
    /* Remove default streamlit branding colors */
    .stApp header {
        background: transparent;
    }
    
    /* Selectbox styling */
    .stSelectbox label {
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    /* Slider label */
    .stSlider label {
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title(
    "Smart Study Assistant"
)

st.markdown(
    "<p style='font-size: 1.1rem; opacity: 0.7; margin-top: -15px; font-weight: 300;'>"
    "Transform your study materials into comprehensive notes and practice quizzes"
    "</p>",
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header(
    "Study Settings"
)

st.sidebar.markdown("---")

learning_level = st.sidebar.radio(
    "Learning Level",
    ["Beginner", "Intermediate", "Advanced"],
    help="Choose based on your current knowledge"
)

st.sidebar.markdown("---")

study_mode = st.sidebar.radio(
    "Study Mode",
    ["Quick Revision", "Exam Preparation", "Detailed Study"],
    help="Select your study goal"
)

st.sidebar.markdown("---")

# Feature descriptions
with st.sidebar.expander("About These Settings"):
    st.markdown("""
    **Learning Levels:**
    - **Beginner**: Simple explanations, basic concepts
    - **Intermediate**: Balanced technical content
    - **Advanced**: Complex theory, in-depth analysis
    
    **Study Modes:**
    - **Quick Revision**: Concise key points
    - **Exam Preparation**: Focus on testable material
    - **Detailed Study**: Comprehensive coverage
    """)


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Study Material",
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
                    st.error("Could not extract text from PDF. Please ensure the PDF contains readable text.")
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
                    st.error("Failed to create text chunks. Please try a different PDF.")
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
                "Study material processed successfully"
            )

        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
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
        "Important Keywords"
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
            "Study Notes",
            "Practice Quiz",
            "Ask Questions"
        ]
    )


    # ==================================================
    # FEATURE 1: SMART NOTES
    # ==================================================

    with tab1:

        st.header(
            "Study Notes"
        )

        st.markdown(
            "<p style='opacity: 0.7; font-weight: 300;'>Generate comprehensive, level-appropriate study notes with visual aids.</p>",
            unsafe_allow_html=True
        )
        
        # Add note format options
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            generate_btn = st.button(
                "Generate Notes",
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
                    "Generating your personalized study notes..."
                ):

                    notes = generate_notes(
                        context,
                        st.session_state.keywords,
                        learning_level,
                        study_mode
                    )
                    
                    # Store notes in session state
                    st.session_state.generated_notes = notes

                st.success("Notes generated successfully")
                
            except Exception as e:
                st.error(f"Error generating notes: {str(e)}")
        
        # Display and download options if notes exist
        if 'generated_notes' in st.session_state:
            
            st.markdown("---")
            
            # Display the notes in a clean card
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown(st.session_state.generated_notes)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            col_dl1, col_dl2 = st.columns(2)
            
            with col_dl1:
                # Markdown download
                st.download_button(
                    label="Download Markdown",
                    data=st.session_state.generated_notes,
                    file_name=f"notes_{uploaded_file.name.replace('.pdf', '')}_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            with col_dl2:
                # PDF download
                try:
                    pdf_data = markdown_to_pdf(st.session_state.generated_notes)
                    st.download_button(
                        label="Download PDF",
                        data=pdf_data,
                        file_name=f"notes_{uploaded_file.name.replace('.pdf', '')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.info("PDF export coming soon")


    # ==================================================
    # FEATURE 2: INTERACTIVE QUIZ FLASHCARDS
    # ==================================================

    with tab2:

        st.header(
            "Practice Quiz"
        )

        st.markdown(
            "<p style='opacity: 0.7; font-weight: 300;'>Test your knowledge with interactive practice questions.</p>",
            unsafe_allow_html=True
        )

        col_q1, col_q2 = st.columns(2)

        with col_q1:
            difficulty = st.selectbox(
                "Difficulty Level",
                ["Easy", "Medium", "Hard"],
                key="quiz_difficulty"
            )

        with col_q2:
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
                    "Creating your personalized quiz..."
                ):

                    questions = generate_quiz(
                        context,
                        difficulty,
                        number_of_questions
                    )
                    
                    if questions:
                        st.session_state.quiz_questions = questions
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_submitted = False
                        st.success(f"Generated {len(questions)} questions")
                    else:
                        st.error("Failed to generate quiz. Please try again.")
                        
            except Exception as e:
                st.error(f"❌ Error generating quiz: {str(e)}")

        # Display flashcards if quiz exists
        if 'quiz_questions' in st.session_state and st.session_state.quiz_questions:
            
            st.markdown("---")
            
            # Quiz interface
            for idx, q in enumerate(st.session_state.quiz_questions):
                
                # Create flashcard HTML
                st.markdown(f"""
                <div class="flashcard">
                    <div class="flashcard-front">
                        <strong>Question {idx + 1}:</strong> {q['question']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Radio buttons for options
                answer_key = f"q_{idx}"
                options_list = [f"{key}. {value}" for key, value in q['options'].items()]
                
                selected = st.radio(
                    "Select your answer:",
                    options_list,
                    key=answer_key,
                    label_visibility="collapsed"
                )
                
                # Store answer
                if selected:
                    st.session_state.quiz_answers[idx] = selected[0]  # Get just the letter (A, B, C, or D)
                
                # Show answer if submitted
                if st.session_state.get('quiz_submitted', False):
                    user_answer = st.session_state.quiz_answers.get(idx, "")
                    correct_answer = q['correct_answer']
                    
                    if user_answer == correct_answer:
                        st.success(f"Correct! The answer is {correct_answer}.")
                    else:
                        st.error(f"Incorrect. The correct answer is {correct_answer}.")
                    
                    # Show explanation
                    with st.expander("Explanation"):
                        st.write(q['explanation'])
                
                st.markdown("<br>", unsafe_allow_html=True)
            
            # Submit button
            if not st.session_state.get('quiz_submitted', False):
                col_submit1, col_submit2, col_submit3 = st.columns([1, 1, 1])
                with col_submit2:
                    if st.button("Submit Quiz", key="submit_quiz", use_container_width=True):
                        st.session_state.quiz_submitted = True
                        st.rerun()
            else:
                # Show score
                correct_count = sum(
                    1 for idx, q in enumerate(st.session_state.quiz_questions)
                    if st.session_state.quiz_answers.get(idx, "") == q['correct_answer']
                )
                total = len(st.session_state.quiz_questions)
                percentage = (correct_count / total) * 100
                
                st.markdown("---")
                st.markdown(f"""
                <div class="content-card" style="text-align: center;">
                    <h2 style="color: #ffffff !important;">Your Score</h2>
                    <h1 style="color: #ffffff !important; font-size: 3rem;">{correct_count}/{total}</h1>
                    <p style="font-size: 1.5rem; color: #888 !important;">{percentage:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Try again button
                col_again1, col_again2, col_again3 = st.columns([1, 1, 1])
                with col_again2:
                    if st.button("Try New Quiz", key="new_quiz", use_container_width=True):
                        del st.session_state.quiz_questions
                        del st.session_state.quiz_answers
                        del st.session_state.quiz_submitted
                        st.rerun()


    # ==================================================
    # FEATURE 3: AI STUDY ASSISTANT
    # ==================================================

    with tab3:

        st.header(
            "Ask Questions"
        )

        st.write(
            "Ask questions from your uploaded study material"
        )

        question = st.text_input(
            "Ask your question:",
            placeholder="Example: What is Reinforcement Learning?"
        )

        if st.button(
            "Ask AI",
            key="ask_button"
        ):

            if not question.strip():

                st.warning(
                    "Please enter a question"
                )

            else:

                try:
                    # RAG disabled for cloud deployment
                    st.warning("Q&A feature requires advanced dependencies not available in free cloud deployment. Notes and Quiz features work perfectly!")
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
                        "Answer"
                    )

                    st.write(answer)

                    # Show retrieved chunks
                    with st.expander(
                        "View Retrieved Material"
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
                    st.error(f"Error answering question: {str(e)}")


else:
    # Show instructions when no file is uploaded
    st.info(
        "Please upload a PDF document to get started. "
        "The app will automatically extract text and enable all features."
    )
    
    with st.expander("How to use this app"):
        st.markdown("""
        ### Step-by-step guide:
        
        1. **Upload PDF**: Click the upload button and select your study material
        2. **Wait for processing**: The app will extract text and prepare the content
        3. **Set preferences**: Choose your learning level and study mode in the sidebar
        4. **Use features**:
           - **Study Notes**: Generate comprehensive notes
           - **Practice Quiz**: Create practice questions
           - **Ask Questions**: Get answers to specific questions
        
        ### Tips:
        - Use clear, well-formatted PDFs for best results
        - Adjust learning preferences to match your needs
        - The AI uses only your uploaded material
        - You can download generated notes
        """)