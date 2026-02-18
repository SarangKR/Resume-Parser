import { useState, useRef } from 'react'
import { FileText, Menu, PanelLeft, Mail } from 'lucide-react'
import Upload from './components/Upload'
import Dashboard from './components/Dashboard'
import Sidebar from './components/Sidebar'

function App() {
    const [resumeData, setResumeData] = useState(null)
    const [loading, setLoading] = useState(false)
    const [uploadError, setUploadError] = useState(null)
    const [isSidebarOpen, setIsSidebarOpen] = useState(true)
    const [autoOpenUpload, setAutoOpenUpload] = useState(false) // Added this state

    const handleUpload = async (file, options = {}) => {
        setLoading(true)
        setUploadError(null)
        setResumeData(null)
        setAutoOpenUpload(false) // Reset flag after upload starts

        const formData = new FormData()
        formData.append('file', file)

        if (options.requiredSkills) {
            formData.append('required_skills', options.requiredSkills)
        }
        if (options.recruiterEmail) {
            formData.append('recruiter_email', options.recruiterEmail)
        }

        try {
            const response = await fetch('/api/parse', {
                method: 'POST',
                body: formData,
            })

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}))
                throw new Error(errorData.detail || 'Failed to parse resume')
            }

            const result = await response.json()
            // Merge meta into the data object so Dashboard receives everything
            setResumeData({ ...result.data, meta: result.meta })
        } catch (error) {
            console.error("Upload failed", error)
            setUploadError(error.message || "Failed to parse resume. Please ensure the backend is running.")
        } finally {
            setLoading(false)
        }
    }

    const handleReset = () => {
        setResumeData(null)
        setUploadError(null)
    }

    return (
        <div className="min-h-screen flex flex-row bg-transparent text-slate-200 font-sans">
            {/* Sidebar */}
            <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />

            <div className="flex-1 flex flex-col min-h-screen relative overflow-hidden">
                {/* Mobile Header (Only visible on small screens) */}
                <header className="lg:hidden bg-onyx/80 backdrop-blur-md border-b border-irongrey py-3 md:py-4 sticky top-0 z-50 transition-all duration-300">
                    <div className="container mx-auto px-4 md:px-6 flex items-center justify-between gap-3">
                        <div className="flex items-center gap-3">
                            <button onClick={() => setIsSidebarOpen(true)} className="p-2 text-white hover:bg-white/10 rounded-lg transition-colors">
                                <Menu className="w-6 h-6" />
                            </button>
                            <div className="flex items-center gap-3">
                                <h1 className="text-base md:text-xl font-bold tracking-widest text-white/90 font-heading text-glow uppercase">TalentScout</h1>
                            </div>
                        </div>
                    </div>
                </header>

                {/* Desktop Toggle Button (Absolute position or injected into main) */}
                <button
                    onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                    className="hidden lg:flex absolute top-6 left-6 z-40 p-2 bg-onyx/50 backdrop-blur-md border border-irongrey/50 rounded-lg text-slate-300 hover:text-white hover:bg-onyx transition-all"
                    title={isSidebarOpen ? "Close Sidebar" : "Open Sidebar"}
                >
                    <PanelLeft className={`w-5 h-5 transition-transform duration-300 ${!isSidebarOpen && 'rotate-180'}`} />
                </button>

                {/* Main Content Area */}
                <main className="flex-1 overflow-y-auto w-full">
                    <div className="container mx-auto px-4 md:px-8 py-8 md:py-12 max-w-7xl">
                        {!resumeData ? (
                            <div className="max-w-4xl mx-auto flex flex-col items-center justify-center min-h-[80vh] fade-in">
                                <div className="mb-8 md:mb-12 text-center space-y-4">
                                    <h2 className="text-4xl sm:text-5xl md:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white via-slate-200 to-grey mb-2 tracking-wide font-heading text-glow uppercase">
                                        Resume Parser
                                    </h2>
                                    <p className="text-grey text-sm sm:text-base md:text-lg max-w-2xl mx-auto leading-relaxed font-sans tracking-wide">
                                        Extract, analyze, and structure candidate data automatically with precision.
                                        Compare the extracted data with the job description and get the best match.
                                    </p>
                                </div>

                                <Upload onUpload={handleUpload} loading={loading} />

                                {uploadError && (
                                    <div className="mt-6 p-4 bg-red-500/10 border border-red-500/20 text-red-200 rounded-lg text-sm md:text-base animate-pulse font-sans">
                                        ⚠️ {uploadError}
                                    </div>
                                )}
                            </div>
                        ) : (
                            <Dashboard data={resumeData} onReset={handleReset} />
                        )}
                    </div>
                </main>

                <footer className="py-6 border-t border-irongrey/30 bg-onyx/40 backdrop-blur-sm mt-auto">
                    <div className="container mx-auto px-4 md:px-8 flex flex-col md:flex-row items-center justify-between gap-4">
                        <div className="text-center md:text-left">
                            <p className="text-dimgrey text-xs font-sans">© 2026 TalentScout AI. All rights reserved.</p>
                        </div>

                        <div className="flex items-center gap-4">
                            <span className="text-xs text-grey font-heading uppercase tracking-widest font-bold">Contact</span>
                            <a
                                href="mailto:k.r.sarang06@gmail.com"
                                className="p-2 text-slate-400 hover:text-white hover:bg-white/5 rounded-full transition-all group bg-onyx border border-irongrey/30 hover:border-primary/50"
                                aria-label="Contact via Email"
                            >
                                <Mail className="w-4 h-4 group-hover:text-primary transition-colors" />
                            </a>
                        </div>
                    </div>
                </footer>
            </div>
        </div>
    )
}

export default App
