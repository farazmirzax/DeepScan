import { motion } from 'framer-motion';
import {
  ArrowRight,
  BadgeCheck,
  BrainCircuit,
  Clapperboard,
  Eye,
  Radar,
  ShieldCheck,
  Sparkles,
  Upload,
  Zap,
  CheckCircle2,
} from 'lucide-react';

interface LandingPageProps {
  onLaunch: () => void;
}

const capabilities = [
  {
    icon: BrainCircuit,
    title: 'Vigilante-V2: Swap Hunter',
    description: 'Specialized Vision Transformer that detects face swaps and traditional deepfakes with 92% accuracy.',
  },
  {
    icon: Eye,
    title: 'Sentinel-X: GenAI Hunter',
    description: 'Identifies AI-generated faces, GANs, and synthetic content with deep learning analysis.',
  },
  {
    icon: Radar,
    title: 'Prism: Digital Forensics',
    description: 'Inspects metadata, pixel compression anomalies, and facial geometry to find editing traces.',
  },
];

const stats = [
  { value: 'Triple-Agent', label: 'Three specialized detection systems' },
  { value: 'AI + Forensics', label: 'Machine learning meets digital forensics' },
  { value: '100% Explainable', label: 'Every verdict backed by evidence logs' },
];

const workflow = [
  {
    icon: Upload,
    title: 'Upload Media',
    description: 'Submit an image or video URL for analysis. Supports JPG, PNG, WEBP, and YouTube links.',
    details: 'Fast processing with no data storage',
    color: 'from-[#ff7b54] to-[#ff9f71]',
    iconBg: 'bg-[#ff7b54]/20 text-[#ff7b54]',
  },
  {
    icon: Zap,
    title: 'Run Triple-Agent Pipeline',
    description: 'DeepScan simultaneously queries Vigilante-V2, Sentinel-X, and Prism forensics.',
    details: '3-5 seconds for images, 10-20 seconds for videos',
    color: 'from-[#6ee7ff] to-[#8ed9ff]',
    iconBg: 'bg-[#6ee7ff]/20 text-[#6ee7ff]',
  },
  {
    icon: CheckCircle2,
    title: 'Get Explainable Verdict',
    description: 'Receive a detailed verdict with AI confidence scores and forensic evidence logs.',
    details: 'Understand why, not just what',
    color: 'from-[#f5d061] to-[#ffe28d]',
    iconBg: 'bg-[#f5d061]/20 text-[#f5d061]',
  },
];

export default function LandingPage({ onLaunch }: LandingPageProps) {
  return (
    <div className="relative min-h-screen overflow-hidden bg-[radial-gradient(circle_at_top_left,_rgba(255,255,255,0.08),_transparent_30%),linear-gradient(145deg,_#07111f_0%,_#102236_42%,_#05070b_100%)] text-white">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(120,169,255,0.08)_1px,transparent_1px),linear-gradient(to_bottom,rgba(120,169,255,0.08)_1px,transparent_1px)] bg-[size:72px_72px] opacity-40" />
      <div className="absolute left-[-10%] top-10 h-72 w-72 rounded-full bg-[#ff7b54]/20 blur-3xl" />
      <div className="absolute right-[-5%] top-1/4 h-96 w-96 rounded-full bg-[#6ee7ff]/18 blur-3xl" />
      <div className="absolute bottom-[-10%] left-1/3 h-96 w-96 rounded-full bg-[#f5d061]/15 blur-3xl" />

      <div className="relative z-10 mx-auto flex min-h-screen max-w-7xl flex-col px-6 py-8 lg:px-10">
        <header className="flex flex-col gap-4 border-b border-white/10 pb-6 md:flex-row md:items-center md:justify-between">
          <div>
            <div className="mb-2 flex items-center gap-3 text-sm uppercase tracking-[0.35em] text-[#8ed9ff]">
              <ShieldCheck className="h-4 w-4" />
              DeepScan Forensics
            </div>
            <h1 className="font-display text-3xl font-semibold tracking-tight text-white md:text-4xl">
              Detect deepfakes and AI-generated media with confidence.
            </h1>
          </div>

          <div className="flex items-center gap-3 self-start rounded-full border border-white/12 bg-white/6 px-4 py-2 text-sm text-white/70 backdrop-blur">
            <BadgeCheck className="h-4 w-4 text-[#f5d061]" />
            AI models + digital forensics in one platform
          </div>
        </header>

        <main className="grid flex-1 gap-10 py-10 lg:grid-cols-[1.2fr_0.8fr] lg:items-center">
          <section className="space-y-8">
            <motion.div
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="space-y-6"
            >
              <div className="inline-flex items-center gap-2 rounded-full border border-[#8ed9ff]/30 bg-[#0b1b2d]/70 px-4 py-2 text-sm text-[#cdefff] backdrop-blur">
                <Sparkles className="h-4 w-4 text-[#f5d061]" />
                Professional-grade deepfake detection system
              </div>

              <div className="space-y-4">
                <h2 className="max-w-4xl font-display text-5xl font-semibold leading-none tracking-tight text-white md:text-7xl">
                  Analyze images and videos for deepfakes using AI and forensics.
                </h2>
                <p className="max-w-2xl text-lg leading-8 text-slate-200/82 md:text-xl">
                  DeepScan combines two specialized Vision Transformers with a forensic analysis engine to detect face swaps, 
                  synthetic media, and edited content. Every verdict is backed by explainable evidence.
                </p>
              </div>

              <div className="flex flex-col gap-4 sm:flex-row">
                <button
                  onClick={onLaunch}
                  className="group inline-flex cursor-pointer items-center justify-center gap-3 rounded-full bg-[#f5d061] px-7 py-4 font-semibold text-slate-950 transition-all duration-300 hover:translate-y-[-2px] hover:bg-[#ffe28d] hover:shadow-[0_18px_50px_rgba(245,208,97,0.28)]"
                >
                  Launch Scanner
                  <ArrowRight className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
                </button>

                <a
                  href="#overview"
                  className="inline-flex items-center justify-center gap-3 rounded-full border border-white/15 bg-white/6 px-7 py-4 font-semibold text-white transition-colors duration-300 hover:bg-white/12"
                >
                  Explore Overview
                  <Radar className="h-4 w-4 text-[#8ed9ff]" />
                </a>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 24 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.65, delay: 0.12 }}
              className="grid gap-4 md:grid-cols-3"
            >
              {stats.map((stat) => (
                <div
                  key={stat.label}
                  className="rounded-[1.75rem] border border-white/10 bg-white/7 p-5 shadow-[0_18px_60px_rgba(0,0,0,0.18)] backdrop-blur"
                >
                  <div className="mb-2 font-display text-3xl text-[#f5d061]">{stat.value}</div>
                  <p className="text-sm leading-6 text-white/74">{stat.label}</p>
                </div>
              ))}
            </motion.div>
          </section>

          <motion.aside
            initial={{ opacity: 0, x: 28 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7, delay: 0.18 }}
            className="rounded-[2rem] border border-white/12 bg-[linear-gradient(180deg,rgba(255,255,255,0.12),rgba(255,255,255,0.04))] p-6 shadow-[0_30px_100px_rgba(0,0,0,0.35)] backdrop-blur-xl"
          >
            <div className="mb-6 flex items-center justify-between">
              <div>
                <div className="text-xs uppercase tracking-[0.3em] text-[#8ed9ff]">Detection Agents</div>
                <div className="mt-2 font-display text-2xl text-white">Your forensic team</div>
              </div>
              <div className="rounded-2xl bg-[#f5d061]/16 p-3 text-[#f5d061]">
                <ShieldCheck className="h-6 w-6" />
              </div>
            </div>

            <div className="space-y-4">
              {capabilities.map(({ icon: Icon, title, description }) => (
                <div key={title} className="rounded-[1.5rem] border border-white/10 bg-slate-950/35 p-4">
                  <div className="mb-3 flex items-center gap-3">
                    <div className="rounded-2xl bg-[#8ed9ff]/14 p-3 text-[#8ed9ff]">
                      <Icon className="h-5 w-5" />
                    </div>
                    <h3 className="font-display text-xl text-white">{title}</h3>
                  </div>
                  <p className="text-sm leading-6 text-white/70">{description}</p>
                </div>
              ))}
            </div>
          </motion.aside>
        </main>

        <section id="overview" className="grid gap-6 border-t border-white/10 py-10 lg:grid-cols-[0.9fr_1.1fr]">
          <div className="space-y-4">
            <div className="text-sm uppercase tracking-[0.35em] text-[#8ed9ff]">How It Works</div>
            <h2 className="font-display text-4xl font-semibold text-white md:text-5xl">
              Three detection agents working together.
            </h2>
            <p className="max-w-xl text-base leading-7 text-white/72">
              DeepScan processes media through AI models for detection, then adds forensic analysis for verification. 
              The result is a verdict grounded in both machine learning and digital evidence.
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-3">
            {workflow.map(({ icon: Icon, title, description, details, color, iconBg }, index) => (
              <motion.div
                key={title}
                initial={{ opacity: 0, y: 24 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.15 * index }}
                whileHover={{ y: -4 }}
                className="group relative"
              >
                {/* Gradient border background */}
                <div className={`absolute inset-0 bg-gradient-to-br ${color} rounded-[1.5rem] opacity-0 group-hover:opacity-20 blur transition-opacity duration-300`} />
                
                {/* Card container */}
                <div className="relative rounded-[1.5rem] border border-white/10 bg-slate-950/40 backdrop-blur transition-all duration-300 group-hover:border-white/20 group-hover:bg-slate-950/60 p-6 h-full flex flex-col">
                  {/* Step indicator + Icon */}
                  <div className="mb-4 flex items-start justify-between">
                    <div className={`inline-flex h-12 w-12 items-center justify-center rounded-xl ${iconBg} transition-transform duration-300 group-hover:scale-110`}>
                      <Icon className="h-6 w-6" />
                    </div>
                    <div className={`text-xs font-bold tracking-[0.2em] bg-gradient-to-r ${color} bg-clip-text text-transparent`}>
                      STEP {index + 1}
                    </div>
                  </div>

                  {/* Title */}
                  <h3 className="font-display text-xl font-semibold text-white mb-2 leading-tight">
                    {title}
                  </h3>

                  {/* Description */}
                  <p className="text-sm leading-6 text-white/75 mb-4 flex-grow">
                    {description}
                  </p>

                  {/* Details */}
                  <div className={`inline-flex items-center gap-2 text-xs font-medium bg-gradient-to-r ${color} bg-clip-text text-transparent`}>
                    <div className={`h-1 w-1 rounded-full bg-gradient-to-r ${color}`} />
                    {details}
                  </div>


                </div>
              </motion.div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
