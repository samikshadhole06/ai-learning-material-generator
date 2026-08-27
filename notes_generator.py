from gemini_service import generate_response


def generate_notes(context, keywords, learning_level, study_mode):
    """
    Generate comprehensive, well-structured study notes.
    """

    prompt = f"""You are an expert educator creating comprehensive study notes.

IMPORTANT: Generate COMPLETE and DETAILED notes covering ALL the material provided. Do not summarize too much.

LEARNING LEVEL: {learning_level}
STUDY MODE: {study_mode}
KEY TOPICS: {", ".join(keywords[:15])}

CONTENT REQUIREMENTS:

1. **Comprehensive Coverage**: Include ALL important concepts, definitions, and details from the material
2. **Clear Structure**: Use hierarchical organization with main topics and subtopics
3. **Visual Elements**: Include diagrams, flowcharts, and tables where appropriate
4. **Examples**: Provide concrete examples for each major concept
5. **Complete Information**: Don't skip details - be thorough and comprehensive

FORMATTING GUIDELINES:

**Headers and Structure:**
- # for main sections
- ## for major topics
- ### for subtopics
- Use bullet points for lists
- Use numbered lists for sequences/steps

**Visual Elements (use ASCII art):**
- Flowcharts with arrows: → ↓ ← ↑
- Boxes: ┌─┐ │ └─┘
- Tables with | and -
- Diagrams showing relationships

**Special Callouts:**
- 💡 **Key Concept:** For fundamental ideas
- ⚠️ **Important:** For critical information
- 📝 **Example:** For practical examples
- 🔍 **Deep Dive:** For detailed explanations
- ✅ **Remember:** For key takeaways

**Content Depth by Level:**

{f'''BEGINNER Level:
- Use simple, accessible language
- Define every technical term
- Include many examples
- Break down complex concepts
- Use analogies and comparisons
- Step-by-step explanations''' if learning_level == "Beginner" else ''}

{f'''INTERMEDIATE Level:
- Balance technical and accessible language
- Connect concepts together
- Show practical applications
- Include comparisons and contrasts
- Provide detailed explanations
- Mix theory with practice''' if learning_level == "Intermediate" else ''}

{f'''ADVANCED Level:
- Use precise technical terminology
- Explore complex relationships
- Include advanced theory
- Provide in-depth analysis
- Discuss edge cases and limitations
- Connect to broader context''' if learning_level == "Advanced" else ''}

**Content Style by Mode:**

{f'''QUICK REVISION Mode:
- Clear, concise bullet points
- Highlight key facts and formulas
- Include quick-reference tables
- Use bold for important terms
- Memory aids and mnemonics
- Summary boxes''' if study_mode == "Quick Revision" else ''}

{f'''EXAM PREPARATION Mode:
- Focus on testable material
- Include practice questions inline
- Highlight common exam topics
- Provide tips and tricks
- Show common mistakes to avoid
- Comprehensive coverage of syllabus''' if study_mode == "Exam Preparation" else ''}

{f'''DETAILED STUDY Mode:
- Extensive explanations
- Background and context
- Multiple examples per concept
- Related topics and connections
- Additional insights and perspectives
- Thorough, complete coverage''' if study_mode == "Detailed Study" else ''}

STUDY MATERIAL:
{context}

NOW CREATE COMPREHENSIVE, WELL-STRUCTURED, COMPLETE NOTES:
- Cover EVERYTHING important in the material
- Make it detailed and thorough
- Include visual elements (diagrams, flowcharts, tables)
- Use the formatting guidelines above
- Adapt to the {learning_level} level and {study_mode} mode
- Make it engaging and easy to learn from"""

    return generate_response(prompt, temperature=0.4)