# DINOv3 Experiment Notes

Summary of experiments exploring DINOv3 as a potential approach for the verification pipeline.

- Objective: evaluate self-supervised features from DINOv3 for face/document matching and robust embedding extraction.
- Setup: ran feature extraction on recaptured ID images and selfie pairs; evaluated cosine similarity distributions.
- Initial Findings:
  - DINOv3 embeddings show promising clustering by identity in controlled lighting.
  - Cross-device variance remains an issue; normalization and augmented finetuning needed.
- Next steps:
  - Integrate a small-head classifier on top of frozen DINOv3 features for fine-grained verification.
  - Evaluate on recaptured multi-phone dataset (see `data_samples/DATASET_README.md`).
  - Measure latency and memory footprint for on-device vs server inference.

Notes:
- This repository contains notes and prototyping artifacts only; model weights and large datasets are stored externally.
