import { User, CheckCircle, Code2, Target } from 'lucide-react'

export default function CandidateList({ candidates, onSelectCandidate, onReset }) {
    if (!candidates || candidates.length === 0) return null

    return (
        <div className="space-y-8 fade-in">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-irongrey/30 pb-4">
                <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-white tracking-widest font-heading uppercase text-glow">
                    Candidate List <span className="text-primary text-xl px-2 py-0.5 ml-2 bg-primary/10 rounded-full">{candidates.length}</span>
                </h2>
                <button
                    onClick={onReset}
                    className="w-full md:w-auto px-6 py-3 text-sm font-medium text-slate-200 bg-onyx border border-irongrey rounded-lg hover:bg-carbon hover:border-primary/50 hover:text-white transition-all duration-200 shadow-sm font-heading tracking-wide uppercase"
                >
                    Upload New Resumes
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {candidates.map((candidate, index) => {
                    const completeness = candidate.meta?.confidence_score || 0
                    const isShortlisted = candidate.meta?.job_match?.is_shortlisted
                    const matchScore = candidate.meta?.job_match?.score

                    return (
                        <div
                            key={index}
                            onClick={() => onSelectCandidate(candidate)}
                            className={`cursor-pointer bg-carbon rounded-xl border ${isShortlisted ? 'border-primary/50' : 'border-irongrey/50'} shadow-lg p-6 hover:border-primary transition-all duration-300 hover:scale-[1.02] flex flex-col h-full`}
                        >
                            <div className="flex items-start justify-between mb-6">
                                <div className="flex items-center gap-3 w-full pr-2">
                                    <div className="w-12 h-12 bg-onyx rounded-full flex items-center justify-center flex-shrink-0 border border-irongrey">
                                        <User className="w-6 h-6 text-slate-300" />
                                    </div>
                                    <div className="overflow-hidden">
                                        <h3 className="font-bold text-white text-lg tracking-wide font-heading truncate">
                                            {candidate.Name ? candidate.Name : candidate.fileName}
                                        </h3>
                                        {candidate.Name && (
                                            <div className="text-xs text-dimgrey font-sans truncate" title={candidate.fileName}>
                                                {candidate.fileName}
                                            </div>
                                        )}
                                        {!candidate.Name && (
                                            <div className="text-xs text-amber-500/80 font-sans italic truncate">
                                                Name not detected
                                            </div>
                                        )}
                                    </div>
                                </div>
                                {isShortlisted && (
                                    <div className="bg-primary/20 text-primary px-2.5 py-1 flex items-center gap-1.5 rounded-full text-xs font-bold uppercase tracking-wider whitespace-nowrap shrink-0 border border-primary/30">
                                        <CheckCircle className="w-3.5 h-3.5" /> Shortlisted
                                    </div>
                                )}
                            </div>

                            <div className="space-y-4 mb-auto">
                                {matchScore !== undefined && (
                                    <div className="flex justify-between items-end bg-onyx/30 p-2 text-sm rounded border border-irongrey/30">
                                        <div className="flex items-center gap-1.5 font-bold text-grey uppercase tracking-widest font-heading">
                                            <Target className="w-4 h-4 text-primary/70" /> Match Score
                                        </div>
                                        <div className={`text-lg font-bold font-heading ${matchScore >= 50 ? 'text-primary' : 'text-amber-500'}`}>
                                            {matchScore}%
                                        </div>
                                    </div>
                                )}

                                <div className="flex justify-between items-end px-2">
                                    <div className="text-xs font-bold text-slate-400 uppercase tracking-widest font-heading">
                                        Completeness
                                    </div>
                                    <div className={`text-base font-bold font-heading ${completeness > 80 ? 'text-emerald-500' : 'text-amber-500'}`}>
                                        {completeness}%
                                    </div>
                                </div>

                                <div className="flex justify-between items-end px-2">
                                    <div className="flex items-center gap-1.5 text-xs font-bold text-slate-400 uppercase tracking-widest font-heading">
                                        <Code2 className="w-3.5 h-3.5 text-grey" /> Skills Found
                                    </div>
                                    <div className="text-base font-bold font-heading text-white">
                                        {candidate.meta?.skills_count || candidate.Skills?.length || 0}
                                    </div>
                                </div>
                            </div>

                            <div className="mt-6 pt-4 border-t border-irongrey/30 text-center flex items-center justify-center gap-2 group-hover:text-primary transition-colors text-slate-400 text-sm font-bold uppercase tracking-widest">
                                <span>View Full Details</span>
                                <span className="transform group-hover:translate-x-1 transition-transform">&rarr;</span>
                            </div>
                        </div>
                    )
                })}
            </div>
        </div>
    )
}
