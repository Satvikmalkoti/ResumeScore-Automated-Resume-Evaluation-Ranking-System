"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { useParams } from "next/navigation"
import AnalysisDashboard from "@/components/analysis-dashboard"
import AppNav from "@/components/app-nav"

export default function CandidatePage() {
    const { id } = useParams()
    const [cand, setCand] = useState<any>(null)
    const [checkedStorage, setCheckedStorage] = useState(false)

    useEffect(() => {
        const stored = sessionStorage.getItem("results")
        if (stored) {
            const data = JSON.parse(stored)
            setCand(data.results[Number(id)])
        }
        setCheckedStorage(true)
    }, [id])

    if (!checkedStorage) return (
        <div className="flex items-center justify-center min-h-screen bg-background-light">
            <div className="text-4xl font-black uppercase tracking-tighter animate-pulse">Loading Profile...</div>
        </div>
    )

    if (!cand) return (
        <div className="bg-background-light min-h-screen text-brutal-black font-sans p-8">
            <div className="max-w-7xl mx-auto">
                <AppNav className="mb-16 px-4" />
                <div className="brutalist-card bg-white p-10 border-4 text-center">
                    <div className="text-4xl font-black uppercase tracking-tighter mb-4">Profile Not Found</div>
                    <p className="max-w-xl mx-auto font-bold uppercase tracking-widest text-slate-400 mb-10">
                        This candidate page needs a parsed pool in session storage. Open results from the upload flow.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <Link href="/results" className="brutalist-button text-sm py-4 px-10">
                            Candidates
                        </Link>
                        <Link href="/upload" className="brutalist-button-primary text-sm py-4 px-10">
                            Upload Pool
                        </Link>
                    </div>
                </div>
            </div>
            <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
        </div>
    )

    const name = cand.filename.split('.')[0]

    return (
        <div className="bg-background-light min-h-screen text-brutal-black font-sans p-8">
            <div className="max-w-7xl mx-auto">
                <AppNav
                    className="mb-8 px-4"
                    rightSlot={
                        <div className="hidden md:flex items-center gap-4 border-l-2 border-brutal-black pl-6">
                            <span className="material-symbols-outlined hover:bg-slate-100 p-2 rounded-full cursor-pointer transition-colors border-2 border-transparent hover:border-brutal-black">
                                notifications
                            </span>
                            <div className="size-10 bg-slate-200 rounded-full border-2 border-brutal-black overflow-hidden shadow-hard-sm">
                                <img
                                    src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${name}`}
                                    alt="User"
                                    className="w-full h-full object-cover"
                                />
                            </div>
                        </div>
                    }
                />
                <div className="flex items-center gap-4 font-black uppercase text-xs tracking-[0.2em] text-slate-400 mb-12 px-4">
                    <Link href="/results" className="hover:text-brutal-black transition-colors">Candidates</Link>
                    <span>&rsaquo;</span>
                    <span className="text-brutal-black italic">{name}</span>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 px-4">
                    {/* Left Column: Profile Card & Breakdown */}
                    <div className="lg:col-span-4 space-y-8">
                        <div className="brutalist-card bg-white p-8 border-4 group">
                            <div className="flex justify-center mb-8">
                                <div className="size-32 bg-slate-100 border-4 border-brutal-black rounded-lg overflow-hidden shadow-hard group-hover:shadow-none group-hover:translate-x-1 group-hover:translate-y-1 transition-all">
                                    <img src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${name}`} alt={name} className="w-full h-full object-cover" />
                                </div>
                            </div>
                            <div className="text-center mb-10">
                                <div className="inline-block bg-primary text-white text-[10px] font-black uppercase tracking-widest px-3 py-1 mb-4 border-2 border-brutal-black">Available</div>
                                <h2 className="text-4xl font-black uppercase tracking-tighter mb-2">{name}</h2>
                                <p className="text-xs font-bold uppercase tracking-widest text-slate-400 italic">Senior Software Engineer</p>
                            </div>
                            <div className="grid grid-cols-3 gap-1 border-t-4 border-brutal-black pt-8">
                                <div className="text-center border-r-2 border-slate-100">
                                    <p className="text-[10px] font-black uppercase opacity-40 mb-2">Score</p>
                                    <p className="text-2xl font-black tabular-nums">{cand.score.total}</p>
                                </div>
                                <div className="text-center border-r-2 border-slate-100">
                                    <p className="text-[10px] font-black uppercase opacity-40 mb-2">Rank</p>
                                    <p className="text-2xl font-black tabular-nums">#{cand.rank}</p>
                                </div>
                                <div className="text-center">
                                    <p className="text-[10px] font-black uppercase opacity-40 mb-2">Match</p>
                                    <p className="text-2xl font-black tabular-nums">{cand.job_match.score}%</p>
                                </div>
                            </div>
                        </div>

                        <div className="brutalist-card bg-white p-8 border-4 border-primary shadow-[8px_8px_0px_0px_rgba(25,112,194,0.1)]">
                            <h3 className="flex items-center gap-3 text-lg font-black uppercase tracking-tight mb-8">
                                <span className="material-symbols-outlined text-primary">analytics</span>
                                Score Breakdown
                            </h3>
                            <div className="space-y-8">
                                {Object.entries(cand.score.breakdown).slice(0, 4).map(([key, val]: [string, any]) => (
                                    <div key={key}>
                                        <div className="flex justify-between text-[10px] font-black uppercase mb-3">
                                            <span className="tracking-widest opacity-60">{key.replace('_', ' ')}</span>
                                            <span className="tabular-nums font-mono">{val.toFixed(0)} / {key === 'internships' || key === 'skills' ? 20 : 10}</span>
                                        </div>
                                        <div className="h-4 bg-slate-50 border-2 border-brutal-black rounded-sm overflow-hidden relative">
                                            <div
                                                className="h-full bg-primary transition-all duration-1000 border-r-2 border-brutal-black shadow-[inset_-2px_0px_0px_0px_rgba(255,255,255,0.3)]"
                                                style={{ width: `${(val / (key === 'internships' || key === 'skills' ? 20 : 10)) * 100}%` }}
                                            ></div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                            <button className="w-full mt-10 py-4 bg-primary text-white border-2 border-brutal-black font-black uppercase text-sm tracking-widest shadow-hard hover:shadow-none hover:translate-x-1 hover:translate-y-1 transition-all">
                                Schedule Interview
                            </button>
                        </div>
                    </div>

                    {/* Right Column: Detailed Info */}
                    <div className="lg:col-span-8 space-y-12">
                        {/* AI Analysis Dashboard (Premium Feature) */}
                        {cand.job_match && cand.ai_insights && (
                            <section>
                                <AnalysisDashboard
                                    swot={cand.ai_insights.swot_analysis}
                                    questions={cand.ai_insights.interview_questions}
                                    aiPowered={cand.ai_insights.ai_powered}
                                    matchScores={{
                                        tfidf: cand.job_match.tfidf_similarity,
                                        semantic: cand.job_match.semantic_similarity,
                                        hybrid: cand.job_match.score
                                    }}
                                    skillMatch={cand.job_match.skill_analysis}
                                />
                            </section>
                        )}

                        {/* Skills Section */}
                        <section className="brutalist-card bg-white p-10 border-4">
                            <h3 className="text-2xl font-black uppercase tracking-tight mb-10 inline-block border-b-4 border-primary pb-2">Skills & Proficiencies</h3>
                            <div className="flex flex-wrap gap-3">
                                {cand.skills.map((skill: string, i: number) => (
                                    <span key={i} className="bg-white border-2 border-brutal-black px-5 py-2 font-black uppercase text-xs shadow-hard-sm hover:translate-y-[-2px] hover:shadow-hard cursor-default transition-all">
                                        {skill}
                                    </span>
                                ))}
                            </div>
                        </section>

                        {/* Projects Section */}
                        <section className="brutalist-card bg-white p-10 border-4 relative">
                            <div className="absolute top-0 right-0 p-8 opacity-10 pointer-events-none">
                                <span className="material-symbols-outlined text-[100px]">architecture</span>
                            </div>
                            <h3 className="text-2xl font-black uppercase tracking-tight mb-10">Key Projects</h3>
                            <div className="space-y-12">
                                {cand.projects.slice(0, 3).map((proj: string, i: number) => (
                                    <div key={i} className="group">
                                        <div className="flex justify-between items-start mb-4">
                                            <h4 className="text-xl font-black uppercase group-hover:text-primary transition-colors italic">"{proj.split(':')[0] || 'Project Delta'}"</h4>
                                            <span className="text-[10px] font-black font-mono opacity-40">2023</span>
                                        </div>
                                        <p className="text-sm font-bold text-slate-500 leading-relaxed max-w-2xl pl-4 border-l-4 border-slate-100">
                                            {proj.includes(':') ? proj.split(':')[1] : 'Developed a high-performance system architecture focused on scalability and low-latency data processing.'}
                                        </p>
                                    </div>
                                ))}
                            </div>
                        </section>

                        {/* Work Experience Section */}
                        <section className="brutalist-card bg-white p-10 border-4">
                            <h3 className="text-2xl font-black uppercase tracking-tight mb-12">Work Experience</h3>
                            <div className="space-y-0 relative">
                                <div className="absolute left-[7px] top-2 bottom-2 w-1 bg-slate-100"></div>
                                {cand.experience.length > 0 ? cand.experience.map((exp: string, i: number) => (
                                    <div key={i} className="pl-12 pb-12 last:pb-0 relative">
                                        <div className={`absolute left-0 top-1.5 size-4 border-2 border-brutal-black ${i === 0 ? 'bg-primary' : 'bg-white'} shadow-hard-sm`}></div>
                                        <div className="flex flex-col md:flex-row justify-between mb-4 gap-4">
                                            <h4 className="text-lg font-black uppercase tracking-tight">{exp}</h4>
                                            <span className="px-3 py-1 border-2 border-brutal-black text-[10px] font-black uppercase tracking-widest self-start">{i === 0 ? '2021 — PRESENT' : '2018 — 2021'}</span>
                                        </div>
                                        <p className="text-sm font-bold text-slate-500 max-w-2xl">Led engineering teams in developing complex cloud-native applications, improving overall system reliability and deployment frequency.</p>
                                    </div>
                                )) : (
                                    <div className="pl-12 pb-12 relative">
                                        <div className="absolute left-0 top-1.5 size-4 border-2 border-brutal-black bg-primary shadow-hard-sm"></div>
                                        <div className="flex flex-col md:flex-row justify-between mb-4 gap-4">
                                            <h4 className="text-lg font-black uppercase tracking-tight">Software Engineer @ OpenSource Dev</h4>
                                            <span className="px-3 py-1 border-2 border-brutal-black text-[10px] font-black uppercase tracking-widest self-start">2021 — PRESENT</span>
                                        </div>
                                        <p className="text-sm font-bold text-slate-500 max-w-2xl">Building scalable web architecture and contributing to core system modules.</p>
                                    </div>
                                )}
                            </div>
                        </section>

                        {/* Education Section */}
                        <section className="brutalist-card bg-white p-10 border-4">
                            <h3 className="text-2xl font-black uppercase tracking-tight mb-10">Education</h3>
                            <div className="flex gap-8 group">
                                <div className="size-16 bg-slate-50 border-2 border-brutal-black flex items-center justify-center rounded group-hover:bg-primary transition-colors group-hover:text-white">
                                    <span className="material-symbols-outlined text-3xl">school</span>
                                </div>
                                <div>
                                    <h4 className="text-lg font-black uppercase tracking-tight mb-2">B.S. Computer Science</h4>
                                    <p className="text-xs font-black uppercase tracking-widest text-slate-400 mb-4">{cand.education[0] || 'Unknown University'} • 2014 — 2018</p>
                                    <div className="p-4 bg-slate-50 border-2 border-dashed border-slate-200 font-bold italic text-sm text-slate-500">
                                        "Graduated with High Honors (GPA: {cand.cgpa})"
                                    </div>
                                </div>
                            </div>
                        </section>
                    </div>
                </div>

                <footer className="mt-20 pt-12 border-t-4 border-brutal-black/5 text-center">
                    <p className="text-[10px] font-black uppercase tracking-[0.4em] opacity-30 italic">© 2024 RESUMERANKER — SYSTEM STATUS: OPERATIONAL</p>
                </footer>
            </div>
            <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
        </div>
    )
}
