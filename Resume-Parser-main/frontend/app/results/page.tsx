"use client"

import { useEffect, useState } from "react"
import Link from "next/link"

export default function ResultsPage() {
  const [data, setData] = useState<any>(null)

  useEffect(() => {
    const stored = sessionStorage.getItem("results")
    if (stored) setData(JSON.parse(stored))
  }, [])

  if (!data) return (
    <div className="flex items-center justify-center min-h-screen bg-background-light">
      <div className="text-4xl font-black uppercase tracking-tighter animate-pulse">Analyzing Pool...</div>
    </div>
  )

  return (
    <div className="bg-background-light min-h-screen text-brutal-black font-sans p-8">
      <div className="max-w-7xl mx-auto">
        <header className="flex justify-between items-center mb-16 px-4">
          <Link href="/" className="flex items-center gap-2 group">
            <div className="size-10 bg-brutal-black flex items-center justify-center rounded-xl text-white group-hover:rotate-12 transition-transform shadow-hard">
              <span className="material-symbols-outlined text-2xl">auto_awesome</span>
            </div>
            <span className="text-xl font-black uppercase tracking-tighter">ResumeRanker</span>
          </Link>
          <div className="flex items-center gap-8">
            <nav className="hidden md:flex gap-6 font-black uppercase text-xs tracking-widest">
              <Link href="/" className="hover:text-primary transition-colors italic">Dashboard</Link>
              <Link href="/results" className="text-primary underline underline-offset-4 decoration-4">Candidates</Link>
              <Link href="#" className="hover:text-primary transition-colors">Jobs</Link>
              <Link href="#" className="hover:text-primary transition-colors">Settings</Link>
            </nav>
            <div className="flex items-center gap-4 border-l-2 border-brutal-black pl-8">
              <span className="material-symbols-outlined hover:bg-slate-100 p-2 rounded-full cursor-pointer transition-colors">notifications</span>
              <div className="size-10 bg-slate-200 rounded-full border-2 border-brutal-black overflow-hidden shadow-hard-sm">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="User" className="w-full h-full object-cover" />
              </div>
            </div>
          </div>
        </header>

        <section className="px-4 mb-20">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-8 mb-4">
            <div>
              <h1 className="text-[100px] font-black uppercase tracking-[calc(-0.05em)] leading-[0.85] mb-4">
                Top <span className="text-primary">Candidates</span>
              </h1>
              <p className="text-lg font-bold uppercase tracking-widest text-slate-400">AI-driven analysis for the uploaded pool.</p>
            </div>
            <div className="flex gap-4">
              <button className="px-8 py-3 bg-white border-2 border-brutal-black font-black uppercase text-sm tracking-widest shadow-hard hover:shadow-none hover:translate-x-1 hover:translate-y-1 transition-all flex items-center gap-2">
                <span className="material-symbols-outlined text-lg">download</span>
                Export CSV
              </button>
              <button className="px-8 py-3 bg-primary text-white border-2 border-brutal-black font-black uppercase text-sm tracking-widest shadow-hard hover:shadow-none hover:translate-x-1 hover:translate-y-1 transition-all">
                Refresh Rankings
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
            {[
              { label: 'Total Evaluated', value: data.stats.count, color: 'bg-white' },
              { label: 'High Potential', value: data.results.filter((r: any) => r.score.total > 80).length, color: 'bg-white text-primary' },
              { label: 'Global Avg. Match', value: `${data.stats.avg_score}%`, color: 'bg-white' },
            ].map((stat, i) => (
              <div key={i} className={`brutalist-card p-10 ${stat.color} border-4 group hover:-rotate-1 transition-transform`}>
                <p className="text-xs font-black uppercase tracking-[0.2em] opacity-60 mb-8">{stat.label}</p>
                <p className="text-6xl font-black tabular-nums">{stat.value}</p>
              </div>
            ))}
          </div>
        </section>

        <div className="space-y-8 px-4 mb-32">
          {data.results.map((cand: any, i: number) => (
            <div key={i} className="brutalist-card bg-white p-8 flex flex-col md:flex-row items-center justify-between gap-12 group hover:shadow-hard-lg transition-all border-4 relative overflow-hidden">
              <div className={`absolute top-0 left-0 w-2 h-full ${i === 0 ? 'bg-yellow-400' : i === 1 ? 'bg-slate-300' : 'bg-orange-400'}`}></div>
              <div className="flex items-center gap-10 flex-1">
                <div className={`size-16 flex items-center justify-center border-2 border-brutal-black ${i === 0 ? 'bg-yellow-400' : 'bg-slate-100'}`}>
                  {i === 0 ? (
                    <span className="material-symbols-outlined text-3xl font-black">rewarded_ads</span>
                  ) : (
                    <span className="text-2xl font-black">{i + 1}</span>
                  )}
                </div>
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-[10px] font-black uppercase tracking-widest text-slate-400">{i === 0 ? '1ST RANK' : i === 1 ? '2ND RANK' : i === 2 ? '3RD RANK' : 'STANDARD RANK'}</span>
                    {i < 3 && <span className="text-[10px] bg-brutal-black text-white px-2 py-0.5 font-black uppercase tracking-widest">Verified</span>}
                  </div>
                  <h3 className="text-3xl font-black uppercase tracking-tighter mb-4">{cand.filename.split('.')[0]}</h3>
                  <div className="flex gap-2 flex-wrap">
                    {cand.skills.slice(0, 4).map((s: string, j: number) => (
                      <span key={j} className="text-[10px] font-black uppercase border-2 border-brutal-black px-3 py-1 bg-white hover:bg-slate-50 cursor-default">{s}</span>
                    ))}
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-16 shrink-0 w-full md:w-auto border-t-2 md:border-t-0 md:border-l-2 border-slate-100 pt-8 md:pt-0 md:pl-16">
                <div className="text-center md:text-left">
                  <p className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-2">AI Match Score</p>
                  <div className="flex items-baseline gap-1">
                    <span className="text-5xl font-black font-mono">{cand.job_match.score}</span>
                    <span className="text-xl font-black opacity-30">/100</span>
                  </div>
                </div>
                <Link
                  href={`/candidate/${i}`}
                  className="px-8 py-4 border-2 border-dashed border-brutal-black font-black uppercase text-sm tracking-widest hover:bg-brutal-black hover:text-white hover:border-solid transition-all flex items-center gap-2 group/btn shadow-[4px_4px_0px_0px_rgba(0,0,0,0.1)] hover:shadow-none"
                >
                  Full Profile
                  <span className="material-symbols-outlined group-hover/btn:translate-x-1 transition-transform">arrow_forward</span>
                </Link>
              </div>
            </div>
          ))}

          <div className="flex justify-center pt-12">
            <button className="px-12 py-5 border-4 border-brutal-black bg-white font-black uppercase text-lg tracking-tighter shadow-hard hover:shadow-none hover:translate-x-1 hover:translate-y-1 transition-all flex items-center gap-4 italic group">
              View More Results
              <span className="material-symbols-outlined group-hover:translate-y-1 transition-transform">keyboard_arrow_down</span>
            </button>
          </div>
        </div>
      </div>
      <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
    </div>
  )
}
