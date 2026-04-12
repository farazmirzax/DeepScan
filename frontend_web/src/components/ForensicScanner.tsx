import { useEffect, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { CheckCircle2, Terminal } from 'lucide-react';

const SCAN_STEPS = [
  { id: 0, label: 'INITIALIZING PRISM ENGINE', duration: 1200, color: '#00f3ff' },
  { id: 1, label: 'VIGILANTE-V2: FACE SWAP SCAN', duration: 1800, color: '#facc15' },
  { id: 2, label: 'SENTINEL-X: AI GENERATION SCAN', duration: 1800, color: '#c084fc' },
  { id: 3, label: 'PRISM: METADATA EXTRACTION', duration: 1000, color: '#93c5fd' },
  { id: 4, label: 'PRISM: ERROR LEVEL ANALYSIS', duration: 1200, color: '#fb923c' },
  { id: 5, label: 'PRISM: FACE GEOMETRY MAPPING', duration: 1000, color: '#f472b6' },
  { id: 6, label: 'COMPILING FORENSIC VERDICT', duration: 800, color: '#00f3ff' },
];

interface ForensicScannerProps {
  imageUrl: string | null;
  mode?: 'image' | 'video';
  videoUrl?: string;
}

export default function ForensicScanner({ imageUrl, mode = 'image', videoUrl }: ForensicScannerProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [completedSteps, setCompletedSteps] = useState<number[]>([]);
  const [progressPercent, setProgressPercent] = useState(0);

  useEffect(() => {
    if (currentStep >= SCAN_STEPS.length) return;

    const step = SCAN_STEPS[currentStep];
    const timer = setTimeout(() => {
      setCompletedSteps((prev) => [...prev, currentStep]);
      setCurrentStep((prev) => prev + 1);
    }, step.duration);

    return () => clearTimeout(timer);
  }, [currentStep]);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgressPercent((prev) => {
        const target = ((completedSteps.length + 0.5) / SCAN_STEPS.length) * 100;
        if (prev >= 95) return 95;
        return Math.min(prev + 0.8, target);
      });
    }, 50);

    return () => clearInterval(interval);
  }, [completedSteps]);

  const activeStep = currentStep < SCAN_STEPS.length ? SCAN_STEPS[currentStep] : null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center overflow-hidden bg-black">
      <div className="absolute inset-0 opacity-[0.03]">
        <div className="absolute inset-0 bg-[linear-gradient(0deg,transparent_24%,rgba(0,243,255,0.08)_25%,rgba(0,243,255,0.08)_26%,transparent_27%,transparent_74%,rgba(0,243,255,0.08)_75%,rgba(0,243,255,0.08)_76%,transparent_77%)] bg-[length:60px_60px]" />
        <div className="absolute inset-0 bg-[linear-gradient(90deg,transparent_24%,rgba(0,243,255,0.08)_25%,rgba(0,243,255,0.08)_26%,transparent_27%,transparent_74%,rgba(0,243,255,0.08)_75%,rgba(0,243,255,0.08)_76%,transparent_77%)] bg-[length:60px_60px]" />
      </div>

      <div className="relative z-10 flex w-full max-w-5xl flex-col items-center gap-8 px-6 lg:flex-row lg:gap-12">
        <div className="relative shrink-0">
          <div className="relative h-72 w-72 sm:h-80 sm:w-80">
            {mode === 'image' && imageUrl && (
              <img
                src={imageUrl}
                alt="Scanning"
                className="h-full w-full rounded-lg object-cover"
                style={{ filter: 'grayscale(30%) contrast(1.1)' }}
              />
            )}
            {mode === 'video' && (
              <div className="flex h-full w-full flex-col items-center justify-center rounded-lg border-2 border-cyber-neon/50 bg-cyber-black/80 p-6">
                <div className="mb-4 text-cyan-400">
                  <svg className="h-16 w-16 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <p className="font-mono text-xs tracking-wider text-gray-400">VIDEO STREAM</p>
                <p className="mt-2 break-all text-center font-mono text-[10px] text-cyan-400/60">{videoUrl}</p>
              </div>
            )}

            <motion.div
              className="absolute left-0 right-0 z-20 h-1"
              style={{
                background: 'linear-gradient(180deg, transparent, rgba(0,243,255,0.8), rgba(0,243,255,0.3), transparent)',
                boxShadow: '0 0 30px 10px rgba(0,243,255,0.3)',
              }}
              animate={{ top: ['-4px', '100%'] }}
              transition={{ duration: 2.2, repeat: Infinity, ease: 'linear' }}
            />

            <div className="absolute left-0 top-0 z-10 h-8 w-8 border-l-2 border-t-2 border-cyber-neon" />
            <div className="absolute right-0 top-0 z-10 h-8 w-8 border-r-2 border-t-2 border-cyber-neon" />
            <div className="absolute bottom-0 left-0 z-10 h-8 w-8 border-b-2 border-l-2 border-cyber-neon" />
            <div className="absolute bottom-0 right-0 z-10 h-8 w-8 border-b-2 border-r-2 border-cyber-neon" />

            <motion.div
              className="pointer-events-none absolute inset-0 z-10 rounded-lg border-2 border-cyber-neon/50"
              animate={{
                borderColor: ['rgba(0,243,255,0.3)', 'rgba(0,243,255,0.7)', 'rgba(0,243,255,0.3)'],
                boxShadow: [
                  '0 0 10px rgba(0,243,255,0.1)',
                  '0 0 25px rgba(0,243,255,0.3)',
                  '0 0 10px rgba(0,243,255,0.1)',
                ],
              }}
              transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
            />

            <motion.div
              className="pointer-events-none absolute inset-0 z-[5] rounded-lg bg-black/40"
              animate={{ opacity: [0.5, 0.2, 0.5] }}
              transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
            />

            {activeStep && (
              <motion.div
                key={activeStep.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="absolute bottom-3 left-3 right-3 z-30 rounded-md border border-gray-700 bg-black/80 px-3 py-2 backdrop-blur-sm"
              >
                <div className="flex items-center gap-2">
                  <motion.div
                    className="h-2 w-2 shrink-0 rounded-full"
                    style={{ backgroundColor: activeStep.color }}
                    animate={{ opacity: [1, 0.3, 1] }}
                    transition={{ duration: 0.6, repeat: Infinity }}
                  />
                  <span className="font-mono text-[11px] tracking-wider" style={{ color: activeStep.color }}>
                    {activeStep.label}
                  </span>
                </div>
              </motion.div>
            )}
          </div>

          <div className="mt-3 text-center">
            <span className="font-mono text-[10px] tracking-[0.3em] text-gray-600">
              {mode === 'image' ? 'SUBJECT // IMAGE-001' : 'SUBJECT // VIDEO-ANALYSIS'}
            </span>
          </div>
        </div>

        <div className="w-full max-w-sm flex-1">
          <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="mb-5">
            <h3 className="mb-1 font-mono text-lg font-bold tracking-[0.2em] text-cyber-neon">DEEP FORENSIC SCAN</h3>
            <p className="font-mono text-[11px] tracking-widest text-gray-600">MULTI-LAYER ANALYSIS IN PROGRESS</p>
          </motion.div>

          <div className="mb-5 h-1.5 w-full overflow-hidden rounded-full border border-gray-800 bg-gray-900">
            <motion.div
              className="h-full rounded-full"
              style={{
                width: `${progressPercent}%`,
                background: 'linear-gradient(90deg, #00f3ff, #a855f7, #00f3ff)',
              }}
              transition={{ duration: 0.3 }}
            />
          </div>

          <div className="mb-5 space-y-1">
            {SCAN_STEPS.map((step) => {
              const isCompleted = completedSteps.includes(step.id);
              const isActive = currentStep === step.id;
              const isPending = !isCompleted && !isActive;

              return (
                <motion.div
                  key={step.id}
                  initial={{ opacity: 0, x: 15 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: step.id * 0.06 }}
                  className={`flex items-center gap-2.5 rounded px-2 py-1 font-mono transition-all duration-300 ${
                    isActive ? 'bg-white/[0.03]' : ''
                  } ${isPending ? 'opacity-25' : ''}`}
                >
                  <div className="flex h-4 w-4 shrink-0 items-center justify-center">
                    {isCompleted ? (
                      <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: 'spring', stiffness: 400 }}>
                        <CheckCircle2 size={13} className="text-cyber-safe" />
                      </motion.div>
                    ) : isActive ? (
                      <motion.div
                        className="h-2 w-2 rounded-full"
                        style={{ backgroundColor: step.color }}
                        animate={{ opacity: [1, 0.2, 1], scale: [1, 1.3, 1] }}
                        transition={{ duration: 0.8, repeat: Infinity }}
                      />
                    ) : (
                      <div className="h-1.5 w-1.5 rounded-full bg-gray-700" />
                    )}
                  </div>

                  <span
                    className={`text-[11px] tracking-wider ${
                      isCompleted ? 'text-gray-500 line-through' : isActive ? 'font-semibold' : 'text-gray-700'
                    }`}
                    style={isActive ? { color: step.color } : {}}
                  >
                    {step.label}
                  </span>

                  {isActive && (
                    <motion.span
                      className="ml-auto text-[10px]"
                      style={{ color: step.color }}
                      animate={{ opacity: [0, 1, 0] }}
                      transition={{ duration: 1, repeat: Infinity }}
                    >
                      ...
                    </motion.span>
                  )}
                </motion.div>
              );
            })}
          </div>

          <div className="rounded-lg border border-gray-800/50 bg-black/60 p-3">
            <div className="mb-2 flex items-center gap-1.5 font-mono text-[9px] uppercase tracking-widest text-gray-600">
              <Terminal size={9} /> Live Output
            </div>
            <div className="space-y-0.5">
              <AnimatePresence>
                {completedSteps.map((stepId) => (
                  <motion.div
                    key={`done-${stepId}`}
                    initial={{ opacity: 0, x: -5 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="font-mono text-[10px] text-gray-600"
                  >
                    <span className="text-cyber-safe/60">[ok]</span> {SCAN_STEPS[stepId].label}
                  </motion.div>
                ))}
              </AnimatePresence>
              {activeStep && (
                <motion.div
                  key={`active-${activeStep.id}`}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="font-mono text-[10px]"
                  style={{ color: activeStep.color }}
                >
                  {'>'} {activeStep.label}...
                </motion.div>
              )}
            </div>
            <motion.span
              animate={{ opacity: [1, 0] }}
              transition={{ duration: 0.5, repeat: Infinity }}
              className="font-mono text-[10px] text-cyber-neon"
            >
              _
            </motion.span>
          </div>
        </div>
      </div>
    </div>
  );
}
