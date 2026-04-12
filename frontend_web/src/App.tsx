import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import LandingPage from './components/LandingPage';
import ScannerApp from './components/ScannerApp';

function App() {
  const [view, setView] = useState<'landing' | 'scanner'>('landing');

  return (
    <AnimatePresence mode="wait">
      {view === 'landing' ? (
        <motion.div
          key="landing"
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -24 }}
          transition={{ duration: 0.45, ease: 'easeOut' }}
        >
          <LandingPage onLaunch={() => setView('scanner')} />
        </motion.div>
      ) : (
        <motion.div
          key="scanner"
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -24 }}
          transition={{ duration: 0.45, ease: 'easeOut' }}
        >
          <ScannerApp onBack={() => setView('landing')} />
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export default App;
