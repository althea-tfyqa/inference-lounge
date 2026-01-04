# freeze_detector.py
"""
Freeze Detector - Detects when the Qt main thread stops responding.

This utility runs a background thread that periodically checks if the main
event loop is processing events. If the main thread doesn't respond within
a timeout, it logs a warning with a stack trace of all threads.

Usage:
    from freeze_detector import FreezeDetector
    
    # In your main.py, after creating QApplication:
    freeze_detector = FreezeDetector(timeout_seconds=5)
    freeze_detector.start()
    
    # The detector will automatically log warnings when freezes are detected.
    # Check freeze_log.txt for details.

Note: This is a DEBUG tool. Disable in production as it adds overhead.
"""

import sys
import os
import threading
import traceback
import time
from datetime import datetime
from pathlib import Path

# Try to import Qt - but don't fail if not available
try:
    from PyQt6.QtCore import QTimer, QCoreApplication
    HAS_QT = True
except ImportError:
    HAS_QT = False


class FreezeDetector:
    """
    Detects main thread freezes by checking if the event loop is responsive.
    
    How it works:
    1. A background thread periodically sets a flag
    2. A QTimer in the main thread clears the flag
    3. If the flag isn't cleared within timeout, main thread is frozen
    4. On freeze, logs stack traces of all threads to freeze_log.txt
    """
    
    def __init__(self, timeout_seconds=5, check_interval=1, log_file="freeze_log.txt"):
        """
        Args:
            timeout_seconds: How long to wait before declaring a freeze
            check_interval: How often to check (seconds)
            log_file: Where to write freeze logs
        """
        self.timeout = timeout_seconds
        self.check_interval = check_interval
        self.log_file = Path(log_file)
        
        self._last_heartbeat = time.time()
        self._running = False
        self._thread = None
        self._timer = None
        
    def start(self):
        """Start the freeze detector."""
        if not HAS_QT:
            print("[FreezeDetector] Qt not available, cannot start")
            return
            
        if self._running:
            return
            
        self._running = True
        self._last_heartbeat = time.time()
        
        # Start the main thread heartbeat timer
        self._timer = QTimer()
        self._timer.timeout.connect(self._heartbeat)
        self._timer.start(int(self.check_interval * 500))  # Check at 2x rate
        
        # Start the watchdog thread
        self._thread = threading.Thread(target=self._watchdog_loop, daemon=True)
        self._thread.start()
        
        print(f"[FreezeDetector] Started (timeout={self.timeout}s, log={self.log_file})")
    
    def stop(self):
        """Stop the freeze detector."""
        self._running = False
        if self._timer:
            self._timer.stop()
            self._timer = None
    
    def _heartbeat(self):
        """Called by QTimer in the main thread - proves event loop is running."""
        self._last_heartbeat = time.time()
    
    def _watchdog_loop(self):
        """Background thread that monitors the main thread."""
        consecutive_freezes = 0
        
        while self._running:
            time.sleep(self.check_interval)
            
            if not self._running:
                break
            
            elapsed = time.time() - self._last_heartbeat
            
            if elapsed > self.timeout:
                consecutive_freezes += 1
                
                if consecutive_freezes == 1:
                    # First detection - log it
                    self._log_freeze(elapsed)
                elif consecutive_freezes % 5 == 0:
                    # Periodic reminder
                    print(f"[FreezeDetector] Still frozen ({elapsed:.1f}s)")
            else:
                if consecutive_freezes > 0:
                    print(f"[FreezeDetector] Recovered after {consecutive_freezes} checks")
                consecutive_freezes = 0
    
    def _log_freeze(self, elapsed):
        """Log freeze with stack traces of all threads."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Build the log message
        lines = [
            "",
            "=" * 70,
            f"[FREEZE DETECTED] {timestamp}",
            f"Main thread unresponsive for {elapsed:.1f} seconds",
            "=" * 70,
            "",
            "Stack traces of all threads:",
            "-" * 40,
        ]
        
        # Get stack traces for all threads
        for thread_id, frame in sys._current_frames().items():
            thread_name = "Unknown"
            for t in threading.enumerate():
                if t.ident == thread_id:
                    thread_name = t.name
                    break
            
            lines.append(f"\nThread: {thread_name} (id={thread_id})")
            lines.append("-" * 30)
            for line in traceback.format_stack(frame):
                lines.append(line.rstrip())
        
        lines.append("")
        lines.append("=" * 70)
        lines.append("")
        
        log_content = "\n".join(lines)
        
        # Print to console
        print(log_content)
        
        # Write to file
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_content)
            print(f"[FreezeDetector] Details logged to: {self.log_file}")
        except Exception as e:
            print(f"[FreezeDetector] Failed to write log: {e}")


# Also add faulthandler for segfaults
def enable_faulthandler(log_file="crash_log.txt"):
    """
    Enable Python's faulthandler to catch segfaults and write to log.
    
    Call this early in your main.py:
        from freeze_detector import enable_faulthandler
        enable_faulthandler()
    """
    import faulthandler
    
    try:
        # Open file in append mode
        log_path = Path(log_file)
        log_handle = open(log_path, "a", encoding="utf-8")
        
        # Enable faulthandler to write to both stderr and file
        faulthandler.enable(file=log_handle, all_threads=True)
        
        # Also dump stacks on SIGUSR1 (Unix only)
        if hasattr(faulthandler, 'register'):
            import signal
            faulthandler.register(signal.SIGUSR1, file=log_handle, all_threads=True)
        
        print(f"[FaultHandler] Enabled, logging to: {log_path}")
        return log_handle
        
    except Exception as e:
        print(f"[FaultHandler] Failed to enable: {e}")
        # Fall back to just stderr
        faulthandler.enable()
        return None


# =============================================================================
# Standalone test
# =============================================================================

if __name__ == "__main__":
    print("Testing FreezeDetector...")
    
    if not HAS_QT:
        print("Qt not available, cannot test")
        sys.exit(1)
    
    from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
    
    app = QApplication(sys.argv)
    
    # Enable faulthandler
    enable_faulthandler()
    
    # Start freeze detector
    detector = FreezeDetector(timeout_seconds=3)
    detector.start()
    
    # Create test window
    window = QWidget()
    window.setWindowTitle("Freeze Detector Test")
    layout = QVBoxLayout(window)
    
    def simulate_freeze():
        """Simulate a freeze by blocking the main thread."""
        print("Simulating 5-second freeze...")
        time.sleep(5)
        print("Freeze ended!")
    
    freeze_btn = QPushButton("Simulate Freeze (5s)")
    freeze_btn.clicked.connect(simulate_freeze)
    layout.addWidget(freeze_btn)
    
    quit_btn = QPushButton("Quit")
    quit_btn.clicked.connect(app.quit)
    layout.addWidget(quit_btn)
    
    window.show()
    
    print("\nClick 'Simulate Freeze' to test freeze detection.")
    print("The detector should log a warning after 3 seconds.\n")
    
    sys.exit(app.exec())