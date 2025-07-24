# Animated Intelligence Podcast Transcript Generation Workflow

## Episode List (8 Total)
Based on Apple Podcasts search, need to catalog all episodes with:
- Episode numbers/titles
- Publication dates  
- Guest information
- Episode lengths

## Transcription Strategy

### Phase 1: Audio File Collection
1. Download high-quality audio files from podcast hosting platform
2. Organize by episode in MCP_SYSTEM/podcast_audio/
3. Standardize naming: `AnimatedIntelligence_E01_[Title].mp3`

### Phase 2: Automated Transcription
**Recommended Tool: Descript**
- Upload all 8 episodes
- Batch process with speaker identification
- Export as text files with timestamps
- Cost estimate: ~$20-40 for full series

**Alternative: OpenAI Whisper (Free)**
```bash
# Install whisper
pip install openai-whisper

# Process each episode
whisper episode01.mp3 --model large --output_format txt --output_dir transcripts/
```

### Phase 3: Quality Enhancement
1. Review for technical AI/ML terminology accuracy
2. Add speaker labels (Scott Broock, Mike Seymour, guests)
3. Format for readability
4. Add timestamps for key segments

### Phase 4: Integration
- Save to MCP_SYSTEM/podcast_transcripts/
- Create searchable database in Obsidian
- Tag with episode themes and concepts
- Link to related research notes

## Technical Requirements
- Audio quality: 44.1kHz/16-bit minimum
- File format: WAV or high-bitrate MP3
- Total estimated processing time: 2-4 hours
- Storage needed: ~500MB for audio + transcripts

## Deliverables
- 8 complete episode transcripts
- Searchable text database
- Key themes index
- Speaker-identified versions
- Timestamp references for quotes
