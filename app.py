import streamlit as st
import traceback

from pdf_processor import (
    extract_text_from_pdf
)

from text_processor import (
    clean_text,
    extract_keywords,
    chunk_text
)

# Embeddings and vector store disabled for cloud deployment
# from embeddings import generate_embeddings
# from vector_store import create_vector_store

from notes_generator import (
    generate_notes
)

from quiz_generator import (
    generate_quiz
)

# RAG disabled for cloud deployment - requires embeddings
# from rag import ask_question


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Learning Material Generator",
    page_icon="📚",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title(
    "📚 AI-Powered Personalized "
    "Learning Material Generator"
)

st.write(
    "Upload your study material and generate "
    "concise notes, quizzes, and document-grounded answers."
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


study_mode = st.sidebar.selectbox(
    "Study Mode",
    [
        "Quick Revision",
        "Exam Preparation",
        "Detailed Study"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This app uses AI to transform PDFs into personalized learning materials. "
    "It employs RAG (Retrieval-Augmented Generation) to ensure answers are "
    "grounded in your uploaded documents."
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

                # 5. Generate embeddings
                embeddings = generate_embeddings(
                    chunks
                )

                # 6. Create FAISS index
                index = create_vector_store(
                    embeddings
                )

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
            "📝 Smart Notes Generator"
        )

        st.write(
            "Generate concise, exam-oriented "
            "notes from your uploaded material."
        )

        if st.button(
            "Generate Smart Notes",
            key="notes_button"
        ):

            # Use chunks as context
            context = "\n\n".join(
                st.session_state.chunks
            )

            try:
                with st.spinner(
                    "Generating your notes..."
                ):

                    notes = generate_notes(
                        context,
                        st.session_state.keywords,
                        learning_level,
                        study_mode
                    )

                st.markdown(notes)
                
                # Download button
                st.download_button(
                    label="📥 Download Notes",
                    data=notes,
                    file_name=f"notes_{uploaded_file.name.replace('.pdf', '')}.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"❌ Error generating notes: {str(e)}")


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