# Rhythm and Timing Analysis Reference

## Quick BPM Calculation Methods

### The 6-Second Method
1. Find section with clear, steady beat
2. Count all beats (kicks, snares, hats) in exactly 6 seconds
3. Multiply count by 10
4. Result = approximate BPM

**Example:**
- Count in 6 seconds: 12 beats
- 12 × 10 = 120 BPM

### The 10-Second Method
1. Find section with clear, steady beat
2. Count all beats in exactly 10 seconds
3. Multiply count by 6
4. Result = approximate BPM

**Example:**
- Count in 10 seconds: 20 beats
- 20 × 6 = 120 BPM

### Mathematical Basis
- 60 seconds per minute
- 6 seconds = 60/10 → multiply by 10
- 10 seconds = 60/6 → multiply by 6

## Drum Frequency Reference Chart

### Sub-Bass (20-60 Hz)
**Instruments:** Electronic sub-bass, 808 bass, synth bass
**Characteristics:**
- Felt more than heard
- Requires good subwoofers to reproduce
- Creates physical chest vibration
- Foundation of modern electronic music

**In spectrograms:**
- Lowest visible energy
- Appears as horizontal bands (sustained)
- Or vertical spikes (sub-bass drops)

### Kick Drum (60-100 Hz)
**Fundamental frequency range**
**Characteristics:**
- Primary low-frequency transient
- Marks downbeats in most music
- "Thump" or "punch" of the kick
- Core of the rhythm section

**Spectral signature:**
- Bright vertical lines/spots
- Clear transients in low-frequency band
- Typically evenly spaced in modern music
- May show pitch variation in acoustic kicks

**Genre variations:**
- EDM: Clean sine wave kick (60-80 Hz)
- Rock: Broader spectrum kick (80-100 Hz)
- Hip-hop: Deep 808 kick (40-60 Hz)
- Jazz: Acoustic kick (70-90 Hz with overtones)

### Snare Drum (200 Hz + 2-6 kHz)
**Body resonance + crack/snap**
**Characteristics:**
- Appears in TWO frequency bands simultaneously
- Body: ~200 Hz (drum shell resonance)
- Crack: 2-6 kHz (snare wires rattling)
- Defines backbeat (beats 2 & 4 in 4/4)

**Spectral signature:**
- Dual-band transient pattern
- Vertical line at 200 Hz
- Corresponding vertical line at 2-6 kHz
- Both appear at same moment in time

**Genre variations:**
- Rock: Loud crack (strong 2-6 kHz)
- Jazz: Brushes (minimal high frequencies)
- Electronic: Clap samples (mostly 1-4 kHz)

### Tom Drums (80-400 Hz)
**Pitch-dependent percussion**
**Characteristics:**
- Floor tom: 80-120 Hz (low, rumbling)
- Mid tom: 120-200 Hz (melodic middle)
- High tom: 200-400 Hz (sharp, cutting)
- Used for fills and transitions

**Spectral signature:**
- Pitched transients (specific frequency center)
- Brief duration (not sustained)
- Often appear in sequences (fills)
- May show slight pitch decay

### Hi-Hats and Cymbals (6-20 kHz)
**High-frequency percussion**
**Characteristics:**
- Brightest spectral elements
- Often plays subdivisions (8ths, 16ths)
- Creates rhythmic texture and "sizzle"
- Closed hat: Tighter, shorter
- Open hat: Longer, more sustained
- Crash: Wide spectrum, longer decay
- Ride: Sustained "ping" pattern

**Spectral signature:**
- Very high frequency content only
- Regular pattern of transients (if hi-hat)
- Wide frequency splash (if cymbal crash)
- May show slight pitch modulation

## Time Signature Patterns

### 4/4 (Common Time)
**Most common in:** Pop, rock, EDM, hip-hop, funk

**Beat pattern:** Strong-weak-strong-weak (or 1-2-3-4)

**Typical rhythm section pattern:**
```
Beat:    1     2     3     4
Kick:    X           X      
Snare:         X           X
Hi-hat:  X  X  X  X  X  X  X  X
```

**In spectrograms:**
- Kick on beats 1 & 3 (60-100 Hz)
- Snare on beats 2 & 4 (200 Hz + 2-6 kHz)
- Hi-hat every eighth note (6-20 kHz)
- Even spacing between all elements

**Measure length calculation:**
- 4 beats per measure
- At 120 BPM: 4 beats × (60/120) = 2 seconds per measure
- At 140 BPM: 4 beats × (60/140) = 1.71 seconds per measure

### 3/4 (Waltz Time)
**Most common in:** Waltzes, some ballads, country

**Beat pattern:** Strong-weak-weak (or 1-2-3)

**Typical rhythm section pattern:**
```
Beat:    1     2     3
Kick:    X           
Snare:         X     X
Hi-hat:  X  X  X  X  X  X
```

**In spectrograms:**
- Kick on beat 1 only (strong)
- Lighter snare or rim on beats 2 & 3
- Groups of three visible
- Longer "breathing" feel than 4/4

**Measure length calculation:**
- 3 beats per measure
- At 180 BPM: 3 beats × (60/180) = 1 second per measure
- At 120 BPM: 3 beats × (60/120) = 1.5 seconds per measure

### 6/8 (Compound Meter)
**Most common in:** Irish jigs, some ballads, Baroque music

**Beat pattern:** Strong-weak-weak-strong-weak-weak

**Felt as:** Two main beats, each subdivided into three

**Typical rhythm section pattern:**
```
Beat:    1  &  a  2  &  a
Kick:    X        X      
Snare:         X        X
Hi-hat:  X  X  X  X  X  X
```

**In spectrograms:**
- Two strong kicks per measure
- Grouped in threes (triplet feel)
- Lilting, flowing rhythm
- Differs from 3/4 by subdivision

**Measure length calculation:**
- 6 eighth notes per measure (felt as 2 beats)
- At 120 BPM (counted in dotted quarters): 2 beats × (60/120) = 1 second per measure

### 7/4 or 7/8 (Odd Meter)
**Most common in:** Progressive rock, jazz fusion, Balkan music

**Beat pattern:** Various groupings (2+2+3, 3+2+2, 3+4, etc.)

**In spectrograms:**
- Irregular spacing creates "limp" or "uneven" feel
- Pattern repeats, but with unusual grouping
- Requires careful counting to identify
- Look for consistent asymmetric pattern

### 5/4 (Odd Meter)
**Most common in:** Jazz, progressive rock (e.g., "Take Five")

**Beat pattern:** Often 3+2 or 2+3

**Typical pattern (3+2):**
```
Beat:    1     2     3  |  4     5
Kick:    X           X     X      
Snare:         X              X
```

**In spectrograms:**
- Clearly grouped in fives
- Asymmetric feel
- Pattern repeats consistently

## Phrase Structure Patterns

### 4-Bar Phrases (Most Common)
- Standard building block of popular music
- Verse, chorus, bridge typically multiples of 4
- In spectrogram: Repetition every ~8-16 seconds (depending on tempo)

**Example at 120 BPM:**
- 4 bars = 16 beats
- 16 beats × (60/120 seconds per beat) = 8 seconds

### 8-Bar Sections
- Complete verse or chorus
- Standard length for melodic ideas
- In spectrogram: Major texture/pattern change every ~16-32 seconds

### 16-Bar Sections
- Full statement of musical idea
- Often paired 8-bar phrases
- In spectrogram: Large-scale structural boundaries

### Phrase Boundary Markers

**Drum fills:**
- Rapid succession of toms/snares
- Typically last 1-2 beats
- Occur at end of 4 or 8 bar phrase
- Create spectral "burst" pattern

**Cymbal crashes:**
- Mark phrase beginnings (downbeat of new section)
- Bright flash across high frequencies
- Often coincides with chord change

**Texture changes:**
- Instruments enter or exit
- Visible as density increase/decrease
- Marks formal sections (verse → chorus)

**Dynamic shifts:**
- Overall brightness changes
- Crescendo into new section
- Sudden drop for dynamics

## Tempo Terminology and Ranges

### Classical Tempo Markings
- **Grave:** Very slow, solemn (< 40 BPM)
- **Largo:** Broadly, slowly (40-60 BPM)
- **Adagio:** Slow (60-80 BPM)
- **Andante:** Walking pace (80-108 BPM)
- **Moderato:** Moderate (108-120 BPM)
- **Allegro:** Fast, lively (120-168 BPM)
- **Presto:** Very fast (168-200 BPM)
- **Prestissimo:** Extremely fast (> 200 BPM)

### Modern Genre Tempo Ranges

**Hip-Hop:** 60-100 BPM (often half-time feel makes it feel 120-200)

**Trap:** 130-170 BPM (but kick pattern creates half-time feel)

**House:** 120-130 BPM (four-on-the-floor kick pattern)

**Techno:** 120-150 BPM (driving, mechanical feel)

**Drum & Bass:** 160-180 BPM (fast breakbeats)

**Dubstep:** 135-145 BPM (half-time feel, heavy wobble bass)

**Pop:** 100-130 BPM (varies widely by era)

**Rock:** 110-140 BPM (energetic, driving)

**Metal:** 120-180+ BPM (fast, aggressive)

**Jazz:** 60-200+ BPM (extremely variable, often rubato)

**Reggae:** 60-90 BPM (relaxed, emphasis on offbeat)

## Rubato and Tempo Flexibility

### Strict Tempo (Quantized)
**Characteristics:**
- Mechanical precision
- All beats perfectly aligned to grid
- No human variation
- BPM constant throughout

**Musical contexts:**
- Electronic dance music
- Modern pop production
- Sequenced/programmed music
- Metronome practice tracks

**In spectrograms:**
- Perfectly regular transient spacing
- Vertical alignment across all frequencies
- Mathematical precision visible

### Dynamic Tempo (Rubato)
**Characteristics:**
- Human flexibility
- Tempo varies moment-to-moment
- "Stolen time" (rubato = "robbed")
- Follows phrasing and emotional intent

**Musical contexts:**
- Classical performance
- Jazz interpretation
- Singer-songwriter material
- Expressive instrumental solos

**In spectrograms:**
- Irregular transient spacing
- Accelerando: transients closer together
- Ritardando: transients farther apart
- Organic, breathing quality

**Common rubato patterns:**
- Phrase ending ritardando (slowing at cadences)
- Pickup notes rushed into downbeat
- Climactic passages accelerating
- Lyrical passages with flexible timing

### Hybrid Approaches
**Electronic + Classical fusion (your Vivaldi remix):**
- Strict tempo for electronic elements
- Rubato for classical passages
- Switching between mechanical and organic
- Best of both worlds

**Jazz with rhythm section:**
- Rhythm section keeps steady time
- Soloist plays freely over the time
- "Time" vs. "out of time"

## Analyzing Your Vivaldi Winter Remix

### Structural Timing Decisions

**Movement 1 (Allegro - Storm):**
- Short phrases of strict 4/4 (modern electronic foundation)
- Dynamic timing in Baroque passages (classical flexibility)
- Frequency riser builds tension (EDM production technique)
- Sub-bass foundation at specific BPM anchors modern sections
- Fusion serves narrative: storm = chaos = mixture of strict/free

**Movement 2 (Largo - Calm):**
- Primarily maintains Baroque flexibility
- Minimal strict quantization
- Sub-bass at 48-49 Hz adds weight without imposing grid
- Gentle, flowing feel preserved
- Enhancement serves narrative: calm = organic = less electronic intervention

## Practical Analysis Tips

### Finding the Beat in Complex Music

1. **Start with lowest frequencies** (kick drum easiest to identify)
2. **Look for patterns** (repetition reveals structure)
3. **Check multiple frequency bands** (confirm timing across instruments)
4. **Use longer time windows** (phrase structure becomes clearer)
5. **Compare similar sections** (verify pattern consistency)

### Dealing with Tempo Changes

1. **Section-by-section analysis** (calculate BPM for each section separately)
2. **Graph tempo over time** (visualize accelerando/ritardando)
3. **Identify stable sections** (use as reference points)
4. **Mark transition points** (where tempo shifts occur)

### Verifying Time Signature

1. **Count beats between accents** (confirms grouping)
2. **Look for pattern repetition** (time signature creates cyclical structure)
3. **Check multiple measures** (ensure consistency)
4. **Listen for "strong" beats** (downbeats have more instruments/emphasis)

## Integration with Other Analysis

### Rhythm + Harmony
- Chord changes align with measure boundaries
- Harmonic rhythm (chord change rate) relates to meter
- Cadences fall on strong beats

### Rhythm + Form
- Section boundaries marked by rhythmic changes
- Verse/chorus distinguished partly by rhythm
- Build-ups use rhythmic intensification

### Rhythm + Production
- Compression emphasizes transients
- Reverb affects perceived rhythm
- Panning creates spatial rhythm

## Remember: Context Matters

**Cultural context:**
- Different traditions emphasize different aspects of rhythm
- African music: Complex polyrhythm
- Western classical: Precise notation, tempo markings
- Jazz: Swing feel, flexible time
- Electronic: Grid-based precision

**Historical context:**
- Pre-metronome music had no absolute tempo
- Recording enabled tempo consistency
- Quantization made mechanical precision possible
- Modern music blends strict and flexible approaches

**Musical intent:**
- Rhythm serves the emotion and narrative
- Strict timing can create energy and drive
- Flexible timing can create intimacy and expression
- The best music uses timing purposefully
