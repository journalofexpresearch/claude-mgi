#!/usr/bin/env python3
"""
Spectral Analysis - Core audio frequency analysis
Extracts frequency data, harmonics, and mathematical relationships from audio
"""

import librosa
import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def analyze_audio(audio_path, output_dir="analysis_output"):
    """
    Comprehensive spectral analysis of an audio file
    
    Args:
        audio_path: Path to audio file
        output_dir: Directory to save output files
    
    Returns:
        dict: Analysis results including frequency data, harmonics, and metrics
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Load audio
    y, sr = librosa.load(audio_path, sr=None)
    duration = len(y) / sr
    
    print(f"Loaded: {audio_path}")
    print(f"Duration: {duration:.2f}s, Sample rate: {sr}Hz")
    
    # 1. SPECTRAL ANALYSIS
    # Compute Short-Time Fourier Transform
    D = librosa.stft(y)
    magnitude = np.abs(D)
    phase = np.angle(D)
    
    # Convert to dB scale
    S_db = librosa.amplitude_to_db(magnitude, ref=np.max)
    
    # 2. HARMONIC ANALYSIS
    # Separate harmonics from percussives
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    
    # Compute chromagram (pitch classes)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    
    # 3. FREQUENCY DOMAIN FEATURES
    # Spectral centroid (brightness)
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    
    # Spectral rolloff
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    
    # Spectral bandwidth
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
    
    # Zero crossing rate
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    
    # 4. ENERGY AND DYNAMICS
    # RMS energy
    rms = librosa.feature.rms(y=y)[0]
    
    # 5. TEMPO AND RHYTHM
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    
    # 6. PITCH DETECTION
    pitches, magnitudes_pitch = librosa.piptrack(y=y, sr=sr)
    
    # Get dominant pitch over time
    pitch_timeline = []
    for t in range(pitches.shape[1]):
        index = magnitudes_pitch[:, t].argmax()
        pitch = pitches[index, t]
        pitch_timeline.append(pitch if pitch > 0 else 0)
    
    pitch_timeline = np.array(pitch_timeline)
    
    # 7. MATHEMATICAL RELATIONSHIPS
    # Detect consonant/dissonant patterns by analyzing frequency ratios
    consonance_score = calculate_consonance(chroma)
    
    # 8. CREATE VISUALIZATIONS
    fig, axes = plt.subplots(4, 1, figsize=(14, 12))
    
    # Spectrogram
    img1 = librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='hz', ax=axes[0])
    axes[0].set_title('Spectrogram (Frequency over Time)')
    axes[0].set_ylabel('Frequency (Hz)')
    fig.colorbar(img1, ax=axes[0], format='%+2.0f dB')
    
    # Chromagram
    img2 = librosa.display.specshow(chroma, sr=sr, x_axis='time', y_axis='chroma', ax=axes[1])
    axes[1].set_title('Chromagram (Pitch Classes)')
    fig.colorbar(img2, ax=axes[1])
    
    # Energy and Dynamics
    times = librosa.times_like(rms, sr=sr)
    axes[2].plot(times, rms, label='RMS Energy', color='blue', alpha=0.7)
    axes[2].plot(times, spectral_centroids / sr, label='Spectral Centroid (normalized)', color='red', alpha=0.7)
    axes[2].set_title('Energy and Spectral Characteristics')
    axes[2].set_xlabel('Time (s)')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    # Pitch timeline
    pitch_times = librosa.times_like(pitch_timeline, sr=sr)
    axes[3].plot(pitch_times, pitch_timeline, color='green', alpha=0.7)
    axes[3].set_title('Dominant Pitch Over Time')
    axes[3].set_xlabel('Time (s)')
    axes[3].set_ylabel('Frequency (Hz)')
    axes[3].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    spectrogram_path = output_path / "spectrogram.png"
    plt.savefig(spectrogram_path, dpi=150, bbox_inches='tight')
    print(f"Saved spectrogram: {spectrogram_path}")
    plt.close()
    
    # 9. COMPILE RESULTS
    results = {
        "file": str(audio_path),
        "duration_seconds": float(duration),
        "sample_rate": int(sr),
        "tempo_bpm": float(tempo),
        "num_beats": len(beats),
        "spectral_features": {
            "mean_centroid_hz": float(np.mean(spectral_centroids)),
            "mean_rolloff_hz": float(np.mean(spectral_rolloff)),
            "mean_bandwidth_hz": float(np.mean(spectral_bandwidth)),
            "mean_zero_crossing_rate": float(np.mean(zcr))
        },
        "energy": {
            "mean_rms": float(np.mean(rms)),
            "max_rms": float(np.max(rms)),
            "min_rms": float(np.min(rms)),
            "dynamic_range": float(np.max(rms) - np.min(rms))
        },
        "harmonic_characteristics": {
            "consonance_score": float(consonance_score),
            "mean_pitch_hz": float(np.mean([p for p in pitch_timeline if p > 0] or [0]))
        },
        "output_files": {
            "spectrogram": str(spectrogram_path)
        }
    }
    
    # Save JSON report
    json_path = output_path / "analysis_report.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Saved analysis report: {json_path}")
    
    return results

def calculate_consonance(chroma):
    """
    Calculate a consonance score based on chromagram
    Higher values indicate more consonant (harmonically stable) content
    Based on mathematical frequency ratios
    """
    # Perfect consonances (octave, fifth, fourth) have simple ratios
    # We look for clear pitch class patterns
    
    # Calculate variance - lower variance suggests more consonant relationships
    variance = np.var(chroma, axis=1).mean()
    
    # Calculate peak clarity - clearer peaks suggest stronger harmonic relationships
    peak_clarity = np.max(chroma, axis=1).mean()
    
    # Consonance score: high clarity, low variance
    consonance = peak_clarity / (variance + 0.01)  # Add small value to avoid division by zero
    
    return consonance

def compare_tracks(audio_path1, audio_path2, output_dir="comparison_output"):
    """
    Compare spectral characteristics between two audio files
    """
    print(f"\n=== Comparing Two Tracks ===")
    
    results1 = analyze_audio(audio_path1, output_dir + "/track1")
    results2 = analyze_audio(audio_path2, output_dir + "/track2")
    
    comparison = {
        "track1": results1["file"],
        "track2": results2["file"],
        "tempo_difference_bpm": abs(results1["tempo_bpm"] - results2["tempo_bpm"]),
        "spectral_similarity": {
            "centroid_diff_hz": abs(
                results1["spectral_features"]["mean_centroid_hz"] - 
                results2["spectral_features"]["mean_centroid_hz"]
            ),
            "bandwidth_diff_hz": abs(
                results1["spectral_features"]["mean_bandwidth_hz"] - 
                results2["spectral_features"]["mean_bandwidth_hz"]
            )
        },
        "energy_difference": abs(results1["energy"]["mean_rms"] - results2["energy"]["mean_rms"]),
        "consonance_difference": abs(
            results1["harmonic_characteristics"]["consonance_score"] - 
            results2["harmonic_characteristics"]["consonance_score"]
        )
    }
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    comparison_path = output_path / "comparison_report.json"
    with open(comparison_path, 'w') as f:
        json.dump(comparison, f, indent=2)
    
    print(f"\nComparison saved: {comparison_path}")
    return comparison

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python spectral_analysis.py <audio_file> [output_dir]")
        print("   or: python spectral_analysis.py --compare <audio1> <audio2> [output_dir]")
        sys.exit(1)
    
    if sys.argv[1] == "--compare":
        if len(sys.argv) < 4:
            print("Need two audio files for comparison")
            sys.exit(1)
        output_dir = sys.argv[4] if len(sys.argv) > 4 else "comparison_output"
        compare_tracks(sys.argv[2], sys.argv[3], output_dir)
    else:
        audio_file = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "analysis_output"
        analyze_audio(audio_file, output_dir)
