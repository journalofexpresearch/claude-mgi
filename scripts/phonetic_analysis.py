#!/usr/bin/env python3
"""
Phonetic Pattern Analysis - Detect emotional vocal characteristics
Identifies plosives, sibilants, fricatives, and other phonetic patterns
"""

import librosa
import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path
import speech_recognition as sr
from pydub import AudioSegment
import warnings
warnings.filterwarnings('ignore')

def analyze_phonetic_patterns(audio_path, output_dir="phonetic_analysis"):
    """
    Analyze phonetic characteristics for emotional content
    
    Args:
        audio_path: Path to audio file
        output_dir: Directory for outputs
    
    Returns:
        dict: Phonetic pattern analysis
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Load audio
    y, sr = librosa.load(audio_path, sr=None)
    duration = len(y) / sr
    
    print(f"Analyzing phonetic patterns: {audio_path}")
    
    # 1. HIGH FREQUENCY ENERGY (Sibilants: s, sh, z, ch)
    # Sibilants are characterized by high-frequency noise
    D = librosa.stft(y)
    magnitude = np.abs(D)
    
    # Focus on high frequencies (4kHz-10kHz where sibilants dominate)
    freq_bins = librosa.fft_frequencies(sr=sr)
    high_freq_mask = (freq_bins >= 4000) & (freq_bins <= 10000)
    sibilant_energy = np.mean(magnitude[high_freq_mask, :], axis=0)
    sibilant_times = librosa.times_like(sibilant_energy, sr=sr)
    
    # Normalize
    sibilant_normalized = (sibilant_energy - sibilant_energy.min()) / (sibilant_energy.max() - sibilant_energy.min() + 1e-10)
    
    # 2. PLOSIVE DETECTION (p, t, k, b, d, g)
    # Plosives create sudden bursts of energy across spectrum
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512)
    onset_times = librosa.times_like(onset_env, sr=sr, hop_length=512)
    
    # Find sharp onsets (plosive candidates)
    from scipy.signal import find_peaks
    plosive_peaks, _ = find_peaks(onset_env, height=np.percentile(onset_env, 85), distance=sr//1024)
    plosive_times = onset_times[plosive_peaks]
    plosive_strengths = onset_env[plosive_peaks]
    
    # 3. FRICATIVE DETECTION (f, v, th, h)
    # Fricatives: mid-to-high frequency noise, less sharp than sibilants
    mid_freq_mask = (freq_bins >= 2000) & (freq_bins <= 6000)
    fricative_energy = np.mean(magnitude[mid_freq_mask, :], axis=0)
    fricative_normalized = (fricative_energy - fricative_energy.min()) / (fricative_energy.max() - fricative_energy.min() + 1e-10)
    
    # 4. NASAL/LIQUID DETECTION (m, n, l, r)
    # Lower frequency, sustained energy
    low_freq_mask = (freq_bins >= 200) & (freq_bins <= 1500)
    nasal_energy = np.mean(magnitude[low_freq_mask, :], axis=0)
    nasal_normalized = (nasal_energy - nasal_energy.min()) / (nasal_energy.max() - nasal_energy.min() + 1e-10)
    
    # 5. VOCAL INTENSITY BURSTS
    # Track sudden changes that might indicate emotional emphasis
    rms = librosa.feature.rms(y=y, hop_length=512)[0]
    rms_times = librosa.times_like(rms, sr=sr, hop_length=512)
    rms_gradient = np.abs(np.gradient(rms))
    
    # 6. PHONEME DENSITY
    # Estimate how "busy" the vocals are (rapid delivery vs sustained notes)
    spectral_flux = librosa.onset.onset_strength(y=y, sr=sr)
    phoneme_density = np.mean(spectral_flux)
    
    # 7. EMOTIONAL CLASSIFICATION BASED ON PATTERNS
    emotional_indicators = {
        "aggressive": {
            "plosive_count": len(plosive_peaks),
            "mean_plosive_strength": float(np.mean(plosive_strengths)),
            "high_sibilance": float(np.mean(sibilant_normalized[sibilant_normalized > 0.7]))
        },
        "tense": {
            "mean_sibilance": float(np.mean(sibilant_normalized)),
            "sibilant_peaks": int(np.sum(sibilant_normalized > 0.6))
        },
        "smooth": {
            "mean_nasal_liquid": float(np.mean(nasal_normalized)),
            "low_plosive_rate": float(len(plosive_peaks) / duration)
        },
        "dynamic": {
            "phoneme_density": float(phoneme_density),
            "intensity_variation": float(np.std(rms))
        }
    }
    
    # 8. TIMELINE ANALYSIS
    # Create time-aligned phonetic features
    timeline = []
    for i, t in enumerate(sibilant_times):
        if i < len(fricative_normalized) and i < len(nasal_normalized):
            timeline.append({
                "time": float(t),
                "sibilance": float(sibilant_normalized[i]),
                "fricative": float(fricative_normalized[i]),
                "nasal_liquid": float(nasal_normalized[i])
            })
    
    # 9. CREATE VISUALIZATION
    fig, axes = plt.subplots(4, 1, figsize=(14, 12))
    
    # Phonetic energy patterns
    axes[0].plot(sibilant_times, sibilant_normalized, label='Sibilants (s, sh, z)', color='red', alpha=0.7)
    axes[0].plot(sibilant_times[:len(fricative_normalized)], fricative_normalized, label='Fricatives (f, v, th)', color='orange', alpha=0.7)
    axes[0].plot(sibilant_times[:len(nasal_normalized)], nasal_normalized, label='Nasals/Liquids (m, n, l, r)', color='blue', alpha=0.7)
    axes[0].set_title('Phonetic Pattern Energy Over Time')
    axes[0].set_ylabel('Normalized Energy')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Plosive events
    axes[1].plot(onset_times, onset_env, color='gray', alpha=0.5, label='Onset Strength')
    axes[1].scatter(plosive_times, plosive_strengths, color='red', s=100, zorder=5, label='Plosives (p, t, k, b, d, g)', marker='x')
    axes[1].set_title('Plosive Detection (Percussive Consonants)')
    axes[1].set_ylabel('Strength')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    # Vocal intensity changes
    axes[2].plot(rms_times, rms, label='RMS Intensity', color='purple')
    axes[2].plot(rms_times, rms_gradient, label='Intensity Change Rate', color='magenta', alpha=0.6)
    axes[2].set_title('Vocal Intensity and Dynamics')
    axes[2].set_ylabel('Amplitude')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    # Spectral flux (phoneme density indicator)
    spectral_flux_times = librosa.times_like(spectral_flux, sr=sr)
    axes[3].plot(spectral_flux_times, spectral_flux, color='green')
    axes[3].set_title('Spectral Flux (Phoneme Density / Vocal Activity)')
    axes[3].set_xlabel('Time (s)')
    axes[3].set_ylabel('Flux')
    axes[3].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    plot_path = output_path / "phonetic_patterns.png"
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    print(f"Saved phonetic pattern plot: {plot_path}")
    plt.close()
    
    # 10. COMPILE RESULTS
    results = {
        "file": str(audio_path),
        "duration_seconds": float(duration),
        "phonetic_summary": {
            "plosive_count": len(plosive_peaks),
            "plosives_per_second": float(len(plosive_peaks) / duration),
            "mean_sibilance": float(np.mean(sibilant_normalized)),
            "mean_fricative_energy": float(np.mean(fricative_normalized)),
            "mean_nasal_liquid_energy": float(np.mean(nasal_normalized)),
            "phoneme_density_score": float(phoneme_density)
        },
        "emotional_indicators": emotional_indicators,
        "notable_plosive_moments": [
            {"time": float(t), "strength": float(s)} 
            for t, s in zip(plosive_times[:20], plosive_strengths[:20])
        ],
        "interpretation": interpret_phonetic_patterns(emotional_indicators),
        "output_files": {
            "visualization": str(plot_path)
        }
    }
    
    # Save JSON report
    json_path = output_path / "phonetic_report.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Saved phonetic analysis: {json_path}")
    
    return results

def interpret_phonetic_patterns(indicators):
    """
    Provide human-readable interpretation of phonetic patterns
    """
    interpretations = []
    
    # Aggressive characteristics
    if indicators["aggressive"]["plosive_count"] > 20:
        interpretations.append("High plosive density suggests aggressive or emphatic delivery")
    
    if indicators["aggressive"]["mean_plosive_strength"] > 5.0:
        interpretations.append("Strong plosive bursts indicate forceful articulation")
    
    # Tense characteristics  
    if indicators["tense"]["mean_sibilance"] > 0.5:
        interpretations.append("Elevated sibilance may indicate tension or intensity")
    
    # Smooth characteristics
    if indicators["smooth"]["mean_nasal_liquid"] > 0.6:
        interpretations.append("High nasal/liquid content suggests smoother, more melodic vocals")
    
    if indicators["smooth"]["low_plosive_rate"] < 2.0:
        interpretations.append("Low plosive rate indicates sustained, flowing vocal style")
    
    # Dynamic characteristics
    if indicators["dynamic"]["phoneme_density"] > 15.0:
        interpretations.append("High phoneme density suggests rapid, complex vocal delivery")
    
    if indicators["dynamic"]["intensity_variation"] > 0.02:
        interpretations.append("High intensity variation indicates expressive, dynamic performance")
    
    if not interpretations:
        interpretations.append("Balanced phonetic characteristics across all categories")
    
    return interpretations

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python phonetic_analysis.py <audio_file> [output_dir]")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "phonetic_analysis"
    
    analyze_phonetic_patterns(audio_file, output_dir)
