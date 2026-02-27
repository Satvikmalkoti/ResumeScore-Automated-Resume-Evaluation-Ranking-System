"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import AppNav from "@/components/app-nav"
import { BarChart, Bar, XAxis, ResponsiveContainer, Cell, Tooltip } from 'recharts'

export default function GraphPage() {
    const [data, setData] = useState<any>(null)
    const [checkedStorage, setCheckedStorage] = useState(false)

    useEffect(() => {
        const stored = sessionStorage.getItem("results")
        if (stored) setData(JSON.parse(stored))
        setCheckedStorage(true)
    }, [])

    if (!checkedStorage) return (
        <div className="flex items-center justify-center min-h-screen bg-background-light">
            <div className="text-4xl font-black uppercase tracking-tighter animate-pulse">Loading Graph...</div>
        </div>
    )

    if (!data) return (
        <div className="bg-background-light min-h-screen text-brutal-black font-sans p-8">
            <div className="max-w-7xl mx-auto">
                <AppNav className="mb-16 px-4" />
                <div className="brutalist-card bg-white p-10 border-4 text-center">
                    <div className="text-4xl font-black uppercase tracking-tighter mb-4">No Graph Data</div>
                    <p className="max-w-xl mx-auto font-bold uppercase tracking-widest text-slate-400 mb-10">
                        Upload a candidate pool to generate correlation views.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <Link href="/upload" className="brutalist-button-primary text-sm py-4 px-10">
                            Upload Pool
                        </Link>
                        <Link href="/analytics" className="brutalist-button text-sm py-4 px-10">
                            Analytics
                        </Link>
                    </div>
                </div>
            </div>
            <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
        </div>
    )

    const expData = [
        { name: 'Entry', count: data.results.filter((r: any) => r.experience_years <= 2).length, fill: '#141414' },
        { name: 'Mid', count: data.results.filter((r: any) => r.experience_years > 2 && r.experience_years <= 5).length, fill: '#141414' },
        { name: 'Senior', count: data.results.filter((r: any) => r.experience_years > 5 && r.experience_years <= 10).length, fill: '#141414' },
        { name: 'Expert', count: data.results.filter((r: any) => r.experience_years > 10).length, fill: '#ff4d00' },
    ]

    return (
        <div className="bg-background-light min-h-screen text-brutal-black font-sans p-8">
            <div className="max-w-7xl mx-auto">
                <AppNav
                    className="mb-20 px-4"
                    rightSlot={
                        <div className="hidden md:flex items-center gap-3">
                            <div className="bg-brutal-black text-white px-4 py-2 font-black uppercase tracking-widest text-xs rounded-full border-2 border-brutal-black">
                                Deep Graph
                            </div>
                            <button className="brutalist-button text-xs py-2">
                                Export JSON
                            </button>
                        </div>
                    }
                />

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 px-4 mb-20">
                    {/* Main Graph Area */}
                    <div className="lg:col-span-8 brutalist-card bg-white border-4 p-10 h-[600px] relative overflow-hidden group">
                        <div className="absolute top-0 right-0 p-8 opacity-5 pointer-events-none">
                            <span className="material-symbols-outlined text-[200px] rotate-12">hub</span>
                        </div>
                        <h2 className="text-2xl font-black uppercase tracking-tighter mb-4 italic">Skill Correlation Map</h2>
                        <p className="text-[10px] font-black uppercase tracking-[0.3em] opacity-40 mb-12">N-Dimensional Analysis of Cluster Relationships</p>

                        <div className="relative w-full h-[400px]">
                            <svg className="absolute inset-0 w-full h-full opacity-60">
                                <line x1="20%" y1="30%" x2="50%" y2="50%" stroke="#141414" strokeWidth="2" strokeDasharray="8 4" />
                                <line x1="50%" y1="50%" x2="80%" y2="40%" stroke="#141414" strokeWidth="2" strokeDasharray="8 4" />
                                <line x1="50%" y1="50%" x2="40%" y2="80%" stroke="#141414" strokeWidth="4" />
                                <line x1="40%" y1="80%" x2="70%" y2="70%" stroke="#141414" strokeWidth="2" strokeDasharray="4 2" />
                            </svg>

                            <div className="absolute top-[30%] left-[20%] size-24 bg-white border-4 border-brutal-black rounded-full flex flex-col items-center justify-center shadow-hard group-hover:rotate-12 transition-transform">
                                <span className="text-[10px] font-black uppercase">React</span>
                                <span className="text-xl font-black">88%</span>
                            </div>
                            <div className="absolute top-[50%] left-[50%] -translate-x-1/2 -translate-y-1/2 size-40 bg-primary border-4 border-brutal-black rounded-full flex flex-col items-center justify-center text-white shadow-hard group-hover:scale-110 transition-transform">
                                <span className="text-[12px] font-black uppercase tracking-widest">TypeScript</span>
                                <span className="text-4xl font-black italic">94%</span>
                            </div>
                            <div className="absolute top-[40%] left-[80%] size-20 bg-white border-4 border-brutal-black rounded-full flex flex-col items-center justify-center shadow-hard">
                                <span className="text-[10px] font-black uppercase">Node.js</span>
                                <span className="text-lg font-black">72%</span>
                            </div>
                            <div className="absolute top-[80%] left-[40%] size-28 bg-slate-100 border-4 border-brutal-black flex flex-col items-center justify-center shadow-hard group-hover:-rotate-3 transition-transform">
                                <span className="text-[10px] font-black uppercase text-center px-4">Cloud Infrastructure</span>
                                <span className="text-2xl font-black">65%</span>
                            </div>
                        </div>
                    </div>

                    {/* Right Metrics Panel */}
                    <div className="lg:col-span-4 space-y-8">
                        <div className="brutalist-card bg-brutal-black text-white p-8 group overflow-hidden relative">
                            <div className="absolute -bottom-4 -right-4 size-24 bg-primary rotate-12 opacity-80 group-hover:rotate-45 transition-transform"></div>
                            <h3 className="text-xs font-black uppercase tracking-widest opacity-60 mb-6">Insight of the Week</h3>
                            <p className="text-xl font-black leading-tight italic max-w-[200px]">"TS-driven architectures show 14% higher maintainability scores."</p>
                        </div>

                        <div className="brutalist-card bg-white border-4 p-8">
                            <h3 className="text-[10px] font-black uppercase tracking-widest mb-8 opacity-40">Experience Segments</h3>
                            <div className="h-[200px]">
                                <ResponsiveContainer width="100%" height="100%">
                                    <BarChart data={expData}>
                                        <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 9, fontWeight: 900 }} />
                                        <Bar dataKey="count" radius={[2, 2, 0, 0]}>
                                            {expData.map((entry, index) => (
                                                <Cell key={`cell-${index}`} fill={entry.fill} />
                                            ))}
                                        </Bar>
                                    </BarChart>
                                </ResponsiveContainer>
                            </div>
                        </div>

                        <div className="bg-yellow-400 border-4 border-brutal-black p-8 shadow-hard hover:shadow-none hover:translate-x-1 hover:translate-y-1 transition-all">
                            <p className="text-xs font-black uppercase mb-1 tracking-widest">System Anomaly</p>
                            <h4 className="text-2xl font-black italic mb-4">Cache Hit Rate 92%</h4>
                            <p className="text-[10px] font-black opacity-30 uppercase leading-relaxed tracking-widest">Optimized background parsing active for {data.stats.count} profiles.</p>
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 px-4 mb-32">
                    {[
                        { label: 'Entropy', value: '4.2', detail: 'Low variability' },
                        { label: 'Linearity', value: '0.9', detail: 'Consistent quality' },
                        { label: 'Density', value: '78%', detail: 'Skill saturation' },
                        { label: 'Outliers', value: '03', detail: 'Niche profiles' },
                    ].map((item, i) => (
                        <div key={i} className="brutalist-card bg-white p-8 border-4 group hover:bg-slate-50 transition-colors">
                            <p className="text-[10px] font-black uppercase tracking-widest opacity-40 mb-2">{item.label}</p>
                            <p className="text-4xl font-black italic mb-4">{item.value}</p>
                            <div className="flex items-center gap-2">
                                <div className="size-1 bg-primary rounded-full"></div>
                                <span className="text-[9px] font-black uppercase tracking-widest text-slate-400">{item.detail}</span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
            <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
        </div>
    )
}
