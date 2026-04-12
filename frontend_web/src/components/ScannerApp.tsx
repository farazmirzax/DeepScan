import { useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import {
  AlertTriangle,
  ArrowLeft,
  CheckCircle,
  Link,
  ScanLine,
  Shield,
  Terminal,
  Upload,
} from 'lucide-react';
import ForensicScanner from './ForensicScanner';

interface AnalysisResult {
  verdict: 'REAL' | 'FAKE' | 'ERROR';
  confidence_score: string;
  analysis: string;
}

interface ScannerAppProps {
  onBack: () => void;
}

export default function ScannerApp({ onBack }: ScannerAppProps) {
  const [activeTab, setActiveTab] = useState<'image' | 'video'>('image');
  const [url, setUrl] = useState<string>('');
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    const selectedFile = files[0];

    setPreview(URL.createObjectURL(selectedFile));
    setResult(null);
    setError(null);
    setLoading(true);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post<AnalysisResult>('http://127.0.0.1:8000/scan-image/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError("Server error. Make sure 'main.py' is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  const handleVideoScan = async () => {
    if (!url) return;

    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const response = await axios.post<AnalysisResult>('http://127.0.0.1:8000/scan-video/', { url });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError('Agent error. The video could not be fetched. Check the URL and backend service.');
    } finally {
      setLoading(false);
    }
  };

  const formatAnalysisLine = (line: string, index: number) => {
    const cleanLine = line.replace(/[^ -~]/g, '').trim();
    if (!cleanLine) return null;

    let colorClass = 'text-gray-300';
    if (cleanLine.includes('CRITICAL') || cleanLine.includes('WARNING')) {
      colorClass = 'text-red-400 font-semibold';
    } else if (cleanLine.includes('CLEAN')) {
      colorClass = 'text-green-400 font-semibold';
    } else if (cleanLine.includes('Metadata')) {
      colorClass = 'text-blue-300';
    } else if (cleanLine.includes('Geometry')) {
      colorClass = 'text-purple-300';
    } else if (cleanLine.includes('FORENSIC FLAG')) {
      colorClass = 'text-orange-400';
    }

    return (
      <motion.div
        key={index}
        initial={{ opacity: 0, x: -10 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: index * 0.15 + 0.2 }}
        className={`mb-2 flex items-start text-sm font-mono ${colorClass}`}
      >
        <span className="mr-3 mt-0.5 shrink-0 text-cyber-neon">{'>'}</span>
        <span className="leading-relaxed">{cleanLine}</span>
      </motion.div>
    );
  };

  return (
    <div className="relative min-h-screen overflow-hidden bg-cyber-black p-8 font-mono text-white">
      <div className="pointer-events-none absolute inset-0 bg-[linear-gradient(to_right,#1f1f1f_1px,transparent_1px),linear-gradient(to_bottom,#1f1f1f_1px,transparent_1px)] bg-[size:4rem_4rem] opacity-20 [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]" />

      <div className="relative z-10 mx-auto flex max-w-5xl flex-col items-center">
        <div className="mb-8 flex w-full items-center justify-between gap-4">
          <button
            onClick={onBack}
            className="inline-flex cursor-pointer items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.2em] text-white/70 transition-colors hover:bg-white/10 hover:text-white"
          >
            <ArrowLeft size={14} />
            Back To Overview
          </button>

          <div className="text-right text-[11px] uppercase tracking-[0.28em] text-cyber-neon/70">
            Secure Connection // Port 8000
          </div>
        </div>

        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="z-10 mb-12 text-center">
          <div className="mb-2 flex items-center justify-center gap-4">
            <Shield className="h-12 w-12 animate-pulse-fast text-cyber-neon" />
            <h1 className="bg-gradient-to-r from-cyber-neon via-white to-[#f5d061] bg-clip-text text-5xl font-bold tracking-widest text-transparent drop-shadow-[0_0_10px_rgba(0,243,255,0.5)]">
              DEEPSCAN
            </h1>
          </div>
          <div className="flex items-center justify-center gap-2 text-sm tracking-[0.3em] text-cyber-neon/60">
            <Terminal size={14} />
            <span>FORENSIC DETECTION WORKBENCH</span>
          </div>
        </motion.div>

        <div className="relative z-10 w-full max-w-3xl rounded-2xl border border-gray-800 bg-cyber-dark/80 p-8 shadow-2xl shadow-cyber-neon/5 backdrop-blur-md">
          <div className="mb-8 flex gap-4 rounded-xl border border-gray-800 bg-cyber-black p-2">
            <button
              onClick={() => {
                setActiveTab('image');
                setResult(null);
                setError(null);
              }}
              className={`flex flex-1 cursor-pointer items-center justify-center gap-2 rounded-lg py-3 transition-all duration-300 ${
                activeTab === 'image'
                  ? 'bg-cyber-neon font-bold text-black shadow-[0_0_15px_rgba(0,243,255,0.4)]'
                  : 'text-gray-400 hover:bg-white/5 hover:text-white'
              }`}
            >
              <Upload size={20} /> IMAGE ANALYSIS
            </button>
            <button
              onClick={() => {
                setActiveTab('video');
                setResult(null);
                setError(null);
              }}
              className={`flex flex-1 cursor-pointer items-center justify-center gap-2 rounded-lg py-3 transition-all duration-300 ${
                activeTab === 'video'
                  ? 'bg-cyber-neon font-bold text-black shadow-[0_0_15px_rgba(0,243,255,0.4)]'
                  : 'text-gray-400 hover:bg-white/5 hover:text-white'
              }`}
            >
              <Link size={20} /> VIDEO LINK AGENT
            </button>
          </div>

          {loading && <ForensicScanner imageUrl={preview} />}

          <div className="group relative flex min-h-[250px] flex-col items-center justify-center overflow-hidden rounded-xl border-2 border-dashed border-gray-700 bg-black/40 transition-colors hover:border-cyber-neon/50">
            {activeTab === 'image' ? (
              <div className="flex h-full w-full flex-col items-center justify-center p-8">
                {preview ? (
                  <div className="flex w-full flex-col items-center gap-4">
                    <div className="group relative flex w-full justify-center">
                      <img
                        src={preview}
                        alt="Upload preview"
                        className="max-h-64 rounded-lg border border-gray-600 shadow-lg transition-all group-hover:border-cyber-neon"
                      />
                      <div className="absolute bottom-4 rounded-full border border-white/10 bg-black/70 px-4 py-1 text-xs text-white backdrop-blur-md">
                        PREVIEW
                      </div>
                    </div>
                    <button
                      onClick={() => {
                        setPreview(null);
                        setResult(null);
                        setError(null);
                      }}
                      className="flex cursor-pointer items-center gap-2 rounded-lg border border-gray-600 bg-gray-800 px-6 py-2 font-bold tracking-wider text-white transition-all duration-300 hover:bg-cyber-neon hover:text-black"
                    >
                      <Upload size={16} /> UPLOAD ANOTHER IMAGE
                    </button>
                  </div>
                ) : (
                  <label className="flex cursor-pointer flex-col items-center transition-transform duration-300 group-hover:scale-105">
                    <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-cyber-gray transition-colors group-hover:bg-cyber-neon/20">
                      <Upload className="h-10 w-10 text-gray-400 group-hover:text-cyber-neon" />
                    </div>
                    <span className="text-lg font-medium text-gray-300">Click to Upload Evidence</span>
                    <span className="mt-2 text-sm text-gray-600">Supports JPG, PNG, WEBP</span>
                    <input type="file" className="hidden" accept="image/*" onChange={handleImageUpload} />
                  </label>
                )}
              </div>
            ) : (
              <div className="flex w-full flex-col gap-6 p-12">
                <div className="relative">
                  <Link className="absolute left-4 top-4 text-gray-500" />
                  <input
                    type="text"
                    placeholder="Paste YouTube / Instagram / TikTok link..."
                    className="w-full rounded-xl border border-gray-700 bg-cyber-black py-4 pl-12 pr-4 text-white transition-all placeholder:text-gray-600 focus:border-cyber-neon focus:outline-none focus:ring-1 focus:ring-cyber-neon"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                  />
                </div>
                <button
                  onClick={handleVideoScan}
                  disabled={!url}
                  className="flex w-full cursor-pointer items-center justify-center gap-3 rounded-xl border border-gray-600 bg-cyber-gray py-4 font-bold tracking-wider text-white shadow-lg transition-all duration-300 hover:bg-cyber-neon hover:text-black disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <ScanLine size={20} /> INITIALIZE AGENT SCAN
                </button>
              </div>
            )}
          </div>

          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mt-6 flex items-center gap-3 rounded-xl border border-red-500/50 bg-red-900/20 p-4 text-red-400"
              >
                <AlertTriangle className="shrink-0" />
                <span className="text-sm font-mono">{error}</span>
              </motion.div>
            )}
          </AnimatePresence>

          <AnimatePresence>
            {result && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className={`mt-8 overflow-hidden rounded-2xl border-2 ${
                  result.verdict === 'FAKE'
                    ? 'border-cyber-danger bg-red-950/30 shadow-[0_0_30px_rgba(255,0,60,0.2)]'
                    : 'border-cyber-safe bg-green-950/30 shadow-[0_0_30px_rgba(0,255,159,0.2)]'
                }`}
              >
                <div
                  className={`flex items-center justify-between p-6 ${
                    result.verdict === 'FAKE' ? 'bg-cyber-danger/10' : 'bg-cyber-safe/10'
                  }`}
                >
                  <div className="flex items-center gap-4">
                    {result.verdict === 'FAKE' ? (
                      <AlertTriangle className="h-10 w-10 text-cyber-danger" />
                    ) : (
                      <CheckCircle className="h-10 w-10 text-cyber-safe" />
                    )}
                    <div>
                      <h2
                        className={`text-3xl font-bold tracking-tighter ${
                          result.verdict === 'FAKE' ? 'text-cyber-danger' : 'text-cyber-safe'
                        }`}
                      >
                        {result.verdict === 'FAKE' ? 'DETECTED: DEEPFAKE' : 'VERIFIED: REAL'}
                      </h2>
                      <p className="text-xs uppercase tracking-widest text-white/60">Forensic Analysis Complete</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="mb-1 text-sm text-white/50">CONFIDENCE SCORE</div>
                    <div
                      className={`text-4xl font-bold font-mono ${
                        result.verdict === 'FAKE' ? 'text-cyber-danger' : 'text-cyber-safe'
                      }`}
                    >
                      {result.confidence_score}
                    </div>
                  </div>
                </div>

                <div className="border-t border-white/5 bg-black/60 p-6">
                  <div className="mb-4 flex gap-2 border-b border-white/10 pb-2 text-xs font-bold uppercase tracking-widest text-cyber-neon/80">
                    <Terminal size={14} /> FORENSIC DIAGNOSTICS LOG
                  </div>

                  <div className="flex flex-col">
                    {result.analysis.split('\n').map((line, idx) => formatAnalysisLine(line, idx))}
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
