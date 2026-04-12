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
} from 'lucide-react';

interface LandingPageProps {
  onLaunch: () => void;
}

const capabilities = [
  {
    icon: Eye,
    title: 'Visual Forensics',
    description: 'Inspect image artifacts, face geometry shifts, and subtle generation signatures in one streamlined workflow.',
  },
  {
    icon: Clapperboard,
    title: 'Video Link Intake',
    description: 'Pass a public video URL into the pipeline and let the app collect frames for investigation.',
  },
  {
    icon: BrainCircuit,
    title: 'Model-Assisted Verdicts',
    description: 'Blend detector confidence with readable diagnostics so the result feels explainable, not mysterious.',
  },
];

const stats = [
  { value: '2 modes', label: 'Image upload and video URL analysis' },
  { value: 'Live scan', label: 'Animated forensic pipeline feedback' },
  { value: 'Readable logs', label: 'Evidence-style result breakdown' },
];

const workflow = [
  'Upload an image or paste a supported video link.',
  'Run the forensic pipeline and watch the scan stages unfold.',
  'Review the verdict, confidence score, and diagnostic evidence log.',
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
              A sharper front door for your deepfake detection system.
            </h1>
          </div>

          <div className="flex items-center gap-3 self-start rounded-full border border-white/12 bg-white/6 px-4 py-2 text-sm text-white/70 backdrop-blur">
            <BadgeCheck className="h-4 w-4 text-[#f5d061]" />
            Built to explain what the application does before analysis begins
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
                Detect manipulated media with a more confident user journey
              </div>

              <div className="space-y-4">
                <h2 className="max-w-4xl font-display text-5xl font-semibold leading-none tracking-tight text-white md:text-7xl">
                  Investigate images and videos with a landing page that builds trust first.
                </h2>
                <p className="max-w-2xl text-lg leading-8 text-slate-200/82 md:text-xl">
                  Instead of dropping visitors directly into the scanner, this page frames the mission, highlights capabilities,
                  and guides them into the actual analysis experience with more clarity and impact.
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
                <div className="text-xs uppercase tracking-[0.3em] text-[#8ed9ff]">Mission Snapshot</div>
                <div className="mt-2 font-display text-2xl text-white">What this application delivers</div>
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
            <div className="text-sm uppercase tracking-[0.35em] text-[#8ed9ff]">Application Story</div>
            <h2 className="font-display text-4xl font-semibold text-white md:text-5xl">
              Explain the workflow before people commit to the tool.
            </h2>
            <p className="max-w-xl text-base leading-7 text-white/72">
              This landing page sets the context: what DeepScan checks, how the analysis runs, and why the verdict feels grounded
              in evidence rather than just a black-box label.
            </p>
          </div>

          <div className="grid gap-4 md:grid-cols-3">
            {workflow.map((step, index) => (
              <motion.div
                key={step}
                initial={{ opacity: 0, y: 24 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.15 * index }}
                className="rounded-[1.5rem] border border-white/10 bg-white/6 p-5 backdrop-blur"
              >
                <div className="mb-4 inline-flex h-10 w-10 items-center justify-center rounded-full bg-[#ff7b54] font-display text-lg font-semibold text-slate-950">
                  {index + 1}
                </div>
                <p className="text-sm leading-6 text-white/78">{step}</p>
              </motion.div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
