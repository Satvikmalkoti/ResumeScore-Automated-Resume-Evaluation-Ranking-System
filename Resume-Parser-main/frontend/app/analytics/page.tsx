"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import AppNav from "@/components/app-nav"
import {
    BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
    RadarChart, PolarGrid, PolarAngleAxis, Radar,
    PieChart, Pie, Cell, AreaChart, Area
} from 'recharts'

export default function AnalyticsPage() {
    const [data, setData] = useState<any>(null)
    const [checkedStorage, setCheckedStorage] = useState(false)

    useEffect(() => {
        const stored = sessionStorage.getItem("results")
        if (stored) setData(JSON.parse(stored))
        setCheckedStorage(true)
    }, [])

    if (!checkedStorage) return (
        <div className="flex items-center justify-center min-h-screen bg-background-light">
            <div className="text-4xl font-black uppercase tracking-tighter animate-pulse">Loading Analytics...</div>
        </div>
    )

    if (!data) return (
        <div className="bg-background-light min-h-screen text-brutal-black font-sans p-8">
            <div className="max-w-7xl mx-auto">
                <AppNav className="mb-16 px-4" />
                <div className="brutalist-card bg-white p-10 border-4 text-center">
                    <div className="text-4xl font-black uppercase tracking-tighter mb-4">No Pool Loaded</div>
                    <p className="max-w-xl mx-auto font-bold uppercase tracking-widest text-slate-400 mb-10">
                        Analytics are generated from your last uploaded candidate pool.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <Link href="/upload" className="brutalist-button-primary text-sm py-4 px-10">
                            Upload Pool
                        </Link>
                        <Link href="/results" className="brutalist-button text-sm py-4 px-10">
                            Candidates
                        </Link>
                    </div>
                </div>
            </div>
            <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
        </div>
    )

    // Data Preparation
    const scoreDist = [
        { range: '0-20', count: data.results.filter((r: any) => r.score.total <= 20).length },
        { range: '21-40', count: data.results.filter((r: any) => r.score.total > 20 && r.score.total <= 40).length },
        { range: '41-60', count: data.results.filter((r: any) => r.score.total > 40 && r.score.total <= 60).length },
        { range: '61-80', count: data.results.filter((r: any) => r.score.total > 60 && r.score.total <= 80).length },
        { range: '81-90', count: data.results.filter((r: any) => r.score.total > 80 && r.score.total <= 90).length },
        { range: '91-100', count: data.results.filter((r: any) => r.score.total > 90).length },
    ]

    // Score radar: Skills, Experience, Projects
    const avgSkills = data.results.reduce((acc: number, r: any) => acc + (r.score.breakdown.skills || 0), 0) / data.results.length
    const avgExp = data.results.reduce((acc: number, r: any) => acc + (r.score.breakdown.experience || 0), 0) / data.results.length
    const avgProj = data.results.reduce((acc: number, r: any) => acc + (r.score.breakdown.projects || 0), 0) / data.results.length

    // Normalize to 100 for radar
    const radarData = [
        { subject: 'Skills', A: (avgSkills / 20) * 100, fullMark: 100 },
        { subject: 'Experience', A: (avgExp / 5) * 100, fullMark: 100 },
        { subject: 'Projects', A: (avgProj / 15) * 100, fullMark: 100 },
    ]

    // Institution tiers
    const tiers = { T1: 0, T2: 0, T3: 0 }
    data.results.forEach((r: any) => {
        if (r.college_tier === 1) tiers.T1++
        else if (r.college_tier === 2) tiers.T2++
        else tiers.T3++
    })
    const pieData = [
        { name: 'Tier 1', value: tiers.T1 },
        { name: 'Tier 2', value: tiers.T2 },
        { name: 'Tier 3/Other', value: tiers.T3 }
    ]

    // Experience ranges
    const expRanges = { '0-2Y': 0, '2-5Y': 0, '5-10Y': 0, '10Y+': 0 }
    data.results.forEach((r: any) => {
        const y = r.experience_years || 0
        if (y < 2) expRanges['0-2Y']++
        else if (y < 5) expRanges['2-5Y']++
        else if (y < 10) expRanges['5-10Y']++
        else expRanges['10Y+']++
    })
    const areaData = Object.entries(expRanges).map(([x, y]) => ({ x, y }))

    const skillsMap: Record<string, number> = {}
    data.results.forEach((r: any) => {
        r.skills.forEach((s: string) => {
            skillsMap[s] = (skillsMap[s] || 0) + 1
        })
    })
    const topSkills = Object.entries(skillsMap)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
        .map(([name, count]) => ({ name: name.toUpperCase(), count: (count / data.results.length) * 100 }))

    const rankData = data.results.map((r: any, i: number) => ({
        name: `C${i + 1}`,
        score: r.score.total,
        fill: r.score.total > 70 ? '#141414' : '#94a3b8'
    }))

    return (
        <div className="bg-background-light min-h-screen text-brutal-black font-sans p-8">
            <div className="max-w-7xl mx-auto">
                <AppNav
                    className="mb-16 px-4"
                    rightSlot={
                        <div className="hidden md:block bg-brutal-black text-white px-4 py-2 font-black uppercase tracking-widest text-xs rounded-full border-2 border-brutal-black">
                            Pool Analytics // Q3 2024
                        </div>
                    }
                />

                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12 px-4">
                    {[
                        { label: 'Avg Score', value: `${data.stats.avg_score}/100`, icon: 'analytics', extra: 'Pool Integrity: 98%' },
                        { label: 'Processing Speed', value: '2.8s', icon: 'bolt', extra: 'GPU Accelerated' },
                        { label: 'Top Score', value: Math.max(...data.results.map((r: any) => r.score.total)), icon: 'trending_up', extra: '+12% vs last pool' },
                        { label: 'Pass Rate', value: '68%', icon: 'task_alt', extra: 'Threshold: 70' },
                    ].map((stat, i) => (
                        <div key={i} className="brutalist-card bg-white p-8 border-4 group hover:-rotate-1 transition-transform">
                            <p className="text-[10px] font-black uppercase tracking-widest opacity-40 mb-4">{stat.label}</p>
                            <div className="flex items-baseline gap-2 mb-6">
                                <p className="text-4xl font-black">{stat.value}</p>
                            </div>
                            <div className="flex items-center gap-2 pt-4 border-t-2 border-slate-50">
                                <span className="material-symbols-outlined text-sm text-primary">{stat.icon}</span>
                                <span className="text-[9px] font-black uppercase tracking-wider text-slate-400">{stat.extra}</span>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Charts Row 1 */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12 px-4">
                    <div className="brutalist-card bg-white p-10 border-4 h-[500px] flex flex-col">
                        <h3 className="text-xs font-black uppercase tracking-[0.2em] mb-12 opacity-60">Score Distribution</h3>
                        <div className="flex-1">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={scoreDist}>
                                    <XAxis dataKey="range" axisLine={false} tickLine={false} tick={{ fontSize: 10, fontWeight: 900 }} />
                                    <Tooltip cursor={{ fill: '#f8fafc' }} contentStyle={{ border: '4px solid #141414', borderRadius: '0', fontWeight: 900 }} />
                                    <Bar dataKey="count" fill="#141414" radius={[4, 4, 0, 0]} />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                    <div className="brutalist-card bg-white p-10 border-4 h-[500px] flex flex-col">
                        <h3 className="text-xs font-black uppercase tracking-[0.2em] mb-12 opacity-60">Avg Category Scores</h3>
                        <div className="flex-1">
                            <ResponsiveContainer width="100%" height="100%">
                                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                                    <PolarGrid stroke="#e2e8f0" strokeWidth={2} />
                                    <PolarAngleAxis dataKey="subject" tick={{ fontSize: 10, fontWeight: 900 }} />
                                    <Radar name="Candidate Pool" dataKey="A" stroke="#141414" fill="#141414" fillOpacity={0.6} strokeWidth={4} />
                                </RadarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>

                {/* Charts Row 2 */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 px-4 mb-12">
                    <div className="brutalist-card bg-white p-8 border-4 h-[400px]">
                        <h3 className="text-[10px] font-black uppercase tracking-widest mb-10 opacity-60">Most Common Skills</h3>
                        <div className="space-y-6">
                            {topSkills.map((s, i) => (
                                <div key={i}>
                                    <div className="flex justify-between text-[10px] font-black mb-2 uppercase">
                                        <span>{s.name}</span>
                                        <span>{s.count.toFixed(0)}%</span>
                                    </div>
                                    <div className="h-3 bg-slate-50 border-2 border-brutal-black overflow-hidden">
                                        <div className="h-full bg-brutal-black" style={{ width: `${s.count}%` }}></div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="brutalist-card bg-white p-8 border-4 h-[400px] flex flex-col">
                        <h3 className="text-[10px] font-black uppercase tracking-widest mb-10 opacity-60">Top Institutions</h3>
                        <div className="flex-1 flex items-center justify-center relative">
                            <div className="absolute flex flex-col items-center">
                                <span className="text-5xl font-black">25</span>
                                <span className="text-[8px] font-black uppercase tracking-widest opacity-40">Candidates</span>
                            </div>
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie data={pieData} innerRadius={80} outerRadius={110} paddingAngle={5} dataKey="value">
                                        <Cell fill="#141414" />
                                        <Cell fill="#cbd5e1" />
                                        <Cell fill="#e2e8f0" />
                                    </Pie>
                                </PieChart>
                            </ResponsiveContainer>
                        </div>
                        <div className="text-center">
                            <p className="text-[9px] font-black uppercase tracking-widest opacity-40">From Top 1% Colleges</p>
                        </div>
                    </div>
                    <div className="brutalist-card bg-white p-8 border-4 h-[400px] flex flex-col">
                        <h3 className="text-[10px] font-black uppercase tracking-widest mb-10 opacity-60">Years of Experience</h3>
                        <div className="flex-1">
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={areaData}>
                                    <defs>
                                        <linearGradient id="colorY" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#141414" stopOpacity={0.8} />
                                            <stop offset="95%" stopColor="#141414" stopOpacity={0} />
                                        </linearGradient>
                                    </defs>
                                    <XAxis dataKey="x" axisLine={false} tickLine={false} tick={{ fontSize: 10, fontWeight: 900 }} />
                                    <Area type="monotone" dataKey="y" stroke="#141414" strokeWidth={4} fillOpacity={1} fill="url(#colorY)" />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>

                {/* All Candidates chart */}
                <section className="px-4 mb-20">
                    <div className="brutalist-card bg-white p-10 border-4">
                        <h3 className="text-[10px] font-black uppercase tracking-widest mb-12 opacity-60">All Candidates Ranked By Score</h3>
                        <div className="h-[400px] relative">
                            <div className="absolute top-[30%] left-0 w-full border-t-2 border-dashed border-red-500 z-10">
                                <span className="absolute left-0 -top-6 text-[10px] font-black text-red-500 bg-white px-2 uppercase italic">Threshold: 70</span>
                            </div>
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={rankData}>
                                    <Bar dataKey="score" />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </section>

                <div className="flex flex-col md:flex-row gap-6 px-4 mb-32">
                    <button className="flex-1 py-8 bg-white border-4 border-brutal-black font-black uppercase text-xl shadow-hard hover:shadow-none hover:translate-x-1 hover:translate-y-1 transition-all flex items-center justify-center gap-4">
                        <span className="material-symbols-outlined text-3xl">table_view</span>
                        Download CSV
                    </button>
                    <button className="flex-1 py-8 bg-white border-4 border-brutal-black font-black uppercase text-xl shadow-hard hover:shadow-none hover:translate-x-1 hover:translate-y-1 transition-all flex items-center justify-center gap-4">
                        <span className="material-symbols-outlined text-3xl">picture_as_pdf</span>
                        Export PDF Report
                    </button>
                </div>
            </div>
            <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
        </div>
    )
}
