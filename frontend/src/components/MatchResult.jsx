import { CheckCircle2, XCircle, MailCheck, AlertTriangle } from 'lucide-react'

export default function MatchResult({ matchData }) {
    if (!matchData) return null

    const isShortlisted = matchData.is_shortlisted
    const score = matchData.score
    const boxColor = isShortlisted ? 'bg-emerald-500/10 border-emerald-500/30' : 'bg-red-500/10 border-red-500/30'
    const textColor = isShortlisted ? 'text-emerald-400' : 'text-red-400'
    const icon = isShortlisted ? <CheckCircle2 className="w-8 h-8 md:w-10 md:h-10 text-emerald-500" /> : <XCircle className="w-8 h-8 md:w-10 md:h-10 text-red-500" />

    return (
        <div className={`w-full rounded-2xl border ${boxColor} p-6 md:p-8 mb-8 animate-fade-in-up flex flex-col md:flex-row items-center justify-between gap-6 shadow-xl relative overflow-hidden group`}>
            {/* Background Glow */}
            <div className={`absolute -top-20 -left-20 w-64 h-64 rounded-full blur-[100px] opacity-20 ${isShortlisted ? 'bg-emerald-500' : 'bg-red-500'} pointer-events-none`}></div>

            <div className="flex items-center gap-6 z-10">
                <div className={`p-4 rounded-full ${isShortlisted ? 'bg-emerald-500/20' : 'bg-red-500/20'}`}>
                    {icon}
                </div>
                <div>
                    <h2 className={`text-2xl md:text-3xl font-bold font-heading uppercase tracking-widest text-glow mb-2 ${textColor}`}>
                        {isShortlisted ? 'Candidate Shortlisted' : 'Skills Mismatch'}
                    </h2>
                    <p className="text-slate-300 font-sans text-sm md:text-base max-w-lg leading-relaxed">
                        {isShortlisted
                            ? "This candidate's skill set matches your requirements. A shortlist notification has been triggered."
                            : "This candidate does not meet the minimum skill matching threshold (50%)."
                        }
                    </p>
                </div>
            </div>

            <div className="flex flex-col items-center md:items-end gap-3 z-10 w-full md:w-auto mt-4 md:mt-0 border-t md:border-t-0 md:border-l border-white/10 pt-4 md:pt-0 md:pl-8">
                <div className="flex flex-col items-center md:items-end">
                    <span className="text-xs font-bold text-grey uppercase tracking-widest font-heading mb-1">Match Score</span>
                    <span className={`text-4xl md:text-5xl font-black font-heading text-glow ${textColor}`}>
                        {score}%
                    </span>
                </div>

                {matchData.email_sent && (
                    <div className="flex items-center gap-2 bg-emerald-500/20 px-3 py-1.5 rounded-full border border-emerald-500/30">
                        <MailCheck className="w-4 h-4 text-emerald-400" />
                        <span className="text-xs text-emerald-300 font-medium tracking-wide font-sans">Email Sent</span>
                    </div>
                )}
            </div>
        </div>
    )
}
