# VisionJev

**Small multimodal models for fast, structured visual decisions.**

English | [简体中文](README_CN.md) · [DriveJev application branch](https://github.com/derekshiii/VisionJev/tree/drivejev)

**Project site:** not yet published — the static site is built in this repository and awaits GitHub Pages setup. Until it is live, this README is the entry point.

VisionJev is the general multimodal research direction of this repository. We build on [Bespoke Nimble](https://github.com/bespokelabsai/nimble), extending its text-only decision workflow to images and textual criteria through Qwen3.5's native vision-language backbone. Inspired by [Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev), the goal is to return decisions that software can use directly.

Our research now follows **visual evidence → structured judgment → downstream action**. We first improve general visual decisions, then transfer the resulting methods to autonomous driving in **DriveJev**.

**Research preview.** The current public repository contains project documentation and evaluated results. Model code is being prepared for release. General multimodal research continues on `visionjev`; driving work is preserved on `drivejev`.

## Motivation

An image-based application often needs a specific judgment: which candidate matches an object, whether a condition is visible, or how two objects are related. A compact decision model can provide that answer directly, while application code determines what happens next.

The central question is whether a small model makes its decision from the relevant visual evidence. A correct answer alone cannot distinguish visual understanding from a strong language prior. We therefore study image-dependent tasks, paired examples whose answers change with the image, and the effect of visual-token budgets on both quality and latency.

Our first target is **Qwen3.5-0.8B**. The 9B model provides a capacity reference. We prioritize experiments that remain useful with limited compute: frozen vision encoders, language-side adaptation, compact inputs, and a small set of controlled comparisons.

## Research path

| Stage | Question | Progress |
| --- | --- | --- |
| Text decisions | Can small models learn a bounded decision interface? | 0.8B and 9B reproduction complete |
| Multimodal input | Can real images enter training and decision inference correctly? | Training, reload, and a real-image smoke test verified |
| Visual decision quality | Does the model use the evidence needed by the question? | Current research priority |
| Efficient visual decisions | How much visual computation is necessary? | Controlled token-budget and adaptation studies planned |
| Driving transfer | Do visual improvements improve planning judgments? | Existing NAVSIM results on the DriveJev branch |

## Multimodal foundation

The existing implementation combines a Qwen3.5 vision encoder, image-token expansion, language-side LoRA, and answer-token scoring. Reported driving models freeze the vision encoder and condition decisions jointly on images and textual state.

A real 0.8B image-inference check has passed at **1,008 visual tokens**. Completed driving evaluations use **364 visual tokens**. These are different processor budgets; the new research will compare budgets under a common task and training protocol.

| Input | Judgment | Application output |
| --- | --- | --- |
| Image + candidates | Visual matching | Candidate identity |
| Image + condition | Visual verification | Yes/no decision |
| Image + objects or regions | Spatial relation | A relation from a defined set |

This table defines the next task suite. Broad visual benchmark results are not yet available.

## Text decision foundation

Using 2,676 training examples and a 324-example holdout, we reproduced the Nimble training recipe at two model sizes.

| Model | Base | Adapted, original run | Independent GPU rerun |
| --- | ---: | ---: | ---: |
| Qwen3.5-0.8B | 45.37% | **68.52%** | 68.21% |
| Qwen3.5-9B | 66.05% | **87.04%** | 87.35% |

<p align="center">
  <img src="assets/figures/text_results.png" width="620" alt="Original 0.8B text adaptation results">
</p>

*Original 0.8B results by task. Each independent rerun differs from its original model result by one tied decision. These are text holdout results, not visual benchmark scores.*

## Next experiments

1. **Visual evidence:** compare real images with matched image substitutions and an independently trained text-only baseline. Split related images and question variants together.
2. **Token efficiency:** hold data and training exposure fixed while comparing two measured image-token budgets. Report small-object and spatial-relation performance separately.
3. **Modality adaptation:** begin with a frozen vision encoder and language-side LoRA. Expand trainable components only after identifying a specific limitation.
4. **Generalization:** test new scenes, objects, and question templates, with option-order checks and per-task metrics.
5. **Driving transfer:** transfer the selected visual adaptation to DriveJev and compare against an equal-training control with the same candidate pool.

See the [multimodal research plan](docs/MULTIMODAL_PLAN_CN.md) for the initial experiment protocol and branch workflow.

## DriveJev: downstream application

The [DriveJev branch](https://github.com/derekshiii/VisionJev/tree/drivejev) preserves the driving methodology, figures, and completed NAVSIM evaluation. Its multimodal 0.8B and 9B systems achieved **0.5116** and **0.5351 PDM** on 12,146 navtest scenes, with **182 ms** and **335 ms** median inference latency on H800.

General visual improvements will be evaluated there under matched driving conditions. The aim is to establish which improvements transfer, rather than assuming a higher visual benchmark score implies better driving.

## Citation

If you use this research branch, cite VisionJev and record the **branch, code revision, model/adapter revision, and dataset release or split manifest**. Cite DriveJev separately when using its driving experiments.

```bibtex
@misc{visionjev2026,
  author = {{VisionJev Contributors}},
  title  = {{VisionJev}: Small Multimodal Models for Structured Visual Decisions},
  year   = {2026},
  url    = {https://github.com/derekshiii/VisionJev}
}
```

[CITATION.cff](CITATION.cff) · [References](references.bib)

## Acknowledgments

Built on [Bespoke Nimble](https://github.com/bespokelabsai/nimble) and Qwen3.5. Inspired by [Jev's System One interface](https://typesafe.ai/blog/introducing-system-one-models-and-jev) and [OpenJev](https://zefan-cai.github.io/open-jev/). Driving evaluation uses [NAVSIM](https://github.com/autonomousvision/navsim).
