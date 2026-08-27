import { useState } from 'react'
import axios from 'axios'
import { Upload, FileText, Brain, MessageCircle, Loader2, Download, BookOpen } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import './App.css'

const API_URL = 'http://localhost:8000/api'

function App() {
  const [docId, setDocId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [docInfo, setDocInfo] = useState(null)
  const [activeTab, setActiveTab] = useState('upload')
  
  // States for each feature
  const [notes, setNotes] = useState('')
  const [quiz, setQuiz] = useState('')
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState(null)
  
  // Preferences
  const [learningLevel, setLearningLevel] = useState('Intermediate')
  const [studyMode, setStudyMode] = useState('Quick Revision')
  const [difficulty, setDifficulty] = useState('Medium')
  const [numQuestions, setNumQuestions] = useState(5)

  const handleFileUpload = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    setLoading(true)
    try {
      const response = await axios.post(`${API_URL}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      
      setDocId(response.data.doc_id)
      setDocInfo(response.data)
      setActiveTab('notes')
      alert('✅ PDF processed successfully!')
    } catch (error) {
      alert('Error: ' + (error.response?.data?.detail || 'Failed to upload PDF'))
    } finally {
      setLoading(false)
    }
  }

  const generateNotes = async () => {
    if (!docId) return

    setLoading(true)
    try {
      const response = await axios.post(`${API_URL}/generate-notes`, {
        doc_id: docId,
        learning_level: learningLevel,
        study_mode: studyMode
      })
      setNotes(response.data.notes)
    } catch (error) {
      alert('Error: ' + (error.response?.data?.detail || 'Failed to generate notes'))
    } finally {
      setLoading(false)
    }
  }

  const generateQuiz = async () => {
    if (!docId) return

    setLoading(true)
    try {
      const response = await axios.post(`${API_URL}/generate-quiz`, {
        doc_id: docId,
        difficulty: difficulty,
        num_questions: numQuestions
      })
      setQuiz(response.data.quiz)
    } catch (error) {
      alert('Error: ' + (error.response?.data?.detail || 'Failed to generate quiz'))
    } finally {
      setLoading(false)
    }
  }

  const askQuestion = async () => {
    if (!docId || !question.trim()) return

    setLoading(true)
    try {
      const response = await axios.post(`${API_URL}/ask-question`, {
        doc_id: docId,
        question: question
      })
      setAnswer(response.data)
    } catch (error) {
      alert('Error: ' + (error.response?.data?.detail || 'Failed to get answer'))
    } finally {
      setLoading(false)
    }
  }

  const downloadContent = (content, filename) => {
    const blob = new Blob([content], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <BookOpen size={32} />
          <h1>AI Learning Material Generator</h1>
          <p>Transform PDFs into smart notes, quizzes, and get AI-powered answers</p>
        </div>
      </header>

      <div className="container">
        {/* Sidebar */}
        <aside className="sidebar">
          <h3>⚙️ Preferences</h3>
          
          <div className="preference-group">
            <label>Learning Level</label>
            <select value={learningLevel} onChange={(e) => setLearningLevel(e.target.value)}>
              <option>Beginner</option>
              <option>Intermediate</option>
              <option>Advanced</option>
            </select>
          </div>

          <div className="preference-group">
            <label>Study Mode</label>
            <select value={studyMode} onChange={(e) => setStudyMode(e.target.value)}>
              <option>Quick Revision</option>
              <option>Exam Preparation</option>
              <option>Detailed Study</option>
            </select>
          </div>

          {docInfo && (
            <div className="doc-stats">
              <h3>📊 Document Stats</h3>
              <div className="stat">
                <span>Characters:</span>
                <strong>{docInfo.num_characters.toLocaleString()}</strong>
              </div>
              <div className="stat">
                <span>Chunks:</span>
                <strong>{docInfo.num_chunks}</strong>
              </div>
              <div className="stat">
                <span>Keywords:</span>
                <strong>{docInfo.keywords.length}</strong>
              </div>
              <div className="keywords">
                <strong>🔑 Keywords:</strong>
                <p>{docInfo.keywords.join(', ')}</p>
              </div>
            </div>
          )}
        </aside>

        {/* Main Content */}
        <main className="main-content">
          {/* Tabs */}
          <div className="tabs">
            <button 
              className={`tab ${activeTab === 'upload' ? 'active' : ''}`}
              onClick={() => setActiveTab('upload')}
            >
              <Upload size={20} /> Upload PDF
            </button>
            <button 
              className={`tab ${activeTab === 'notes' ? 'active' : ''}`}
              onClick={() => setActiveTab('notes')}
              disabled={!docId}
            >
              <FileText size={20} /> Smart Notes
            </button>
            <button 
              className={`tab ${activeTab === 'quiz' ? 'active' : ''}`}
              onClick={() => setActiveTab('quiz')}
              disabled={!docId}
            >
              <Brain size={20} /> Quiz
            </button>
            <button 
              className={`tab ${activeTab === 'ask' ? 'active' : ''}`}
              onClick={() => setActiveTab('ask')}
              disabled={!docId}
            >
              <MessageCircle size={20} /> Ask AI
            </button>
          </div>

          {/* Tab Content */}
          <div className="tab-content">
            {activeTab === 'upload' && (
              <div className="upload-section">
                <div className="upload-box">
                  <Upload size={64} />
                  <h2>Upload Your Study Material</h2>
                  <p>Upload a PDF document to get started</p>
                  <input 
                    type="file" 
                    accept=".pdf" 
                    onChange={handleFileUpload}
                    id="file-upload"
                    disabled={loading}
                  />
                  <label htmlFor="file-upload" className="upload-btn">
                    {loading ? <><Loader2 className="spin" /> Processing...</> : 'Choose PDF File'}
                  </label>
                </div>
              </div>
            )}

            {activeTab === 'notes' && (
              <div className="feature-section">
                <h2>📝 Smart Notes Generator</h2>
                <p>Generate concise, exam-oriented notes from your uploaded material</p>
                
                <button onClick={generateNotes} disabled={loading} className="generate-btn">
                  {loading ? <><Loader2 className="spin" /> Generating...</> : 'Generate Smart Notes'}
                </button>

                {notes && (
                  <div className="result">
                    <div className="result-header">
                      <h3>Your Notes</h3>
                      <button onClick={() => downloadContent(notes, 'notes.md')} className="download-btn">
                        <Download size={16} /> Download
                      </button>
                    </div>
                    <div className="markdown-content">
                      <ReactMarkdown>{notes}</ReactMarkdown>
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'quiz' && (
              <div className="feature-section">
                <h2>🧠 Quiz & MCQ Generator</h2>
                
                <div className="quiz-settings">
                  <div className="setting">
                    <label>Difficulty</label>
                    <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
                      <option>Easy</option>
                      <option>Medium</option>
                      <option>Hard</option>
                    </select>
                  </div>
                  <div className="setting">
                    <label>Number of Questions</label>
                    <input 
                      type="range" 
                      min="3" 
                      max="10" 
                      value={numQuestions}
                      onChange={(e) => setNumQuestions(parseInt(e.target.value))}
                    />
                    <span>{numQuestions} questions</span>
                  </div>
                </div>

                <button onClick={generateQuiz} disabled={loading} className="generate-btn">
                  {loading ? <><Loader2 className="spin" /> Generating...</> : 'Generate Quiz'}
                </button>

                {quiz && (
                  <div className="result">
                    <div className="result-header">
                      <h3>Your Quiz</h3>
                      <button onClick={() => downloadContent(quiz, 'quiz.md')} className="download-btn">
                        <Download size={16} /> Download
                      </button>
                    </div>
                    <div className="markdown-content">
                      <ReactMarkdown>{quiz}</ReactMarkdown>
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'ask' && (
              <div className="feature-section">
                <h2>💬 AI Study Assistant</h2>
                <p>Ask questions about your uploaded study material</p>

                <div className="question-input">
                  <input 
                    type="text" 
                    placeholder="Example: What is Reinforcement Learning?"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && askQuestion()}
                  />
                  <button onClick={askQuestion} disabled={loading || !question.trim()}>
                    {loading ? <Loader2 className="spin" /> : 'Ask AI'}
                  </button>
                </div>

                {answer && (
                  <div className="result">
                    <h3>🤖 Answer</h3>
                    <div className="answer-content">
                      <ReactMarkdown>{answer.answer}</ReactMarkdown>
                    </div>
                    
                    <details className="sources">
                      <summary>🔎 View Retrieved Material ({answer.sources.length} chunks)</summary>
                      {answer.sources.map((source, idx) => (
                        <div key={idx} className="source-chunk">
                          <h4>Source Chunk {idx + 1} <span>(Score: {source.score.toFixed(4)})</span></h4>
                          <p>{source.text}</p>
                        </div>
                      ))}
                    </details>
                  </div>
                )}
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  )
}

export default App
