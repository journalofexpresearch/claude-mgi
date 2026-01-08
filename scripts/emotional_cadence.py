#!/usr/bin/env python3
"""
Emotional Cadence Analysis - Track emotional arcs through mathematical patterns
Analyzes intensity changes, tension/resolution, and dynamic patterns
"""

import librosa
import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path
from scipy import signal
import warnings
warnings.filterwarnings('ignore')

def analyze_emotional_cadence(audio_path, output_dir="emotional_analysis"):
    """
    Analyze emotional progression through intensity and harmonic patterns
    
    Args:
        audio_path: Path to audio file
        output_dir: Directory to save outputs
    
    Returns:
        dict: Emotional cadence analysis with tension/resolution markers
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Load audio
    y, sr = librosa.load(audio_path, sr=None)
    duration = len(y) / sr
    
    print(f"Analyzing emotional cadence: {audio_path}")
    
    # 1. INTENSITY TRACKING
    # RMS energy (overall loudness/intensity)
    rms = librosa.feature.rms(y=y, hop_length=512)[0]
    rms_times = librosa.times_like(rms, sr=sr, hop_length=512)
    
    # Smooth intensity for macro trends
    window_size = max(3, len(rms) // 100)
    if window_size % 2 == 0:
        window_size += 1
    intensity_smooth = signal.savgol_filter(rms, window_size, 2)
    
    # Calculate intensity gradient (rate of change)
    intensity_gradient = np.gradient(intensity_smooth)
    
    # 2. TENSION DETECTION (Dissonance)
    # Use harmonic-percussive separation
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    
    # Chromagram for harmonic analysis
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=512)
    
    # Calculate dissonance over time
    tension_timeline = []
    for frame in range(chroma.shape[1]):
        # Variance in pitch classes indicates dissonance/tension
        variance = np.var(chroma[:, frame])
        # Spread of energy across frequencies
        spread = np.std(chroma[:, frame])
        # Combined tension metric
        tension = variance * spread
        tension_timeline.append(tension)
    
    tension_timeline = np.array(tension_timeline)
    tension_times = librosa.times_like(tension_timeline, sr=sr, hop_length=512)
    
    # Normalize tension
    tension_normalized = (tension_timeline - tension_timeline.min()) / (tension_timeline.max() - tension_timeline.min() + 1e-10)
    
    # 3. CONSONANCE/RESOLUTION DETECTION
    # Lower tension = more resolution/consonance
    consonance_timeline = 1 - tension_normalized
    
    # 4. SPECTRAL FLUX (Measure of change in spectrum)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512)
    onset_times = librosa.times_like(onset_env, sr=sr, hop_length=512)
    
    # 5. EMOTIONAL PEAKS AND VALLEYS
    # Find significant intensity peaks (climaxes)
    from scipy.signal import find_peaks
    
    peaks, peak_properties = find_peaks(intensity_smooth, height=np.percentile(intensity_smooth, 75), distance=sr//512)
    peak_times = rms_times[peaks]
    peak_intensities = intensity_smooth[peaks]
    
    # Find valleys (calm moments)
    valleys, valley_properties = find_peaks(-intensity_smooth, height=-np.percentile(intensity_smooth, 25), distance=sr//512)
    valley_times = rms_times[valleys]
    valley_intensities = intensity_smooth[valleys]
    
    # 6. TENSION/RESOLUTION TRANSITIONS
    # Find moments of major tension release
    tension_drops = []
    for i in range(1, len(tension_normalized)):
        if tension_normalized[i-1] - tension_normalized[i] > 0.15:  # Significant drop
            tension_drops.append({
                "time": float(tension_times[i]),
                "magnitude": float(tension_normalized[i-1] - tension_normalized[i])
            })
    
    # Find moments of tension buildup
    tension_rises = []
    for i in range(1, len(tension_normalized)):
        if tension_normalized[i] - tension_normalized[i-1] > 0.15:  # Significant rise
            tension_rises.append({
                "time": float(tension_times[i]),
                "magnitude": float(tension_normalized[i] - tension_normalized[i-1])
            })
    
    # 7. EMOTIONAL ARC CLASSIFICATION
    # Overall trajectory
    early_intensity = np.mean(intensity_smooth[:len(intensity_smooth)//3])
    mid_intensity = np.mean(intensity_smooth[len(intensity_smooth)//3:2*len(intensity_smooth)//3])
    late_intensity = np.mean(intensity_smooth[2*len(intensity_smooth)//3:])
    
    arc_type = classify_emotional_arc(early_intensity, mid_intensity, late_intensity)
    
    # 8. CREATE VISUALIZATION
    fig, axes = plt.subplots(4, 1, figsize=(14, 12))
    
    # Intensity over time
    axes[0].plot(rms_times, rms, alpha=0.3, label='Raw Intensity', color='gray')
    axes[0].plot(rms_times, intensity_smooth, label='Smoothed Intensity', color='blue', linewidth=2)
    axes[0].scatter(peak_times, peak_intensities, color='red', s=100, zorder=5, label='Peaks', marker='^')
    axes[0].scatter(valley_times, valley_intensities, color='green', s=100, zorder=5, label='Valleys', marker='v')
    axes[0].set_title('Intensity Timeline (Emotional Energy)')
    axes[0].set_ylabel('Intensity')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Tension/Consonance over time
    axes[1].fill_between(tension_times, 0, tension_normalized, alpha=0.5, color='red', label='Tension')
    axes[1].fill_between(tension_times, 0, consonance_timeline, alpha=0.5, color='green', label='Consonance')
    axes[1].set_title('Tension vs Consonance (Harmonic Stability)')
    axes[1].set_ylabel('Level (0-1)')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    # Rate of change (emotional dynamics)
    axes[2].plot(rms_times, intensity_gradient, color='purple', linewidth=1.5)
    axes[2].axhline(y=0, color='black', linestyle='--', alpha=0.3)
    axes[2].set_title('Intensity Gradient (Rate of Emotional Change)')
    axes[2].set_ylabel('Gradient')
    axes[2].grid(True, alpha=0.3)
    
    # Spectral flux (musical change/movement)
    axes[3].plot(onset_times, onset_env, color='orange', linewidth=1.5)
    axes[3].set_title('Spectral Flux (Musical Change/Activity)')
    axes[3].set_xlabel('Time (s)')
    axes[3].set_ylabel('Onset Strength')
    axes[3].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    plot_path = output_path / "emotional_cadence.png"
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    print(f"Saved emotional cadence plot: {plot_path}")
    plt.close()
    
    # 9. COMPILE RESULTS
    results = {
        "file": str(audio_path),
        "duration_seconds": float(duration),
        "emotional_arc": {
            "type": arc_type,
            "early_intensity": float(early_intensity),
            "mid_intensity": float(mid_intensity),
            "late_intensity": float(late_intensity)
        },
        "intensity_metrics": {
            "mean": float(np.mean(intensity_smooth)),
            "max": float(np.max(intensity_smooth)),
            "min": float(np.min(intensity_smooth)),
            "dynamic_range": float(np.max(intensity_smooth) - np.min(intensity_smooth)),
            "variance": float(np.var(intensity_smooth))
        },
        "tension_metrics": {
            "mean_tension": float(np.mean(tension_normalized)),
            "max_tension": float(np.max(tension_normalized)),
            "mean_consonance": float(np.mean(consonance_timeline))
        },
        "emotional_moments": {
            "peaks": [{"time": float(t), "intensity": float(i)} for t, i in zip(peak_times, peak_intensities)],
            "valleys": [{"time": float(t), "intensity": float(i)} for t, i in zip(valley_times, valley_intensities)],
            "tension_releases": tension_drops[:10],  # Top 10
            "tension_buildups": tension_rises[:10]    # Top 10
        },
        "output_files": {
            "visualization": str(plot_path)
        }
    }
    
    # Save JSON report
    json_path = output_path / "emotional_report.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Saved emotional analysis: {json_path}")
    
    return results

def classify_emotional_arc(early, mid, late):
    """
    Classify the overall emotional trajectory of the track
    """
    threshold = 0.1  # 10% difference threshold
    
    if late > mid * (1 + threshold) and mid > early * (1 + threshold):
        return "Building/Crescendo (rises throughout)"
    elif late < mid * (1 - threshold) and mid < early * (1 - threshold):
        return "Declining/Decrescendo (falls throughout)"
    elif mid > early * (1 + threshold) and mid > late * (1 + threshold):
        return "Peak/Climax (peaks in middle)"
    elif early > mid * (1 + threshold) and late > mid * (1 + threshold):
        return "Valley/Dip (drops in middle)"
    elif abs(early - late) < threshold * early:
        return "Cyclical/Stable (consistent intensity)"
    else:
        return "Complex/Variable (mixed patterns)"

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python emotional_cadence.py <audio_file> [output_dir]")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "emotional_analysis"
    
    analyze_emotional_cadence(audio_file, output_dir)
