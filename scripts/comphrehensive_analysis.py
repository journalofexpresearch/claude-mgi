#!/usr/bin/env python3
"""
Comprehensive Music Analysis - Integrated spectral, emotional, and phonetic analysis
Provides complete mathematical "listening" experience
"""

import sys
import json
from pathlib import Path
import subprocess

def comprehensive_analysis(audio_path, output_dir="comprehensive_analysis"):
    """
    Run all analysis scripts and compile integrated report
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("COMPREHENSIVE MUSIC ANALYSIS")
    print("=" * 60)
    print(f"File: {audio_path}")
    print()
    
    # Get the script directory
    script_dir = Path(__file__).parent
    
    results = {
        "audio_file": str(audio_path),
        "analyses": {}
    }
    
    # 1. SPECTRAL ANALYSIS
    print("\n[1/3] Running Spectral Analysis...")
    print("-" * 60)
    try:
        spectral_dir = output_path / "spectral"
        subprocess.run([
            "python3",
            str(script_dir / "spectral_analysis.py"),
            audio_path,
            str(spectral_dir)
        ], check=True)
        
        # Load spectral results
        with open(spectral_dir / "analysis_report.json") as f:
            results["analyses"]["spectral"] = json.load(f)
        
        print("✓ Spectral analysis complete")
    except Exception as e:
        print(f"✗ Spectral analysis failed: {e}")
        results["analyses"]["spectral"] = {"error": str(e)}
    
    # 2. EMOTIONAL CADENCE
    print("\n[2/3] Running Emotional Cadence Analysis...")
    print("-" * 60)
    try:
        emotional_dir = output_path / "emotional"
        subprocess.run([
            "python3",
            str(script_dir / "emotional_cadence.py"),
            audio_path,
            str(emotional_dir)
        ], check=True)
        
        # Load emotional results
        with open(emotional_dir / "emotional_report.json") as f:
            results["analyses"]["emotional"] = json.load(f)
        
        print("✓ Emotional cadence analysis complete")
    except Exception as e:
        print(f"✗ Emotional cadence analysis failed: {e}")
        results["analyses"]["emotional"] = {"error": str(e)}
    
    # 3. PHONETIC PATTERNS
    print("\n[3/3] Running Phonetic Pattern Analysis...")
    print("-" * 60)
    try:
        phonetic_dir = output_path / "phonetic"
        subprocess.run([
            "python3",
            str(script_dir / "phonetic_analysis.py"),
            audio_path,
            str(phonetic_dir)
        ], check=True)
        
        # Load phonetic results
        with open(phonetic_dir / "phonetic_report.json") as f:
            results["analyses"]["phonetic"] = json.load(f)
        
        print("✓ Phonetic pattern analysis complete")
    except Exception as e:
        print(f"✗ Phonetic pattern analysis failed: {e}")
        results["analyses"]["phonetic"] = {"error": str(e)}
    
    # 4. CREATE INTEGRATED SUMMARY
    print("\n" + "=" * 60)
    print("INTEGRATED ANALYSIS SUMMARY")
    print("=" * 60)
    
    summary = create_integrated_summary(results)
    
    # Save summary
    summary_path = output_path / "integrated_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary to console
    print_summary(summary)
    
    print(f"\nAll results saved to: {output_path}")
    print(f"Integrated summary: {summary_path}")
    
    return summary

def create_integrated_summary(results):
    """
    Synthesize insights from all analyses
    """
    summary = {
        "audio_file": results["audio_file"],
        "mathematical_listening_experience": {}
    }
    
    try:
        # Extract key metrics
        spectral = results["analyses"].get("spectral", {})
        emotional = results["analyses"].get("emotional", {})
        phonetic = results["analyses"].get("phonetic", {})
        
        # Harmonic characteristics
        if "harmonic_characteristics" in spectral:
            summary["mathematical_listening_experience"]["harmonic_quality"] = {
                "consonance_score": spectral["harmonic_characteristics"].get("consonance_score"),
                "interpretation": interpret_consonance(spectral["harmonic_characteristics"].get("consonance_score", 0))
            }
        
        # Emotional journey
        if "emotional_arc" in emotional:
            summary["mathematical_listening_experience"]["emotional_journey"] = {
                "arc_type": emotional["emotional_arc"].get("type"),
                "intensity_progression": {
                    "beginning": emotional["emotional_arc"].get("early_intensity"),
                    "middle": emotional["emotional_arc"].get("mid_intensity"),
                    "end": emotional["emotional_arc"].get("late_intensity")
                },
                "key_moments": {
                    "peaks": len(emotional.get("emotional_moments", {}).get("peaks", [])),
                    "valleys": len(emotional.get("emotional_moments", {}).get("valleys", [])),
                    "major_releases": len(emotional.get("emotional_moments", {}).get("tension_releases", []))
                }
            }
        
        # Vocal character
        if "phonetic_summary" in phonetic:
            summary["mathematical_listening_experience"]["vocal_character"] = {
                "delivery_style": interpret_delivery_style(phonetic),
                "emotional_tone": phonetic.get("interpretation", []),
                "phonetic_metrics": {
                    "plosive_rate": phonetic["phonetic_summary"].get("plosives_per_second"),
                    "sibilance_level": phonetic["phonetic_summary"].get("mean_sibilance"),
                    "phoneme_density": phonetic["phonetic_summary"].get("phoneme_density_score")
                }
            }
        
        # Overall impression
        summary["mathematical_listening_experience"]["overall_impression"] = generate_overall_impression(spectral, emotional, phonetic)
        
    except Exception as e:
        summary["error"] = f"Error creating summary: {e}"
    
    return summary

def interpret_consonance(score):
    """Interpret consonance score"""
    if score is None:
        return "Unable to calculate"
    if score > 40:
        return "Highly consonant - mathematically stable, harmonically pure"
    elif score > 25:
        return "Moderately consonant - balanced harmonic relationships"
    elif score > 15:
        return "Mixed consonance/dissonance - dynamic tension"
    else:
        return "Dissonant - complex, tense harmonic relationships"

def interpret_delivery_style(phonetic):
    """Interpret vocal delivery from phonetic data"""
    summary = phonetic.get("phonetic_summary", {})
    
    plosive_rate = summary.get("plosives_per_second", 0)
    density = summary.get("phoneme_density_score", 0)
    
    if plosive_rate > 3 and density > 15:
        return "Aggressive, rapid delivery with percussive emphasis"
    elif plosive_rate > 2:
        return "Emphatic delivery with strong articulation"
    elif density > 15:
        return "Fast-paced, dense vocal delivery"
    elif plosive_rate < 1.5 and summary.get("mean_nasal_liquid_energy", 0) > 0.5:
        return "Smooth, melodic vocal style"
    else:
        return "Balanced, moderate delivery"

def generate_overall_impression(spectral, emotional, phonetic):
    """Generate integrated interpretation"""
    impressions = []
    
    # Harmonic impression
    if "harmonic_characteristics" in spectral:
        consonance = spectral["harmonic_characteristics"].get("consonance_score", 0)
        if consonance > 30:
            impressions.append("Harmonically elegant with clear mathematical relationships")
        elif consonance < 15:
            impressions.append("Harmonically complex with sophisticated tension patterns")
    
    # Emotional impression
    if "emotional_arc" in emotional:
        arc = emotional["emotional_arc"].get("type", "")
        if "Building" in arc:
            impressions.append("Progressive emotional buildup toward climax")
        elif "Peak" in arc:
            impressions.append("Dramatic mid-point climax with surrounding dynamics")
    
    # Phonetic impression
    if "interpretation" in phonetic:
        if any("aggressive" in i.lower() for i in phonetic["interpretation"]):
            impressions.append("Forceful, intense vocal delivery")
        if any("smooth" in i.lower() or "melodic" in i.lower() for i in phonetic["interpretation"]):
            impressions.append("Flowing, sustained vocal approach")
    
    if not impressions:
        impressions.append("Balanced composition across multiple dimensions")
    
    return impressions

def print_summary(summary):
    """Print formatted summary to console"""
    exp = summary.get("mathematical_listening_experience", {})
    
    if "harmonic_quality" in exp:
        print("\n🎵 HARMONIC QUALITY:")
        hq = exp["harmonic_quality"]
        print(f"   Consonance Score: {hq.get('consonance_score', 'N/A'):.2f}")
        print(f"   {hq.get('interpretation', '')}")
    
    if "emotional_journey" in exp:
        print("\n💫 EMOTIONAL JOURNEY:")
        ej = exp["emotional_journey"]
        print(f"   Arc Type: {ej.get('arc_type', '')}")
        prog = ej.get("intensity_progression", {})
        print(f"   Progression: {prog.get('beginning', 0):.3f} → {prog.get('middle', 0):.3f} → {prog.get('end', 0):.3f}")
        moments = ej.get("key_moments", {})
        print(f"   Key Moments: {moments.get('peaks', 0)} peaks, {moments.get('valleys', 0)} valleys, {moments.get('major_releases', 0)} releases")
    
    if "vocal_character" in exp:
        print("\n🎤 VOCAL CHARACTER:")
        vc = exp["vocal_character"]
        print(f"   Style: {vc.get('delivery_style', '')}")
        if vc.get("emotional_tone"):
            print("   Characteristics:")
            for tone in vc["emotional_tone"][:3]:
                print(f"      • {tone}")
    
    if "overall_impression" in exp:
        print("\n🌟 OVERALL IMPRESSION:")
        for impression in exp["overall_impression"]:
            print(f"   • {impression}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python comprehensive_analysis.py <audio_file> [output_dir]")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "comprehensive_analysis"
    
    comprehensive_analysis(audio_file, output_dir)
