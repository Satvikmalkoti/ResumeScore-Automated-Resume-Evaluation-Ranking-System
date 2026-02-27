import React from 'react';

interface SWOT {
    strengths: string[];
    weaknesses: string[];
    opportunities: string[];
    threats: string[];
}

interface Question {
    question: string;
    type: string;
    skill_tested: string;
    difficulty: string;
}

interface Props {
    swot: SWOT;
    questions: Question[];
    matchScores: {
        tfidf: number;
        semantic: number;
        hybrid: number;
    };
    skillMatch: any;
    aiPowered?: boolean;
}

export default function AnalysisDashboard({ swot, questions, matchScores, skillMatch, aiPowered }: Props) {
    return (
        <div className="space-y-12">
            {/* Premium Match Scores */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="brutalist-card bg-white p-6 border-4 border-brutal-black hover:-translate-y-1 transition-all">
                    <p className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-2">Keyword Match (TF-IDF)</p>
                    <div className="flex items-baseline gap-1">
                        <p className="text-4xl font-black">{matchScores.tfidf}</p>
                        <p className="text-sm font-black opacity-30">%</p>
                    </div>
                </div>
                <div className="brutalist-card bg-white p-6 border-4 border-primary hover:-translate-y-1 transition-all shadow-hard-sm">
                    <p className="text-[10px] font-black uppercase tracking-widest text-primary mb-2">Semantic Intel</p>
                    <div className="flex items-baseline gap-1">
                        <p className="text-4xl font-black text-primary">{matchScores.semantic}</p>
                        <p className="text-sm font-black text-primary opacity-30">%</p>
                    </div>
                </div>
                <div className="brutalist-card bg-brutal-black p-6 border-4 border-brutal-black hover:-translate-y-1 transition-all text-white shadow-hard flex flex-col justify-center">
                    <p className="text-[10px] font-black uppercase tracking-widest opacity-60 mb-2 text-white">Hybrid Rank Score</p>
                    <div className="flex items-baseline gap-4">
                        <p className="text-5xl font-black italic">{matchScores.hybrid}</p>
                        <span className="material-symbols-outlined text-primary text-3xl">verified</span>
                    </div>
                </div>
            </div>

            {/* AI SWOT Analysis */}
            <div className="brutalist-card bg-white border-4 p-10 relative overflow-hidden">
                <div className="absolute top-0 right-0 p-8 opacity-5 pointer-events-none">
                    <span className="material-symbols-outlined text-[150px]">psychology</span>
                </div>

                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-10">
                    <h3 className="text-2xl font-black uppercase tracking-tight flex items-center gap-3">
                        <span className="material-symbols-outlined text-primary">analytics</span>
                        AI SWOT Analysis
                    </h3>
                    <div className={`inline-flex items-center gap-2 px-3 py-1 border-2 border-brutal-black text-[10px] font-black uppercase tracking-widest ${aiPowered ? 'bg-primary text-white' : 'bg-yellow-400 text-brutal-black'}`}>
                        <span className="material-symbols-outlined text-sm">{aiPowered ? 'bolt' : 'warning'}</span>
                        {aiPowered ? 'AI POWERED' : 'FALLBACK MODE'}
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 relative z-10">
                    <div className="space-y-4">
                        <h4 className="text-sm font-black uppercase tracking-widest text-green-600 flex items-center gap-2">
                            <span className="material-symbols-outlined text-sm">check_circle</span>
                            Strengths
                        </h4>
                        <ul className="space-y-3">
                            {swot.strengths.map((s, i) => (
                                <li key={i} className="text-sm font-bold border-l-4 border-green-200 pl-4 py-1">{s}</li>
                            ))}
                        </ul>
                    </div>
                    <div className="space-y-4">
                        <h4 className="text-sm font-black uppercase tracking-widest text-red-600 flex items-center gap-2">
                            <span className="material-symbols-outlined text-sm">warning</span>
                            Potential Gaps
                        </h4>
                        <ul className="space-y-3">
                            {swot.weaknesses.map((w, i) => (
                                <li key={i} className="text-sm font-bold border-l-4 border-red-200 pl-4 py-1">{w}</li>
                            ))}
                        </ul>
                    </div>
                    <div className="space-y-4">
                        <h4 className="text-sm font-black uppercase tracking-widest text-blue-600 flex items-center gap-2">
                            <span className="material-symbols-outlined text-sm">trending_up</span>
                            Opportunities
                        </h4>
                        <ul className="space-y-3">
                            {swot.opportunities.map((o, i) => (
                                <li key={i} className="text-sm font-bold border-l-4 border-blue-200 pl-4 py-1">{o}</li>
                            ))}
                        </ul>
                    </div>
                    <div className="space-y-4">
                        <h4 className="text-sm font-black uppercase tracking-widest text-orange-600 flex items-center gap-2">
                            <span className="material-symbols-outlined text-sm">error</span>
                            Considerations
                        </h4>
                        <ul className="space-y-3">
                            {swot.threats.map((t, i) => (
                                <li key={i} className="text-sm font-bold border-l-4 border-orange-200 pl-4 py-1">{t}</li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>

            {/* Semantic Matching Details */}
            <div className="brutalist-card bg-slate-50 border-4 border-dashed p-8">
                <h3 className="text-sm font-black uppercase tracking-widest mb-6 flex items-center gap-2">
                    <span className="material-symbols-outlined text-primary">hub</span>
                    Semantic Skill Context
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {skillMatch.matched_skills?.map((match: any, i: number) => (
                        <div key={i} className="bg-white border-2 border-brutal-black p-3 flex justify-between items-center shadow-hard-sm">
                            <div className="flex flex-col">
                                <span className="text-[10px] font-black uppercase opacity-40 italic">Candidate claimed</span>
                                <span className="text-xs font-black">"{match.resume_skill}"</span>
                            </div>
                            <span className="material-symbols-outlined text-slate-300">double_arrow</span>
                            <div className="flex flex-col text-right">
                                <span className="text-[10px] font-black uppercase opacity-40 italic">Matches JD</span>
                                <span className="text-xs font-black text-primary">"{match.matches}"</span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Interview Question Generator */}
            <div className="brutalist-card bg-white border-4 p-10">
                <h3 className="text-2xl font-black uppercase tracking-tight mb-10 flex items-center gap-3">
                    <span className="material-symbols-outlined text-primary">question_answer</span>
                    Tailored Interview Questions
                </h3>
                <div className="space-y-6">
                    {questions.map((q, i) => (
                        <div key={i} className="border-2 border-brutal-black p-6 group hover:translate-x-1 transition-all relative overflow-hidden shadow-hard-sm hover:shadow-hard">
                            <div className="absolute top-0 right-0 p-2">
                                <span className={`text-[8px] font-black uppercase tracking-widest px-2 py-1 border border-brutal-black ${q.difficulty === 'hard' ? 'bg-red-500 text-white' :
                                        q.difficulty === 'medium' ? 'bg-yellow-400' : 'bg-green-400'
                                    }`}>
                                    {q.difficulty}
                                </span>
                            </div>
                            <p className="text-lg font-black italic mb-4">"{q.question}"</p>
                            <div className="flex gap-3">
                                <span className="text-[10px] bg-slate-100 px-3 py-1 font-black uppercase tracking-widest">{q.type}</span>
                                <span className="text-[10px] bg-primary/10 text-primary px-3 py-1 font-black uppercase tracking-widest border border-primary/20">{q.skill_tested}</span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
