import { useState, useRef, useEffect } from 'react'
import { UploadCloud, File, Loader2, Briefcase, Mail, ChevronDown, ChevronUp } from 'lucide-react'

export default function Upload({ onUpload, loading, autoOpen, onFileSelect }) {
    const [dragActive, setDragActive] = useState(false)
    const [showRecruiterOptions, setShowRecruiterOptions] = useState(false)
    const [requiredSkills, setRequiredSkills] = useState('')
    const [recruiterEmail, setRecruiterEmail] = useState('')
    const [selectedFile, setSelectedFile] = useState(null)
    const inputRef = useRef(null)

    // useEffect(() => {
    //     if (autoOpen && inputRef.current) {
    //         inputRef.current.click()
    //     }
    // }, [autoOpen])


    const handleDrag = (e) => {
        e.preventDefault()
        e.stopPropagation()
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true)
        } else if (e.type === "dragleave") {
            setDragActive(false)
        }
    }

    const handleDrop = (e) => {
        e.preventDefault()
        e.stopPropagation()
        setDragActive(false)
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFileSelect(e.dataTransfer.files[0])
        }
    }

    const handleChange = (e) => {
        e.preventDefault()
        if (e.target.files && e.target.files[0]) {
            handleFileSelect(e.target.files[0])
        }
    }

    const handleFileSelect = (file) => {
        setSelectedFile(file)
        if (onFileSelect) onFileSelect()
    }

    const handleSubmit = () => {
        if (selectedFile) {
            onUpload(selectedFile, { requiredSkills, recruiterEmail })
        }
    }

    const onButtonClick = () => {
        inputRef.current.click()
    }

    return (
        <div className="flex flex-col items-center justify-center w-full max-w-2xl mx-auto animate-fade-in-up">
            {/* Recruiter Options Toggle */}
            <div className="w-full mb-4">
                <button
                    onClick={() => setShowRecruiterOptions(!showRecruiterOptions)}
                    className="flex items-center justify-center w-full gap-2 p-3 text-sm text-slate-200 hover:text-white transition-all duration-300 mb-2 font-heading uppercase tracking-wider bg-carbon/60 border border-charcoal rounded-lg hover:bg-carbon/80 shadow-md"
                >
                    {showRecruiterOptions ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    Recruiter Options
                </button>

                {showRecruiterOptions && (
                    <div className="bg-onyx/50 border border-irongrey/50 p-4 rounded-xl space-y-4 mb-4 backdrop-blur-sm animate-fade-in">
                        <div>
                            <label className="block text-xs uppercase tracking-wider text-slate-400 mb-1 font-heading">Required Skills (Comma Separated)</label>
                            <div className="relative">
                                <Briefcase className="absolute left-3 top-2.5 w-4 h-4 text-grey" />
                                <input
                                    type="text"
                                    value={requiredSkills}
                                    onChange={(e) => setRequiredSkills(e.target.value)}
                                    placeholder="e.g. Python, React, Machine Learning"
                                    className="w-full bg-carbon border border-irongrey rounded-lg py-2 pl-10 pr-4 text-sm text-slate-200 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary placeholder:text-dimgrey font-sans"
                                />
                            </div>
                        </div>
                        <div>
                            <label className="block text-xs uppercase tracking-wider text-slate-400 mb-1 font-heading">Recruiter Email (For Shortlist)</label>
                            <div className="relative">
                                <Mail className="absolute left-3 top-2.5 w-4 h-4 text-grey" />
                                <input
                                    type="email"
                                    value={recruiterEmail}
                                    onChange={(e) => setRecruiterEmail(e.target.value)}
                                    placeholder="recruiter@example.com"
                                    className="w-full bg-carbon border border-irongrey rounded-lg py-2 pl-10 pr-4 text-sm text-slate-200 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary placeholder:text-dimgrey font-sans"
                                />
                            </div>
                        </div>
                    </div>
                )}
            </div>

            <div
                className={`
          relative w-full p-4 sm:p-6 md:p-12 border-2 border-dashed rounded-xl transition-all duration-300 ease-in-out
          flex flex-col items-center justify-center gap-4 text-center cursor-pointer group
          ${dragActive
                        ? "border-primary bg-primary/10 scale-[1.02]"
                        : "border-irongrey hover:border-charcoal hover:bg-onyx"
                    }
          ${loading ? "opacity-50 pointer-events-none" : ""}
        `}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={onButtonClick}
            >
                <input
                    ref={inputRef}
                    type="file"
                    className="hidden"
                    accept=".pdf"
                    onChange={handleChange}
                />

                <div className={`p-4 rounded-full shadow-lg transition-all duration-300 ${loading ? 'bg-onyx' : 'bg-gradient-to-br from-carbon to-onyx group-hover:from-graphite group-hover:to-carbon'}`}>
                    {loading ? (
                        <Loader2 className="w-10 h-10 text-primary animate-spin" />
                    ) : (
                        <UploadCloud className="w-10 h-10 text-white group-hover:scale-110 transition-transform duration-300" />
                    )}
                </div>

                <div className="space-y-2">
                    <h3 className="text-lg sm:text-xl md:text-2xl font-bold text-white group-hover:text-primary transition-colors font-heading tracking-widest uppercase text-glow">
                        {loading ? "Analyzing Resume..." : (selectedFile ? "Ready to Submit" : "Upload Candidate Resume")}
                    </h3>
                    <p className={`text-xs sm:text-sm md:text-base font-sans tracking-wide ${selectedFile ? 'text-primary font-semibold' : 'text-grey'}`}>
                        {selectedFile ? `Selected: ${selectedFile.name}` : "Drag and drop your PDF here, or click to browse"}
                    </p>
                </div>

                <div className="text-xs text-dimgrey mt-4 border px-3 py-1 rounded-full border-irongrey/50">
                    Supported Format: PDF
                </div>
            </div>

            {selectedFile && !loading && (
                <button
                    onClick={handleSubmit}
                    className="mt-6 px-10 py-3 rounded-lg font-heading uppercase tracking-widest text-sm font-bold shadow-lg transition-all duration-300 bg-carbon border border-charcoal text-white hover:bg-carbon/80 hover:text-primary hover:border-primary/50"
                >
                    Submit for Parsing
                </button>
            )}

            {loading && (
                <button
                    disabled
                    className="mt-6 px-10 py-3 rounded-lg font-heading uppercase tracking-widest text-sm font-bold shadow-lg transition-all duration-300 bg-onyx border border-irongrey text-dimgrey cursor-not-allowed"
                >
                    Parsing...
                </button>
            )}
        </div>
    )
}
