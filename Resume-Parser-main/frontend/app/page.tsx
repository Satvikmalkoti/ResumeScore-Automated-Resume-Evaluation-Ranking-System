"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function LandingPage() {
  return (
    <div className="bg-background-light font-sans text-brutal-black antialiased min-h-screen selection:bg-primary selection:text-white">
      {/* Top Navigation */}
      <nav className="fixed top-0 w-full z-50 px-6 py-8">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center gap-2 group cursor-pointer">
            <div className="size-10 bg-brutal-black flex items-center justify-center rounded-xl text-white">
              <span className="material-symbols-outlined text-2xl">auto_awesome</span>
            </div>
            <span className="text-xl font-black uppercase tracking-tighter">ResumeRanker</span>
          </div>

          {/* Centered Pill Menu */}
          <div className="hidden md:flex items-center gap-1 bg-white/80 backdrop-blur-md p-1.5 rounded-full border-2 border-brutal-black shadow-hard">
            <Link href="/" className="px-6 py-2 text-sm font-bold uppercase hover:bg-slate-100 rounded-full transition-colors">Home</Link>
            <Link href="/upload" className="px-6 py-2 text-sm font-bold uppercase hover:bg-slate-100 rounded-full transition-colors">App</Link>
            <Link href="/analytics" className="px-6 py-2 text-sm font-bold uppercase hover:bg-slate-100 rounded-full transition-colors">Analytics</Link>
          </div>

          {/* CTA Button */}
          <button className="bg-brutal-black text-white px-8 py-3 rounded-full text-sm font-black uppercase tracking-widest hover:bg-slate-800 transition-all active:translate-y-0.5">
            Login
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="pt-48 pb-32 px-6">
        <div className="max-w-5xl mx-auto text-center">
          <h1 className="text-[87px] leading-[0.9] font-black uppercase tracking-tighter mb-8 text-brutal-black">
            AI-Powered <br />
            Resume Screening <br />
            <span className="text-primary/40">In Seconds</span>
          </h1>
          <p className="text-[22px] font-medium max-w-2xl mx-auto mb-16 text-slate-600">
            Revolutionize your hiring process with our Brutalist-inspired AI tool. Upload and rank resumes instantly with GPT-4 class accuracy.
          </p>

          {/* Signature Large Input Bar */}
          <div className="relative max-w-3xl mx-auto h-[90px] bg-white rounded-xl border-2 border-brutal-black flex items-center p-2 group transition-all hover:-translate-y-1 shadow-hard hover:shadow-hard-lg">
            <div className="flex items-center gap-4 px-6 text-slate-400">
              <span className="material-symbols-outlined">upload_file</span>
              <span className="text-lg font-bold uppercase tracking-tight">Ready?</span>
            </div>
            <div className="flex-1 bg-transparent border-none focus:ring-0 text-lg font-bold uppercase px-4">
              Select your files
            </div>
            <Link href="/upload" className="h-full bg-brutal-black text-white px-10 rounded-lg text-lg font-black uppercase tracking-widest flex items-center justify-center hover:bg-slate-800 transition-all active:shadow-none active:translate-x-1 active:translate-y-1">
              Get Started
            </Link>
          </div>
        </div>
      </main>

      {/* Dark Section: How It Works */}
      <section className="bg-background-dark text-white py-32 px-6 relative overflow-hidden">
        <div className="absolute inset-0 grid-pattern opacity-30 pointer-events-none"></div>
        <div className="max-w-7xl mx-auto relative z-10">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
            {/* Steps List */}
            <div className="space-y-12">
              <h2 className="text-5xl font-black uppercase tracking-tighter mb-16">How it works</h2>

              <div className="flex gap-8 group">
                <div className="size-16 rounded-xl border-2 border-white/20 flex items-center justify-center shrink-0 group-hover:bg-primary group-hover:border-primary transition-colors">
                  <span className="text-2xl font-black italic">01</span>
                </div>
                <div>
                  <h3 className="text-2xl font-black uppercase tracking-tight mb-2">Upload Files</h3>
                  <p className="text-slate-400 text-lg">Drag and drop your candidate pool. We support PDFs, DOCX, and LinkedIn exports.</p>
                </div>
              </div>

              <div className="flex gap-8 group">
                <div className="size-16 rounded-xl border-2 border-white/20 flex items-center justify-center shrink-0 group-hover:bg-primary group-hover:border-primary transition-colors">
                  <span className="text-2xl font-black italic">02</span>
                </div>
                <div>
                  <h3 className="text-2xl font-black uppercase tracking-tight mb-2">AI Analysis</h3>
                  <p className="text-slate-400 text-lg">Our custom-trained LLM parses every detail, checking for specific skill overlaps and cultural fit indicators.</p>
                </div>
              </div>

              <div className="flex gap-8 group">
                <div className="size-16 rounded-xl border-2 border-white/20 flex items-center justify-center shrink-0 group-hover:bg-primary group-hover:border-primary transition-colors">
                  <span className="text-2xl font-black italic">03</span>
                </div>
                <div>
                  <h3 className="text-2xl font-black uppercase tracking-tight mb-2">Ranked Results</h3>
                  <p className="text-slate-400 text-lg">Get a sorted list of top talent with detailed reasoning for every rank assigned.</p>
                </div>
              </div>
            </div>

            {/* Floating Mockup Card */}
            <div className="relative">
              <div className="bg-white rounded-xl border-2 border-brutal-black p-8 text-slate-900 transform rotate-2 hover:rotate-0 transition-transform duration-500 shadow-hard">
                <div className="flex items-center justify-between mb-8 border-b-2 border-slate-100 pb-4">
                  <h4 className="font-black uppercase tracking-widest text-sm">Analysis Results</h4>
                  <span className="bg-primary/10 text-primary px-3 py-1 rounded-full text-xs font-bold uppercase tracking-widest">Job: Sr. Engineer</span>
                </div>
                <div className="space-y-6">
                  <div className="p-4 bg-slate-50 rounded-lg flex items-center justify-between border-2 border-transparent hover:border-brutal-black transition-all">
                    <div className="flex items-center gap-4">
                      <div className="size-10 bg-slate-200 rounded-full"></div>
                      <div>
                        <p className="font-bold uppercase text-sm">Alex Rivera</p>
                        <p className="text-xs text-slate-500">8 Years Experience</p>
                      </div>
                    </div>
                    <span className="text-2xl font-black text-primary">98</span>
                  </div>
                  <div className="p-4 bg-slate-50 rounded-lg flex items-center justify-between border-2 border-transparent hover:border-brutal-black transition-all">
                    <div className="flex items-center gap-4">
                      <div className="size-10 bg-slate-200 rounded-full"></div>
                      <div>
                        <p className="font-bold uppercase text-sm">Sarah Chen</p>
                        <p className="text-xs text-slate-500">5 Years Experience</p>
                      </div>
                    </div>
                    <span className="text-2xl font-black text-slate-400">92</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer Area */}
      <footer className="bg-background-light py-20 px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8 border-2 border-brutal-black rounded-xl p-12 bg-white shadow-hard">
          <div className="space-y-4 text-center md:text-left">
            <h3 className="text-4xl font-black uppercase tracking-tighter">Ready to optimize?</h3>
            <p className="text-slate-500 font-bold uppercase text-sm tracking-widest">Join 500+ top-tier HR teams today.</p>
          </div>
          <div className="flex gap-4">
            <button className="bg-white border-2 border-brutal-black text-brutal-black px-10 py-4 rounded-xl text-lg font-black uppercase tracking-widest shadow-hard hover:-translate-y-1 transition-all active:translate-y-0.5 active:shadow-none">
              Schedule Demo
            </button>
            <Link href="/upload" className="bg-brutal-black text-white px-10 py-4 rounded-xl text-lg font-black uppercase tracking-widest shadow-hard hover:-translate-y-1 transition-all active:translate-y-0.5 active:shadow-none flex items-center justify-center">
              Get Started
            </Link>
          </div>
        </div>
        <div className="max-w-7xl mx-auto mt-16 text-center text-slate-400 font-bold uppercase text-xs tracking-[0.2em]">
          © 2024 ResumeRanker Inc. — All rights reserved. Built with precision.
        </div>
      </footer>

      {/* Material Symbols Font Link (if not in layout) */}
      <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
    </div>
  )
}
