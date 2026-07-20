# Core Epoch INT8 models

This repository indexes the INT8 ONNX computer-vision models published by
[Core Epoch](https://coreepoch.dev), and documents how their numbers were
produced.

The model files and their cards live on Hugging Face, which is the canonical
source for both. What lives here is the material that does not fit on a model
card: the full measurement protocol behind every published number, and the
exact baseline invocations used for the comparison rows.

## The models

| Model | Task | Accuracy | Δ vs FP32 | Size | Speedup @1 thread |
|---|---|---|---|---|---|
| [EdgeNeXt-S](https://huggingface.co/CoreEpoch/edgenext-small-int8-imagenet) | ImageNet-1K | 81.53% top-1 | −0.03 | 7.2 MB | 1.29× |
| [XCiT-Tiny-12/P8](https://huggingface.co/CoreEpoch/xcit-tiny12-p8-int8-imagenet) | ImageNet-1K | 81.16% top-1 | −0.06 | 8.6 MB | 1.38× |
| [TinyViT-5M](https://huggingface.co/CoreEpoch/tinyvit-5m-int8-imagenet) | ImageNet-1K | 80.53% top-1 | −0.34 | 9.2 MB | see note |
| [RT-DETRv2-S](https://huggingface.co/CoreEpoch/rtdetrv2-s-int8-onnx) | COCO val2017 | 45.7 AP | −2.4 | 32.7 MB | 1.65× |

Classifier accuracy is top-1 on 49,872 ImageNet-1K validation images;
detection is AP50:95 on 4,800 COCO val2017 images. Speedup is measured against
each model's own FP32 baseline on one thread. TinyViT is faster than FP32 at
one thread and slower at four on ONNX Runtime, so its card carries no speed
claim; that model is published for its accuracy under quantization rather than
its latency.

Every file is standard ONNX opset 18 with no custom operators. All four run on
both ONNX Runtime and OpenVINO from the same file, with no GPU required.

## Run one

```
pip install onnxruntime numpy pillow huggingface_hub
```

```python
from huggingface_hub import hf_hub_download
import numpy as np, onnxruntime as ort
from PIL import Image

path = hf_hub_download("CoreEpoch/edgenext-small-int8-imagenet", "edgenext_s_320_int8.onnx")
sess = ort.InferenceSession(path, providers=["CPUExecutionProvider"])
img = Image.open("your_image.jpg").convert("RGB").resize((320, 320), Image.BICUBIC)
x = (np.asarray(img, np.float32) / 255.0 - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
logits = sess.run(None, {"input": x.transpose(2, 0, 1)[None].astype(np.float32)})[0]
print(int(np.argmax(logits)))
```

Each Hugging Face repo also ships `run_classify.py` (or `run_detect.py`) for a
local demo and `eval_imagenet.py` (or `eval_coco.py`) to reproduce that model's
headline number against your own copy of the validation set.

## How the numbers were measured

[PROTOCOL.md](PROTOCOL.md) documents the evaluation sets, preprocessing,
hardware, runtime versions, and the paired-comparison method used for every
number in the table above.

## Reproducing the baseline comparison

Each model card compares the published artifact against ONNX Runtime's own
static quantizer on the same model and the same calibration images. The exact
invocation for each comparison is in [baselines/](baselines/), so the
comparison can be re-run rather than taken on faith.

## About

These models are quantized with Kenosis, Core Epoch's post-training quantizer.
Kenosis itself is proprietary; the artifacts, cards, evaluation scripts, and
protocol are public.

[coreepoch.dev](https://coreepoch.dev) · core@coreepoch.dev
