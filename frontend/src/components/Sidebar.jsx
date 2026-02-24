import { Monitor, Shield, HelpCircle, FileText, X } from 'lucide-react'

export default function Sidebar({ isOpen, onClose, onReset }) {
    return (
        <>
            {/* Mobile Overlay */}
            {isOpen && (
                <div
                    className="fixed inset-0 bg-black/50 z-40 lg:hidden backdrop-blur-sm transition-opacity"
                    onClick={onClose}
                />
            )}

            <aside className={`
                fixed lg:sticky top-0 h-screen z-50 lg:z-0
                w-72 flex-col border-r border-irongrey/30 bg-onyx/95 lg:bg-onyx/40 backdrop-blur-xl
                transition-all duration-300 ease-in-out
                ${isOpen ? 'translate-x-0' : '-translate-x-full lg:w-0 lg:-translate-x-0 lg:overflow-hidden lg:border-none lg:p-0'}
                ${isOpen ? 'lg:w-72 lg:p-6' : ''}
            `}>
                {/* Close Button (Mobile) */}
                <button
                    onClick={onClose}
                    className="lg:hidden absolute top-4 right-4 p-2 text-grey hover:text-white transition-colors"
                >
                    <X className="w-5 h-5" />
                </button>

                <div className={`${!isOpen && 'lg:hidden'} h-full flex flex-col ${isOpen ? 'p-6' : ''}`}>
                    {/* Logo/Branding */}
                    <div className="mb-10 flex items-center gap-3">
                        <button onClick={onReset} className="text-xl font-bold tracking-widest text-white/90 font-heading text-glow uppercase hover:text-white transition-colors cursor-pointer">
                            TalentScout
                        </button>
                    </div>

                    {/* Navigation / Info Sections */}
                    <div className="flex-1 space-y-8 overflow-y-auto custom-scrollbar pl-2">
                        {/* How to Use Section */}
                        <div className="space-y-4">
                            <h3 className="text-sm font-bold text-grey uppercase tracking-widest font-heading flex items-center gap-2">
                                <HelpCircle className="w-4 h-4" />
                                Usage Guide
                            </h3>
                            <div className="relative pl-4 border-l border-irongrey/50 space-y-6">
                                <div className="group relative">
                                    <span className="absolute -left-[21px] top-1 w-2.5 h-2.5 rounded-full bg-onyx border border-grey group-hover:border-primary group-hover:bg-primary transition-colors duration-300"></span>
                                    <h4 className="text-white font-medium font-heading tracking-wide uppercase text-sm mb-1 group-hover:text-primary transition-colors">1. Upload Resume</h4>
                                    <p className="text-xs text-grey font-sans leading-relaxed">
                                        PDF format required. Drag & drop supported.
                                    </p>
                                </div>
                                <div className="group relative">
                                    <span className="absolute -left-[21px] top-1 w-2.5 h-2.5 rounded-full bg-onyx border border-grey group-hover:border-primary group-hover:bg-primary transition-colors duration-300"></span>
                                    <h4 className="text-white font-medium font-heading tracking-wide uppercase text-sm mb-1 group-hover:text-primary transition-colors">2. AI Analysis</h4>
                                    <p className="text-xs text-grey font-sans leading-relaxed">
                                        Extraction of contact info, skills, and experience.
                                    </p>
                                </div>
                                <div className="group relative">
                                    <span className="absolute -left-[21px] top-1 w-2.5 h-2.5 rounded-full bg-onyx border border-grey group-hover:border-primary group-hover:bg-primary transition-colors duration-300"></span>
                                    <h4 className="text-white font-medium font-heading tracking-wide uppercase text-sm mb-1 group-hover:text-primary transition-colors">3. Review Data</h4>
                                    <p className="text-xs text-grey font-sans leading-relaxed">
                                        Verify parsed details and view completeness score.
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* System Status Section */}
                        <div className="space-y-3">
                            <h3 className="text-sm font-bold text-grey uppercase tracking-widest font-heading flex items-center gap-2">
                                <Monitor className="w-4 h-4" />
                                System Status
                            </h3>
                            <div className="p-3 bg-carbon/50 rounded-lg border border-irongrey/30 backdrop-blur-sm">
                                <div className="flex items-center justify-between mb-2">
                                    <span className="text-xs text-slate-300 font-sans">Parser Engine</span>
                                    <span className="flex items-center gap-1.5 text-xs text-green-400 font-bold font-heading uppercase">
                                        <span className="relative flex h-2 w-2">
                                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                                            <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                                        </span>
                                        Online
                                    </span>
                                </div>
                                <div className="w-full bg-onyx rounded-full h-1.5 mb-1">
                                    <div className="bg-green-500 h-1.5 rounded-full" style={{ width: '98%' }}></div>
                                </div>
                                <div className="text-[10px] text-dimgrey font-mono text-right">Latency: 45ms</div>
                            </div>
                        </div>
                    </div>

                    {/* Footer / Version */}
                    <div className="mt-auto pt-6 border-t border-irongrey/30">
                        <div className="flex items-center justify-between text-xs text-grey">
                            <span className="font-heading tracking-widest uppercase opacity-70">Version</span>
                            <span className="font-mono bg-onyx px-2 py-1 rounded text-slate-300 border border-irongrey/50">v1.2.0-beta</span>
                        </div>
                        <div className="mt-4 flex items-center gap-2 text-[10px] text-dimgrey font-sans justify-center opacity-50 hover:opacity-100 transition-opacity cursor-default">
                            <Shield className="w-3 h-3" />
                            <span>Secure Environment</span>
                        </div>
                    </div>
                </div>
            </aside>
        </>
    )
}
