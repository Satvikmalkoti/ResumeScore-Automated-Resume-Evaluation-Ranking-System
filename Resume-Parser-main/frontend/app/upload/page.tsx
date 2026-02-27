"use client"
import Link from "next/link"

import { useState } from "react"
import { useRouter } from "next/navigation"
import AppNav from "@/components/app-nav"

export default function UploadPage() {
    const [files, setFiles] = useState<File[]>([])
    const [jobDescription, setJobDescription] = useState("")
    const [isUploading, setIsUploading] = useState(false)
    const router = useRouter()

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFiles(Array.from(e.target.files))
        }
    }

    const handleUpload = async () => {
        if (files.length === 0 || !jobDescription) return

        setIsUploading(true)
        const formData = new FormData()
        files.forEach(file => formData.append("files", file))
        formData.append("job_description", jobDescription)

        try {
            const response = await fetch("/api/match-job", {
                method: "POST",
                body: formData,
            })
            if (!response.ok) {
                const errorData = await response.json()
                alert(`Analysis failed: ${errorData.detail || 'Unknown error'}`)
                setIsUploading(false)
                return
            }
            const data = await response.json()
            sessionStorage.setItem("results", JSON.stringify(data))
            router.push("/results")
        } catch (error) {
            console.error("Upload failed:", error)
        } finally {
            setIsUploading(false)
        }
    }

    return (
        <div className="bg-background-light min-h-screen text-brutal-black font-sans p-8 grid-pattern opacity-100">
            <div className="max-w-6xl mx-auto">
                <AppNav className="mb-12" />

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Left: Upload and Config */}
                    <div className="lg:col-span-2 space-y-8">
                        <div className="brutalist-card p-8">
                            <h2 className="text-3xl font-black mb-6 flex items-center gap-3">
                                <span className="material-symbols-outlined">upload</span>
                                Upload Resumes
                            </h2>

                            <div
                                className="border-4 border-dashed border-slate-200 p-12 text-center hover:border-brutal-black transition-colors cursor-pointer"
                                onClick={() => document.getElementById('file-input')?.click()}
                            >
                                <input
                                    id="file-input"
                                    type="file"
                                    multiple
                                    className="hidden"
                                    onChange={handleFileChange}
                                />
                                <span className="material-symbols-outlined text-6xl text-slate-300 block mb-4">cloud_upload</span>
                                <p className="text-xl font-bold uppercase tracking-tight text-slate-400">Drag & drop files or click to browse</p>
                                <p className="text-sm font-bold uppercase tracking-widest text-slate-300 mt-2">PDF, DOCX supported • Max 10MB per file</p>
                            </div>

                            {files.length > 0 && (
                                <div className="mt-8 space-y-3">
                                    <h3 className="font-black uppercase text-sm tracking-widest">Selected Files ({files.length})</h3>
                                    {files.map((file, i) => (
                                        <div key={i} className="flex justify-between items-center bg-slate-50 p-3 border-2 border-slate-100 font-bold uppercase text-xs">
                                            <span>{file.name}</span>
                                            <span className="text-slate-400">{(file.size / 1024).toFixed(1)} KB</span>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>

                        <div className="brutalist-card p-8">
                            <h2 className="text-3xl font-black mb-6 flex items-center gap-3">
                                <span className="material-symbols-outlined">description</span>
                                Job Description
                            </h2>
                            <textarea
                                className="w-full h-64 brutalist-input font-medium text-sm normal-case"
                                placeholder="Paste the target job description here for intelligent matching..."
                                value={jobDescription}
                                onChange={(e) => setJobDescription(e.target.value)}
                            />
                        </div>
                    </div>

                    {/* Right: Scoring Config */}
                    <div className="space-y-8">
                        <div className="brutalist-card p-8 bg-primary">
                            <h2 className="text-3xl font-black mb-8 text-white">Scoring Config</h2>
                            <div className="space-y-6">
                                {[
                                    { name: 'Internships', val: 20 },
                                    { name: 'Core Skills', val: 20 },
                                    { name: 'Projects', val: 15 },
                                    { name: 'CGPA Score', val: 10 },
                                    { name: 'Achievements', val: 10 },
                                    { name: 'Other Stats', val: 25 },
                                ].map((stat, i) => (
                                    <div key={i} className="space-y-2">
                                        <div className="flex justify-between font-black uppercase tracking-widest text-xs text-white">
                                            <span>{stat.name}</span>
                                            <span>{stat.val}%</span>
                                        </div>
                                        <div className="h-3 bg-white/20 border-2 border-brutal-black">
                                            <div className="h-full bg-white" style={{ width: `${stat.val}%` }}></div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                            <button
                                onClick={handleUpload}
                                disabled={isUploading || files.length === 0 || !jobDescription}
                                className="w-full mt-12 brutalist-button text-xl py-4 bg-white hover:bg-slate-100 disabled:opacity-50 disabled:shadow-none disabled:translate-y-0"
                            >
                                {isUploading ? 'analyzing...' : 'START ANALYSIS'}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
        </div>
    )
}
