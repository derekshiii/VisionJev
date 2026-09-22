# DriveJev

**Fast multimodal decisions for autonomous driving.**

English | [简体中文](README_CN.md) · Branch: `drivejev` · [VisionJev research](https://github.com/derekshiii/DriveJev/tree/visionjev)

DriveJev builds on [Bespoke Nimble](https://github.com/bespokelabsai/nimble), extending its **text-only, single-modality decision interface** to visual observations and vehicle state. DriveJev jointly processes **images, textual criteria, and vehicle state** to produce structured decisions. With Qwen3.5 as the vision-language backbone, we follow a path from **text decisions → visual understanding → driving decisions**.

**Code release scheduled for September 23, 2026.**

## Motivation

Driving requires repeated, concrete decisions: whether to maintain speed, slow down, keep a proposed trajectory, or revise it as the scene changes. These decisions sit close to trajectory execution, where both the quality of a judgment and the time it takes to produce it matter.

Inspired by [Jev’s System One interface](https://typesafe.ai/blog/introducing-system-one-models-and-jev)—context in, structured decisions out—we bring this decision pattern to visual driving observations.

Our goal is a compact decision module between perception and motion planning: one that understands the current scene and returns a bounded answer that planning code can use directly. By reading scores for allowed answers, DriveJev avoids generating a reasoning trace or parsing free-form responses in this decision path.

We study how far a **0.8B model** can go, use **9B as a capacity reference**, and measure the trade-off between driving quality and end-to-end latency. The current application is trajectory selection; the next step is to assess and selectively correct a planner's proposal. Trajectory generation and vehicle control remain explicit components of the system.

## Text → vision → driving

| Stage | What we learn | Current progress |
| --- | --- | --- |
| **Text decisions** | Map context and criteria to choices, Boolean judgments, and ordered scores | Nimble recipe reproduced on 0.8B and 9B |
| **Visual understanding** | Connect image evidence with the same structured decision interface | Image-conditioned training, inference, and checkpoint reload established |
| **Driving decisions** | Combine road observations, ego motion, and plans to select an action | Multimodal trajectory selection evaluated on NAVSIM |

Nimble provides the starting point for structured text decisions. DriveJev brings the native visual capability of Qwen3.5 into that workflow, then adapts it to driving observations and trajectory supervision. For the current eight-way choice, all answer scores are read together after a single prompt prefill.

## Multimodal capability

DriveJev combines the **native Qwen3.5 vision encoder** with language-side LoRA adaptation. The visual encoder is frozen in the reported driving models; the adapted language model receives image tokens together with vehicle state and candidate plans.

| Component | Current implementation |
| --- | --- |
| Visual input | A real front-camera image processed with the official PIL image backend |
| Driving context | Ego state, motion history, navigation command, and candidate trajectories |
| Visual budget | **364 image tokens** for the reported driving checkpoints |
| Decision output | Candidate ID and a probability distribution over the supplied choices |
| Training pipeline | Shared image preparation for training and inference; checkpoint reload verified |

The multimodal pipeline is established on both 0.8B and 9B. Driving experiments test its value beyond the synthetic visual task used to validate the image pathway.

A real-image inference smoke test has also passed: the 0.8B adapter selected the offline-best candidate for the tested frame. That interface check used **1,008 image tokens**; the benchmark checkpoints above use **364**.

## Text decision results

Training on **2,676 examples** improves 0.8B reference-label agreement from **45.4% to 68.5%** on the **324-example holdout**: a gain of **23.1 percentage points**. Our **9B reproduction improves from 66.05% to 87.04%** on the same 324-example holdout.

<p align="center">
  <img src="assets/figures/text_results.png" width="620" alt="Text decision agreement before and after adaptation">
</p>

*Text adaptation on the Nimble holdout. Each line connects the base and adapted 0.8B model on the same task; values are percentages.*

| Model | Before adaptation | After adaptation |
| --- | ---: | ---: |
| DriveJev 0.8B · text | 45.37% | **68.52%** |
| DriveJev 9B · text | 66.05% | **87.04%** |

For context, [Nimble's published results](https://github.com/bespokelabsai/nimble#evaluation-on-324-held-out-examples) on its 324-example holdout are **90.12%** for Bespoke-Nimble-9B and **93.21%** for Jev 1.13.0. These author-reported results provide a larger-model reference; our table presents our own 0.8B and 9B reproductions.

A fresh GPU re-evaluation reproduced **221/324 (68.21%)** for 0.8B and **283/324 (87.35%)** for 9B, each one example away from the original saved run at a tied decision. The table and figure retain the original run results.

## Multimodal driving results

We combine a **front-view image, ego state, motion history, navigation command, and eight candidate trajectories**. Candidates are generated from the current vehicle state; the model selects a plan through its structured decision interface.

On **12,146 NAVSIM navtest scenes**, the 0.8B model achieves **0.5116 PDM** with **182 ms** median end-to-end inference, while the 9B model reaches **0.5351 PDM** at **335 ms**.

<p align="center">
  <img src="assets/figures/driving_results.png" width="520" alt="Multimodal driving quality versus median end-to-end latency">
</p>

*Driving quality versus inference latency. Higher and further left is better. The dashed line is the offline best-of-eight candidate score.*

| Model | PDM ↑ | Latency p50 ↓ | Latency p95 ↓ |
| --- | ---: | ---: | ---: |
| DriveJev 0.8B · multimodal | 0.5116 | **182 ms** | 191 ms |
| DriveJev 9B · multimodal | **0.5351** | 335 ms | 341 ms |
| Candidate-pool oracle | 0.6827 | — | — |

**Evaluation.** Local project evaluation on a NAVSIM v1 snapshot, covering 12,146 scenes across 136 logs with no missing or failed predictions. PDM uses a 0–1 scale and non-reactive replay. The oracle selects the best candidate using offline scores. The paired 9B advantage is approximately +0.0236 PDM, with a log-cluster bootstrap 95% interval of [+0.017, +0.031]. The selected 0.8B and 9B models received two and one epochs of driving adaptation, respectively.

**Timing.** H800, BF16, batch size 1, unmerged LoRA adapters; 200 scenes over three interleaved rounds, with 30 warm-up measurements excluded (570 timed requests). End-to-end timing includes JPEG decoding, resizing/normalization, tokenization, prefill, and answer readout, with CUDA synchronization. Image download, cold start, and PDM scoring are outside this boundary.

## Optimization path

Our experiments point to three connected priorities.

| Direction | Finding | Next step |
| --- | --- | --- |
| **Stronger text decisions** | Small-model adaptation improves structured judgments substantially | Improve supervision, candidate representations, and training efficiency |
| **More effective visual understanding** | On the development set, 9B improves from 0.6173 with text inputs to 0.6936 with images | Study visual-token budgets, modality alignment, and the environment information required for each decision |
| **Better driving decisions** | Both model choice and candidate coverage affect final PDM | Generalize to unfamiliar plans, assess risk and utility, and make constrained planning corrections |

For 0.8B, the initial image-conditioned model and text-only model performed similarly. Additional multimodal training improved the result, making **matched training exposure and better use of visual evidence** central to the next experiments. In the current development runs, increasing the visual budget from 364 to 1,008 tokens did not improve the score. We are therefore studying how to retain useful scene information with fewer tokens.

The driving roadmap moves from **selecting a plan** to **evaluating a supplied plan**, then **correcting it only when useful**. We will measure successful corrections alongside harmful interventions, progress, comfort, and latency. Closed-loop evaluation with execution delay is the next step toward testing the practical value of fast decisions.

**Research update · September 22.** Trajectory-critic experiments are underway: initial ego-only and lightweight-network runs are complete, and the image-conditioned critic is training. The larger optimization campaign has prepared labels for **30,272 scenes** and **57,668 image frames**. Full evaluations are still running; the tables above retain the completed text and NAVSIM results. Closed-loop evaluation is the next stage.

## Release

**September 23, 2026 — planned code release.**

The release will focus on the text-to-multimodal adaptation pipeline and driving experiments. Further trajectory-assessment and planning-correction work will follow as the research progresses.

## Citation

```bibtex
@misc{drivejev2026,
  author       = {{DriveJev Contributors}},
  title        = {{DriveJev}: Multimodal Decision Models for Autonomous Driving},
  year         = {2026},
  howpublished = {\url{https://github.com/derekshiii/DriveJev}},
  url          = {https://github.com/derekshiii/DriveJev}
}
```

## Acknowledgments

Built on [Bespoke Nimble](https://github.com/bespokelabsai/nimble) and Qwen3.5, with driving evaluation using [NAVSIM](https://github.com/autonomousvision/navsim). Inspired by the structured decision interfaces of [Jev](https://docs.typesafe.ai/concepts/state) and [OpenJev](https://zefan-cai.github.io/open-jev/).
