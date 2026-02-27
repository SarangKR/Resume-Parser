import { useState } from 'react'
import { Mail, Phone, Code2, Briefcase, FolderGit2, ChevronDown, ChevronUp } from 'lucide-react'
import MatchResult from './MatchResult'

const ExpandableList = ({ items, emptyMessage }) => {
    const [isExpanded, setIsExpanded] = useState(false)

    if (!items || items.length === 0) {
        return <p className="text-grey italic text-sm font-sans">{emptyMessage}</p>
    }

    const initialCount = 2
    const hasMore = items.length > initialCount
    const displayedItems = isExpanded ? items : items.slice(0, initialCount)

    return (
        <>
            {displayedItems.map((item, i) => (
                <p key={i} className="text-sm text-slate-300 leading-relaxed border-l-2 border-irongrey pl-3 hover:border-primary transition-colors font-sans group relative">
                    <span className="whitespace-pre-line">{typeof item === 'string' ? item : JSON.stringify(item)}</span>
                </p>
            ))}

            {hasMore && (
                <div className="pt-2 flex justify-start">
                    <button
                        onClick={() => setIsExpanded(!isExpanded)}
                        className="flex items-center gap-1.5 mt-1 text-xs text-primary/80 hover:text-white transition-colors font-bold cursor-pointer uppercase tracking-widest font-heading"
                    >
                        {isExpanded ? (
                            <>Show Less <ChevronUp className="w-3.5 h-3.5" /></>
                        ) : (
                            <>Read More <ChevronDown className="w-3.5 h-3.5" /></>
                        )}
                    </button>
                </div>
            )}
        </>
    )
}

export default function Dashboard({ data, onReset }) {
    const skills = data.Skills || []

    // Calculate confidence logic (logic from backend/streamlit)
    let confidence = 0
    if (data.Email) confidence += 40
    if (data.Phone) confidence += 40
    if (skills.length > 0) confidence += 20

    const scoreColor = confidence > 80 ? "text-emerald-600" : "text-amber-500"
    const progressBarColor = confidence > 80 ? "bg-emerald-500" : "bg-amber-500"

    return (
        <div className="space-y-6 fade-in">
            {/* Prominent Match Result Section (Only if Requirements Provided) */}
            {data.meta?.job_match && (
                <MatchResult matchData={data.meta.job_match} />
            )}

            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-white tracking-widest font-heading uppercase text-glow">Analysis Results</h2>
                <button
                    onClick={onReset}
                    className="w-full md:w-auto px-4 py-2 text-sm font-medium text-white bg-onyx border border-irongrey rounded-lg hover:bg-carbon hover:border-charcoal transition-all duration-200 shadow-sm font-heading tracking-wide uppercase"
                >
                    Upload New Resume
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Profile Card */}
                <div className="md:col-span-2 bg-carbon rounded-xl border border-irongrey/50 shadow-lg p-4 md:p-6 hover:border-irongrey transition-colors">
                    <div className="flex flex-col md:flex-row items-center md:items-start gap-4 md:gap-6 text-center md:text-left">
                        <div className="w-16 h-16 bg-onyx rounded-full flex items-center justify-center flex-shrink-0 border border-irongrey">
                            <span className="text-2xl">👤</span>
                        </div>
                        <div className="flex-1 w-full">
                            <h3 className="text-xl md:text-2xl font-bold text-white mb-4 tracking-wide font-heading uppercase text-glow">
                                {data.Name || 'Not Detected'}
                            </h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 md:gap-4">
                                <div className="flex items-center justify-center md:justify-start gap-2 text-grey bg-onyx/50 md:bg-transparent p-2 md:p-0 rounded-lg group">
                                    <Mail className="w-4 h-4 flex-shrink-0 group-hover:text-primary transition-colors" />
                                    {data.Email ? (
                                        <a href={`mailto:${data.Email}`} className="text-xs sm:text-sm font-medium break-all text-slate-300 font-sans hover:text-primary transition-colors">
                                            {data.Email}
                                        </a>
                                    ) : (
                                        <span className="text-xs sm:text-sm font-medium break-all text-slate-300 font-sans">N/A</span>
                                    )}
                                </div>
                                <div className="flex items-center justify-center md:justify-start gap-2 text-grey bg-onyx/50 md:bg-transparent p-2 md:p-0 rounded-lg group">
                                    <Phone className="w-4 h-4 flex-shrink-0 group-hover:text-primary transition-colors" />
                                    {data.Phone ? (
                                        <a href={`tel:${data.Phone}`} className="text-xs sm:text-sm font-medium text-slate-300 font-sans hover:text-primary transition-colors">
                                            {data.Phone}
                                        </a>
                                    ) : (
                                        <span className="text-xs sm:text-sm font-medium text-slate-300 font-sans">N/A</span>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>



                {/* Score Card */}
                <div className="bg-carbon rounded-xl border border-irongrey/50 shadow-lg p-6 hover:border-irongrey transition-colors">
                    <div className="flex justify-between items-center mb-4">
                        <span className="text-xs font-bold text-grey uppercase tracking-widest font-heading">Completeness</span>
                        <span className={`text-3xl font-bold ${scoreColor} font-heading text-glow`}>{confidence}%</span>
                    </div>
                    <div className="w-full bg-onyx rounded-full h-2.5 mb-6 border border-irongrey/30">
                        <div className={`h-2.5 rounded-full ${progressBarColor} shadow-[0_0_10px_rgba(0,0,0,0.3)]`} style={{ width: `${confidence}%` }}></div>
                    </div>
                    <div className="flex items-center gap-2 text-slate-300">
                        <Code2 className="w-5 h-5 text-primary" />
                        <span className="font-bold text-white font-heading text-xl">{skills.length}</span>
                        <span className="text-grey text-sm font-sans uppercase tracking-wide">Skills Identified</span>
                    </div>
                </div>
            </div>

            {/* Skills Section */}
            <div className="bg-carbon rounded-xl border border-irongrey/50 shadow-lg p-6 hover:border-irongrey transition-colors">
                <div className="flex items-center gap-2 mb-4">
                    <Code2 className="w-5 h-5 text-primary" />
                    <h3 className="font-semibold text-white tracking-widest font-heading uppercase text-glow">Technical Competencies</h3>
                </div>
                <div className="flex flex-wrap gap-2">
                    {skills.length > 0 ? (
                        skills.map((skill, index) => (
                            <span
                                key={index}
                                className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-onyx text-slate-200 border border-irongrey hover:border-charcoal transition-colors shadow-sm font-sans tracking-wide"
                            >
                                {skill}
                            </span>
                        ))
                    ) : (
                        <span className="text-grey italic text-sm font-sans">No skills detected.</span>
                    )}
                </div>
            </div>

            {/* Experience & Projects Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Experience */}
                <div className="bg-carbon rounded-xl border border-irongrey/50 shadow-lg p-4 md:p-6 h-80 md:h-96 flex flex-col hover:border-irongrey transition-colors">
                    <div className="flex items-center gap-2 mb-4 flex-shrink-0">
                        <Briefcase className="w-5 h-5 text-primary" />
                        <h3 className="font-semibold text-white tracking-widest font-heading uppercase text-glow">Work Experience</h3>
                    </div>
                    <div className="flex-1 overflow-y-auto pr-2 space-y-3 custom-scrollbar">
                        <ExpandableList items={data.Experience} emptyMessage="No experience section detected." />
                    </div>
                </div>

                {/* Projects */}
                <div className="bg-carbon rounded-xl border border-irongrey/50 shadow-lg p-4 md:p-6 h-80 md:h-96 flex flex-col hover:border-irongrey transition-colors">
                    <div className="flex items-center gap-2 mb-4 flex-shrink-0">
                        <FolderGit2 className="w-5 h-5 text-primary" />
                        <h3 className="font-semibold text-white tracking-widest font-heading uppercase text-glow">Key Projects</h3>
                    </div>
                    <div className="flex-1 overflow-y-auto pr-2 space-y-3 custom-scrollbar">
                        <ExpandableList items={data.Projects} emptyMessage="No projects section detected." />
                    </div>
                </div>
            </div>
        </div>
    )
}
