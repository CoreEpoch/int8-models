# Core Epoch INT8 models

INT8 ONNX computer vision models quantized with Kenosis by [Core Epoch](https://coreepoch.dev).
Each Hugging Face page has the model file, its accuracy measured against the FP32 original, and
run instructions.

| Model | Task | Accuracy | Size |
|---|---|---|---|
| [RF-DETR Base](https://huggingface.co/CoreEpoch/rfdetr-base-int8-onnx) | COCO val2017 | 53.1 AP | 41.9 MB |
| [RT-DETRv2-S](https://huggingface.co/CoreEpoch/rtdetrv2-s-int8-onnx) | COCO val2017 | 45.7 AP | 32.7 MB |
| [EdgeNeXt-S](https://huggingface.co/CoreEpoch/edgenext-small-int8-imagenet) | ImageNet-1K | 81.53% top-1 | 7.2 MB |
| [XCiT-Tiny-12/P8](https://huggingface.co/CoreEpoch/xcit-tiny12-p8-int8-imagenet) | ImageNet-1K | 81.16% top-1 | 8.6 MB |
| [TinyViT-5M](https://huggingface.co/CoreEpoch/tinyvit-5m-int8-imagenet) | ImageNet-1K | 80.53% top-1 | 9.2 MB |

All five run on ONNX Runtime and OpenVINO from the same file, on CPU, with no GPU required.

For licensing inquiries or custom model quantization: [coreepoch.dev/kenosis](https://coreepoch.dev/kenosis/#licensing) · licensing@coreepoch.dev

## License

This index is [Apache-2.0](LICENSE). Each model's license is on its Hugging Face page. None of
these licenses grants rights in Kenosis, Core Epoch's quantizer, which remains proprietary.
