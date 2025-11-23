import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface User {
  id: number
  username: string
  native_language: string
}

interface Vocabulary {
  id: number
  word_spanish: string
  word_native: string
  word_type: string
  is_verb: boolean
  created_at: string
}

interface LearningQuestion {
  vocabulary_id: number
  question: string
  correct_answer: string
}

interface LearningResponse {
  is_correct: boolean
  correct_answer: string
  explanation: string
}

interface VerbConjugation {
  yo: string
  tu: string
  el_ella_usted: string
  nosotros: string
  vosotros: string
  ellos_ellas_ustedes: string
}

export default function Home() {
  const [user, setUser] = useState<User | null>(null)
  const [username, setUsername] = useState('')
  const [nativeLanguage, setNativeLanguage] = useState<'en' | 'ua'>('en')
  const [activeTab, setActiveTab] = useState<'vocabulary' | 'add' | 'learn'>('vocabulary')
  const [vocabulary, setVocabulary] = useState<Vocabulary[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  // Learning state
  const [currentQuestion, setCurrentQuestion] = useState<LearningQuestion | null>(null)
  const [userAnswer, setUserAnswer] = useState('')
  const [learningFeedback, setLearningFeedback] = useState<LearningResponse | null>(null)
  const [verbConjugation, setVerbConjugation] = useState<VerbConjugation | null>(null)

  // Add word state
  const [wordSpanish, setWordSpanish] = useState('')
  const [wordNative, setWordNative] = useState('')
  const [wordType, setWordType] = useState('noun')

  useEffect(() => {
    if (user) {
      loadVocabulary()
    }
  }, [user])

  const createUser = async () => {
    if (!username.trim()) {
      setError('Please enter a username')
      return
    }
    setLoading(true)
    setError('')
    try {
      const response = await axios.post(`${API_URL}/api/users`, {
        username,
        native_language: nativeLanguage
      })
      setUser(response.data)
      setSuccess('User created successfully!')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create user')
    } finally {
      setLoading(false)
    }
  }

  const loadVocabulary = async () => {
    if (!user) return
    setLoading(true)
    try {
      const response = await axios.get(`${API_URL}/api/vocabulary/${user.id}`)
      setVocabulary(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load vocabulary')
    } finally {
      setLoading(false)
    }
  }

  const addWordText = async () => {
    if (!user || !wordSpanish.trim() || !wordNative.trim()) {
      setError('Please fill in all fields')
      return
    }
    setLoading(true)
    setError('')
    setSuccess('')
    try {
      await axios.post(`${API_URL}/api/vocabulary/${user.id}`, {
        word_spanish: wordSpanish,
        word_native: wordNative,
        word_type: wordType
      })
      setSuccess('Word added successfully!')
      setWordSpanish('')
      setWordNative('')
      setWordType('noun')
      loadVocabulary()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to add word')
    } finally {
      setLoading(false)
    }
  }

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!user || !e.target.files?.[0]) return
    setLoading(true)
    setError('')
    setSuccess('')
    try {
      const formData = new FormData()
      formData.append('file', e.target.files[0])
      await axios.post(`${API_URL}/api/vocabulary/${user.id}/from-image`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setSuccess('Word extracted from image and added!')
      loadVocabulary()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to process image')
    } finally {
      setLoading(false)
    }
  }

  const handleAudioUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!user || !e.target.files?.[0]) return
    setLoading(true)
    setError('')
    setSuccess('')
    try {
      const formData = new FormData()
      formData.append('file', e.target.files[0])
      await axios.post(`${API_URL}/api/vocabulary/${user.id}/from-audio`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setSuccess('Word extracted from audio and added!')
      loadVocabulary()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to process audio')
    } finally {
      setLoading(false)
    }
  }

  const startLearning = async () => {
    if (!user) return
    setLoading(true)
    setError('')
    setLearningFeedback(null)
    setVerbConjugation(null)
    setUserAnswer('')
    try {
      const response = await axios.get(`${API_URL}/api/learning/${user.id}/question`)
      setCurrentQuestion(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get question')
    } finally {
      setLoading(false)
    }
  }

  const submitAnswer = async () => {
    if (!user || !currentQuestion || !userAnswer.trim()) {
      setError('Please enter an answer')
      return
    }
    setLoading(true)
    setError('')
    try {
      const response = await axios.post(`${API_URL}/api/learning/${user.id}/answer`, {
        vocabulary_id: currentQuestion.vocabulary_id,
        user_answer: userAnswer
      })
      setLearningFeedback(response.data)
      
      // If it's a verb, get conjugation
      const vocab = vocabulary.find(v => v.id === currentQuestion.vocabulary_id)
      if (vocab?.is_verb) {
        try {
          const conjResponse = await axios.get(`${API_URL}/api/vocabulary/${vocab.id}/conjugation`)
          setVerbConjugation(conjResponse.data)
        } catch (err) {
          // Ignore conjugation errors
        }
      }
      
      loadVocabulary()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to submit answer')
    } finally {
      setLoading(false)
    }
  }

  if (!user) {
    return (
      <div className="container">
        <div className="card" style={{ maxWidth: '500px', margin: '100px auto' }}>
          <h1 style={{ marginBottom: '20px', color: '#667eea' }}>🇪🇸 Spanish Learning App</h1>
          <p style={{ marginBottom: '20px', color: '#666' }}>
            Welcome! Create your account to start learning Spanish.
          </p>
          {error && <div className="error">{error}</div>}
          {success && <div className="success">{success}</div>}
          <div className="input-group">
            <label className="label">Username</label>
            <input
              type="text"
              className="input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
            />
          </div>
          <div className="input-group">
            <label className="label">Native Language</label>
            <select
              className="input"
              value={nativeLanguage}
              onChange={(e) => setNativeLanguage(e.target.value as 'en' | 'ua')}
            >
              <option value="en">English</option>
              <option value="ua">Ukrainian</option>
            </select>
          </div>
          <button
            className="btn"
            onClick={createUser}
            disabled={loading}
            style={{ width: '100%' }}
          >
            {loading ? 'Creating...' : 'Start Learning'}
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="container">
      <div style={{ textAlign: 'center', marginBottom: '30px', color: 'white' }}>
        <h1 style={{ fontSize: '36px', marginBottom: '10px' }}>🇪🇸 Spanish Learning App</h1>
        <p>Welcome, {user.username}! ({user.native_language === 'en' ? 'English' : 'Ukrainian'})</p>
      </div>

      <div className="card">
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'vocabulary' ? 'active' : ''}`}
            onClick={() => setActiveTab('vocabulary')}
          >
            My Vocabulary
          </button>
          <button
            className={`tab ${activeTab === 'add' ? 'active' : ''}`}
            onClick={() => setActiveTab('add')}
          >
            Add Words
          </button>
          <button
            className={`tab ${activeTab === 'learn' ? 'active' : ''}`}
            onClick={() => setActiveTab('learn')}
          >
            Learn
          </button>
        </div>

        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}

        {activeTab === 'vocabulary' && (
          <div>
            <h2 style={{ marginBottom: '20px', color: '#333' }}>Your Vocabulary ({vocabulary.length} words)</h2>
            {loading ? (
              <div className="loading">Loading...</div>
            ) : vocabulary.length === 0 ? (
              <p style={{ color: '#666', textAlign: 'center', padding: '40px' }}>
                No words yet. Add some words to get started!
              </p>
            ) : (
              <div className="vocabulary-list">
                {vocabulary.map((vocab) => (
                  <div key={vocab.id} className="vocab-item">
                    <h3>{vocab.word_spanish}</h3>
                    <p>{vocab.word_native}</p>
                    <p style={{ fontSize: '12px', color: '#999', marginTop: '8px' }}>
                      {vocab.word_type} {vocab.is_verb && '• Verb'}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'add' && (
          <div>
            <h2 style={{ marginBottom: '20px', color: '#333' }}>Add New Words</h2>
            
            <div style={{ marginBottom: '30px' }}>
              <h3 style={{ marginBottom: '15px', color: '#667eea' }}>Add by Text</h3>
              <div className="input-group">
                <label className="label">Spanish Word</label>
                <input
                  type="text"
                  className="input"
                  value={wordSpanish}
                  onChange={(e) => setWordSpanish(e.target.value)}
                  placeholder="e.g., casa"
                />
              </div>
              <div className="input-group">
                <label className="label">Translation ({user.native_language === 'en' ? 'English' : 'Ukrainian'})</label>
                <input
                  type="text"
                  className="input"
                  value={wordNative}
                  onChange={(e) => setWordNative(e.target.value)}
                  placeholder="e.g., house"
                />
              </div>
              <div className="input-group">
                <label className="label">Word Type</label>
                <select
                  className="input"
                  value={wordType}
                  onChange={(e) => setWordType(e.target.value)}
                >
                  <option value="noun">Noun</option>
                  <option value="verb">Verb</option>
                  <option value="adjective">Adjective</option>
                  <option value="adverb">Adverb</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <button className="btn" onClick={addWordText} disabled={loading}>
                Add Word
              </button>
            </div>

            <div style={{ marginBottom: '30px', paddingTop: '30px', borderTop: '2px solid #e0e0e0' }}>
              <h3 style={{ marginBottom: '15px', color: '#667eea' }}>Add by Image</h3>
              <p style={{ marginBottom: '15px', color: '#666' }}>
                Upload an image containing Spanish text. The app will extract and process it.
              </p>
              <input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                style={{ marginBottom: '10px' }}
              />
            </div>

            <div style={{ paddingTop: '30px', borderTop: '2px solid #e0e0e0' }}>
              <h3 style={{ marginBottom: '15px', color: '#667eea' }}>Add by Voice</h3>
              <p style={{ marginBottom: '15px', color: '#666' }}>
                Record or upload an audio file with Spanish pronunciation.
              </p>
              <input
                type="file"
                accept="audio/*"
                onChange={handleAudioUpload}
                style={{ marginBottom: '10px' }}
              />
            </div>
          </div>
        )}

        {activeTab === 'learn' && (
          <div className="learning-card">
            <h2>Practice Your Spanish!</h2>
            {!currentQuestion ? (
              <div>
                <p style={{ marginBottom: '30px', color: '#666' }}>
                  Click the button below to start a learning session. You'll be asked to translate words from your vocabulary.
                </p>
                <button className="btn" onClick={startLearning} disabled={loading || vocabulary.length === 0}>
                  {vocabulary.length === 0 ? 'Add words first!' : 'Start Learning'}
                </button>
              </div>
            ) : (
              <div>
                <div className="question">{currentQuestion.question}</div>
                <div className="input-group">
                  <input
                    type="text"
                    className="input"
                    value={userAnswer}
                    onChange={(e) => setUserAnswer(e.target.value)}
                    placeholder="Type your answer in Spanish"
                    onKeyPress={(e) => e.key === 'Enter' && submitAnswer()}
                    style={{ maxWidth: '400px', margin: '0 auto' }}
                  />
                </div>
                <button className="btn" onClick={submitAnswer} disabled={loading || !userAnswer.trim()}>
                  {loading ? 'Checking...' : 'Submit Answer'}
                </button>

                {learningFeedback && (
                  <div className={`answer-feedback ${learningFeedback.is_correct ? 'correct' : 'incorrect'}`}>
                    <h3>{learningFeedback.is_correct ? '✅ Correct!' : '❌ Incorrect'}</h3>
                    <p><strong>Correct answer:</strong> {learningFeedback.correct_answer}</p>
                    <p style={{ marginTop: '10px' }}>{learningFeedback.explanation}</p>
                  </div>
                )}

                {verbConjugation && (
                  <div style={{ marginTop: '30px', textAlign: 'left', maxWidth: '600px', margin: '30px auto' }}>
                    <h3 style={{ marginBottom: '15px', color: '#667eea' }}>Verb Conjugation (Simple Present Tense)</h3>
                    <div className="verb-conjugation">
                      <div className="conjugation-item">
                        <strong>Yo</strong>
                        {verbConjugation.yo}
                      </div>
                      <div className="conjugation-item">
                        <strong>Tú</strong>
                        {verbConjugation.tu}
                      </div>
                      <div className="conjugation-item">
                        <strong>Él/Ella/Usted</strong>
                        {verbConjugation.el_ella_usted}
                      </div>
                      <div className="conjugation-item">
                        <strong>Nosotros</strong>
                        {verbConjugation.nosotros}
                      </div>
                      <div className="conjugation-item">
                        <strong>Vosotros</strong>
                        {verbConjugation.vosotros}
                      </div>
                      <div className="conjugation-item">
                        <strong>Ellos/Ellas/Ustedes</strong>
                        {verbConjugation.ellos_ellas_ustedes}
                      </div>
                    </div>
                  </div>
                )}

                <div style={{ marginTop: '30px' }}>
                  <button className="btn btn-secondary" onClick={startLearning} disabled={loading}>
                    Next Question
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

