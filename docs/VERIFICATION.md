# Verification update — September 22, 2026

Based on the final development-environment audit supplied by the project owner. This documentation checkout has not rerun the remote models.

| Evidence | Original result | Independent verification |
| --- | --- | --- |
| 0.8B text | 222/324, 68.52% | 221/324, 68.21%; one tied prediction changes |
| 9B text | 282/324, 87.04% | 283/324, 87.35%; one tied prediction changes |
| Driving development, stored predictions | 9B 0.6936038; 0.8B 0.6919085 | Recomputed exactly from stored candidate scores |
| Driving navtest, stored predictions | 0.8B 0.5115754; 9B 0.5351448 | Recomputed exactly across 12,146 scenes |
| Fresh 9B development inference | Original PDM 0.6936 | PDM 0.6898; five near-tie selections change; choice accuracy unchanged |
| Real-image inference | One 0.8B image-conditioned example | Interface passed at 1,008 image tokens; not an aggregate capability measurement |

Stored-score recomputation and fresh inference are different checks. Preserve original run tables and disclose reruns separately. The current figures show original results.

## Processor and timing

The NAVSIM/latency checkpoints use 401,408 max pixels and 364 actual image tokens. The single-image demo uses 1,048,576 max pixels and 1,008 tokens. The newer research campaign's 524,288-pixel setting yields 480 tokens. Do not combine these configurations under the historical “512” name.

Timing: resident unmerged PeftModel, H800, BF16, batch=1, synchronized GPU timing, 570 timed requests after 30 warmups. Included: JPEG decode, resize/normalize, tokenization, prefill, readout. Excluded: download, cold start, PDM evaluation. Reported memory is torch max_memory_allocated, not reserved or NVML usage.

The original environment used transformers 5.17.0 / peft 0.21.0 without torchvision. Verification used Python 3.10.19, torch 2.8.0+cu128, transformers 5.14.1, peft 0.20.0, accelerate 1.12.0, torchvision 0.23.0, Pillow 12.0.0. A Path-to-string loading shim was used in verification. A clean install guide requires the actual verified commands; this summary is not a substitute.

## Open documentation issues

- The audit labels the matched two-epoch image-free comparison completed, but cites model-size comparisons that do not establish matched exposure with the two-epoch multimodal student. Obtain checkpoint, epochs, initialization and split before claiming this ablation is resolved.
- No upstream commit is available for the NAVSIM v1 snapshot. Use snapshot/content fingerprints; no official leaderboard submission is recorded.
- The upstream published Nimble adapter's 90.12% is not our locally reproduced 9B score; its weights were unavailable for that verification.
- Critic and the large optimization campaign remain partial. Their different split and smoke-only metrics do not replace the completed NAVSIM table.

## Release maintenance

A secret-scanned staging set exists in the development environment, but it has not been imported into this local repository. Do not copy the full source tree: the audit identified exposed storage credentials requiring rotation, internal paths, and non-redistributable driving images. A clean staging scan does not establish that credentials were rotated.

Upstream source/data permission remains unresolved where no license is present; selecting our own license cannot grant rights to upstream material. Keep third-party notices and confirm reuse permissions before importing.

The critic's claimed durable backup was absent, and ongoing artifacts live in ephemeral cache storage. Back up checkpoints, optimizer state, manifests, predictions and logs to authorized durable storage before shutting down the development environment. Verify copied hashes. This local documentation task does not perform that remote backup.
