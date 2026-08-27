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

# Custom CSS for modern, clean UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Modern gradient background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Main content area - card style */
    .main .block-container {
        padding: 2rem;
        max-width: 1200px;
    }
    
    /* Clean white sidebar */
    [data-testid="stSidebar"] {
        background: white;
        box-shadow: 2px 0 10px rgba(0,0,0,0.1);
    }
    
    [data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }
    
    /* Headers - Modern style */
    h1 {
        color: white !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    h2 {
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.8rem !important;
        margin-top: 2rem !important;
    }
    
    h3 {
        color: white !important;
        font-weight: 500 !important;
        font-size: 1.3rem !important;
    }
    
    /* Modern buttons */
    .stButton>button {
        background: white;
        color: #667eea;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 50px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Download buttons */
    .stDownloadButton>button {
        background: rgba(255,255,255,0.2);
        color: white;
        border: 2px solid white;
        padding: 0.6rem 1.5rem;
        font-size: 0.9rem;
        font-weight: 600;
        border-radius: 50px;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton>button:hover {
        background: white;
        color: #667eea;
    }
    
    /* Metrics - Card style */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.95);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        color: #667eea !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #666 !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    /* Tabs - Clean modern style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.2);
        color: white;
        border-radius: 10px 10px 0 0;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: #667eea;
    }
    
    /* File uploader - Modern card */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.95);
        border-radius: 15px;
        padding: 2rem;
        border: 3px dashed rgba(102, 126, 234, 0.3);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #667eea;
        background: white;
    }
    
    /* Expander - Card style */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.95);
        border-radius: 10px;
        font-weight: 600;
        color: #667eea !important;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    details[open] > .streamlit-expanderHeader {
        border-radius: 10px 10px 0 0;
    }
    
    /* Messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        background: rgba(255,255,255,0.95);
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid;
        color: #1a1a1a !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stSuccess {
        border-left-color: #00c851;
    }
    
    .stError {
        border-left-color: #ff4444;
    }
    
    .stWarning {
        border-left-color: #ffbb33;
    }
    
    .stInfo {
        border-left-color: #33b5e5;
    }
    
    /* Text content in white cards */
    p, li, span, div {
        color: white;
    }
    
    /* Input fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background: white;
        color: #1a1a1a;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 0.75rem;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Slider */
    .stSlider>div>div>div>div {
        background: #667eea;
    }
    
    /* Flashcard styling */
    .flashcard {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .flashcard:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
    }
    
    .flashcard-front {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 1rem;
    }
    
    .flashcard-options {
        margin: 1rem 0;
    }
    
    .flashcard-option {
        background: #f5f5f5;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 4px solid transparent;
        transition: all 0.2s ease;
    }
    
    .flashcard-option:hover {
        background: #e8e8e8;
        border-left-color: #667eea;
    }
    
    .flashcard-option.correct {
        background: #d4edda;
        border-left-color: #00c851;
        color: #155724;
    }
    
    .flashcard-option.incorrect {
        background: #f8d7da;
        border-left-color: #ff4444;
        color: #721c24;
    }
    
    /* Content cards */
    .content-card {
        background: rgba(255,255,255,0.95);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #1a1a1a !important;
    }
    
    .content-card * {
        color: #1a1a1a !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255,255,255,0.5);
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title(
    "📚 Smart Study Assistant"
)

st.markdown(
    "<p style='font-size: 1.2rem; opacity: 0.9; margin-top: -15px;'>"
    "Transform PDFs into comprehensive notes and interactive quizzes"
    "</p>",
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header(
    "⚙️ Study Settings"
)

st.sidebar.markdown("---")

learning_level = st.sidebar.radio(
    "📊 Learning Level",
    ["Beginner", "Intermediate", "Advanced"],
    help="Choose based on your current knowledge"
)

st.sidebar.markdown("---")

study_mode = st.sidebar.radio(
    "🎯 Study Mode",
    ["Quick Revision", "Exam Preparation", "Detailed Study"],
    help="Select your study goal"
)

st.sidebar.markdown("---")

# Feature descriptions
with st.sidebar.expander("ℹ️ What do these mean?"):
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
            
            # Display the notes in a clean card
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown(st.session_state.generated_notes)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            col_dl1, col_dl2 = st.columns(2)
            
            with col_dl1:
                # Markdown download
                st.download_button(
                    label="📥 Download Markdown",
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
                        label="📥 Download PDF",
                        data=pdf_data,
                        file_name=f"notes_{uploaded_file.name.replace('.pdf', '')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.info("PDF export coming soon!")


    # ==================================================
    # FEATURE 2: INTERACTIVE QUIZ FLASHCARDS
    # ==================================================

    with tab2:

        st.header(
            "🧠 Interactive Quiz Flashcards"
        )

        st.markdown(
            "<p style='font-size: 1.1rem; opacity: 0.9;'>Test your knowledge with interactive flashcard-style questions.</p>",
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
                    "🎯 Creating your personalized quiz flashcards..."
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
                        st.success(f"✅ Generated {len(questions)} questions!")
                    else:
                        st.error("❌ Failed to generate quiz. Please try again.")
                        
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
                        st.success(f"✅ Correct! The answer is {correct_answer}.")
                    else:
                        st.error(f"❌ Incorrect. The correct answer is {correct_answer}.")
                    
                    # Show explanation
                    with st.expander("📖 Explanation"):
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
                    <h2 style="color: #667eea !important;">📊 Your Score</h2>
                    <h1 style="color: #667eea !important; font-size: 3rem;">{correct_count}/{total}</h1>
                    <p style="font-size: 1.5rem; color: #666 !important;">{percentage:.1f}%</p>
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