# CantoMap-Liujgoj

This repository contains a comprehensively transliterated and streamlined version of the **CantoMap** corpus, strictly converted into **Liujgoj (溜歌粵語)**—a standalone, character-free orthography designed for computational linguistics and Cantonese AI architecture.

The original data belongs to the [gwinterstein/CantoMap](https://github.com/gwinterstein/CantoMap) project. This derivative version strips away heavy unlinked binary assets to provide a lightweight, high-density textual corpus tailored for Cantonese natural language processing.

---

## 🎯 Key Modifications

1. **Strict Liujgoj Transliteration**: Every standard Jyutping syllable has been mapped onto the Liujgoj orthographic inventory, replacing numerical tone marks with letter-based tone markers (`j`, `r`, `x`, `q`, `h`).
2. **Purged Large File Storage (LFS) Overhead**: All broken or unlinked binary/multimedia placeholders (`.wav` audio shells and `.pdf` maps) have been completely removed. The repository is 100% text-driven, lightweight (~1.65 MiB), and optimized for instant cloning/streaming.

---

## 📦 Dataset Features

- **Format & Structure**: Contains **102 EAF (ELAN Annotation Format) files** across organized subfolders, maintaining the exact conversational structure of the original Map Task.
- **Preserved Linguistic Integrity**: 
  - **Word Boundaries**: Retains the exact word-segmentation and token spacing intended by the original transcribers.
  - **Colloquial Markers**: Preserves all native speech-act annotations, filled pauses (`#`), and lengthening markers.
  - **Variant Pronunciations**: Safely preserves phonetic variant tags (e.g., `waih|wair`, `gam|gamr`), making it a goldmine for analyzing morphological tone changes and spontaneous phonetic drifts.

---

## 🤖 AI & LLM Training Applications

This corpus is highly valuable for developing **Speech-Native Multimodal AI** and training **Cantonese Large Language Models (LLMs)**:

- **Stage 1 Continual Pre-training (CPT)**: The pure alphabetical stream of Liujgoj eliminates tokenization fragmentation caused by mixed alphanumeric strings (like `laa1aa1`).
- **Turn-taking & Interactivity**: The interactive Map Task structure provides raw data for fine-tuning conversational agents on genuine, collaborative human dialogue.

### Quick Python Snippet to Parse Text

You can easily extract the Liujgoj text tiers for language modeling using standard XML parsing:

```python
import xml.etree.ElementTree as ET

def extract_liujgoj(eaf_path):
    tree = ET.parse(eaf_path)
    root = tree.getroot()
    texts = []
    for tier in root.findall(".//TIER"):
        tier_id = tier.get("TIER_ID", "")
        if tier_id.endswith("-jyutping") or tier_id == "jyutping":
            for ann in tier.findall(".//ANNOTATION_VALUE"):
                if ann.text:
                    texts.append(ann.text)
    return texts
```

---

📄 Attribution & License
Attribution
The original data and speech-act annotations belong to the CantoMap project created by gwinterstein and collaborators.

Original Repository: gwinterstein/CantoMap

If you use this dataset, please ensure you credit and cite the original parent project accordingly.

License
This derivative dataset is distributed under the CC BY-NC-SA 4.0 (Attribution-NonCommercial-ShareAlike 4.0 International) license, strictly inheriting the original licensing terms of the parent CantoMap corpus.
