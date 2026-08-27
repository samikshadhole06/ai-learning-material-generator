from gemini_service import generate_response


def generate_notes(context, keywords, learning_level, study_mode):
    """
    Generate comprehensive, well-structured study notes.
    """

    # Build level-specific instructions
    level_guide = ""
    if learning_level == "Beginner":
        level_guide = """
Use SIMPLE language. Define ALL technical terms. Include many examples.
Break down complex ideas into simple steps. Use analogies to explain."""
    elif learning_level == "Intermediate":
        level_guide = """
Balance technical and simple language. Connect concepts together.
Show practical applications. Include detailed explanations."""
    else:  # Advanced
        level_guide = """
Use precise technical terminology. Explore complex relationships.
Include advanced theory and in-depth analysis. Discuss edge cases."""

    # Build mode-specific instructions
    mode_guide = ""
    if study_mode == "Quick Revision":
        mode_guide = """
Format: Clear bullet points, key facts highlighted, quick-reference tables.
Include memory aids. Focus on must-know information."""
    elif study_mode == "Exam Preparation":
        mode_guide = """
Format: Focus on exam-relevant topics. Highlight commonly tested concepts.
Include tips and tricks. Provide comprehensive coverage."""
    else:  # Detailed Study
        mode_guide = """
Format: Provide extensive explanations with background context.
Include multiple examples per concept. Add additional insights."""

    prompt = f"""You are creating study notes from the material below.

IMPORTANT RULES:
1. Cover ALL the material provided - be comprehensive and thorough
2. Do NOT summarize or skip content - include all important information
3. Make notes COMPLETE and DETAILED

STUDENT LEVEL: {learning_level}
{level_guide}

STUDY MODE: {study_mode}  
{mode_guide}

KEY TOPICS: {", ".join(keywords[:20])}

FORMATTING:
- Use # ## ### for headers
- Use bullet points and numbered lists
- Include visual elements:
  * Flowcharts with arrows: → ↓ ← ↑
  * Boxes: ┌─┐ │ └─┘
  * Tables with | and -
- Add callouts:
  * 💡 Key Concept
  * ⚠️ Important
  * 📝 Example
  * ✅ Remember

MATERIAL TO CONVERT INTO NOTES:
{context}

CREATE COMPREHENSIVE STUDY NOTES - cover everything, make it detailed and complete:"""

    # Use higher token limit for longer notes
    return generate_response(prompt, temperature=0.3, max_tokens=8000)