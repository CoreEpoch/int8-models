# Measurement protocol

Every number published on the Core Epoch model cards was produced by the
procedure below. It is written so the numbers can be checked rather than
trusted.

## Environment

| Item | Value |
|---|---|
| CPU | Intel Core i5-13420H |
| OS | Windows 11 |
| ONNX Runtime | 1.27.0, CPU execution provider |
| OpenVINO | 2026.2.0, CPU plugin |
| ONNX opset | 18, no custom operators |

## Evaluation sets

**ImageNet-1K (classifiers).** 49,872 images: the full 50,000-image validation
set minus a 128-image hold-out. The evaluation images are the official
validation files. This was checked rather than assumed — a 128-image sample was
downloaded individually from the official distribution and compared by SHA-256
against the local copies, and all 128 matched byte for byte, with the label
multiset matching the official solution file.

**COCO val2017 (detection).** 4,800 images: the full validation set minus the
200-image pool that calibration draws from. Scoring uses pycocotools bbox
evaluation.

## Calibration

Calibration uses 128 real images and no retraining. The source differs by
model, and each card states its own:

| Model | Calibration source |
|---|---|
| EdgeNeXt-S | ImageNet **training** split; no validation image is ever seen |
| XCiT-Tiny-12/P8 | 128-image validation slice, held out of the 49,872-image evaluation set |
| TinyViT-5M | 128-image validation slice, held out of the 49,872-image evaluation set |
| RT-DETRv2-S | 128 COCO images drawn from a 200-image pool excluded from evaluation |

For EdgeNeXt the two arms were measured against each other: training-split
calibration scored 81.320 and a validation slice scored 81.340 on the same
protocol, which is inside the confidence interval. The training-split arm ships
because its provenance is cleaner at no measured cost.

## Accuracy method

All arms of a comparison run on the **same preprocessed tensor** for each
image, in one decode pass. Results are therefore paired: the reported delta is
a per-image difference rather than a difference of two independently drifting
averages, and the 95% confidence interval comes from the count of images whose
prediction flipped in each direction.

Preprocessing follows each base checkpoint's published evaluation transform.
Classifiers use bicubic resize with the model's own crop fraction, `/255`, and
ImageNet mean/std. RT-DETRv2 uses a 640×640 bilinear resize and `/255` with no
mean/std normalization, matching its processor configuration.

Detection decoding applies sigmoid over the logits, takes a flat top-300 over
the (query, class) grid, and maps contiguous class indices to COCO category ids
in ascending order.

## Latency method

Median of 100 timed runs after 20 warmup runs, single real image, batch 1.
Reported at 1 thread and 4 threads.

One thread is the protocol we publish against. That is the deployment reality
for the multi-stream and fractional-vCPU cases these models target, where
per-core throughput decides capacity. It is also the stable measurement: on
this laptop, 4-thread timings move by 10% or more from run to run with thermal
state, so 4-thread figures are reported only where they were reproduced.

Arms compared for latency are always measured in the same run, because thermal
drift on a laptop is larger than several of the effects being measured.

## Cross-runtime check

Every published artifact compiles and runs on both ONNX Runtime and OpenVINO
from the same file. Accuracy equivalence between the two runtimes was measured
by running identical inputs through both and comparing predictions:

| Model | Sample | OpenVINO vs ONNX Runtime | Prediction agreement |
|---|---|---|---|
| EdgeNeXt-S | 2,000 images | −0.25 ±0.43 top-1 | 98.4% |
| XCiT-Tiny-12/P8 | 2,000 images | −0.45 ±0.58 top-1 | 97.7% |
| TinyViT-5M | 2,000 images | −0.55 ±0.56 top-1 | 97.2% |
| RT-DETRv2-S | 500 images | 46.3 vs 45.6 AP | — |

Every classifier interval includes zero. These are spot checks against the
full-set headline numbers, not a second headline protocol, and they are
reported as such.

## Baseline comparison

The comparison row on each card is ONNX Runtime's own static quantizer given
the same model and the same calibration images: QDQ format, per-channel
weights, UInt8 activations, Int8 weights, `quant_pre_process` where the export
accepts it, and onnxruntime's default MinMax calibration. On the EdgeNeXt and
XCiT exports `quant_pre_process` fails inside onnxruntime's symbolic shape
inference, so those baselines quantize the raw export; the scripts record the
failure and fall back the same way. onnxruntime also offers Percentile
and Entropy calibration and per-node exclusion lists; the comparison uses each
tool's standard invocation rather than a per-model tuned one. The exact
invocation for each model is in [baselines/](baselines/).

## What is not claimed

- ARM64 is verified under emulation rather than on hardware. The artifacts
  load and run under QEMU aarch64 with the aarch64 ONNX Runtime wheel,
  reproducing x86 predictions at 96.9% on a 128-image sample, with the
  disagreements being rank-1 versus rank-2 swaps on borderline images. No
  physical Raspberry Pi measurement is published.
- OpenVINO accuracy is a spot check. The headline accuracy numbers are ONNX
  Runtime measurements on the full evaluation sets.
- The numbers come from one machine. Absolute latency will differ on other
  hardware; the ratios are the transferable part, and even those depend on the
  runtime's kernel coverage for the target CPU.
