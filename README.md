# Core Epoch INT8 ONNX Models

Open-weight INT8 ONNX models quantized with [Kenosis](https://coreepoch.dev/kenosis/) by [Core Epoch](https://coreepoch.dev).

| Model | Task | Accuracy vs FP32 | INT8 ONNX Size | Speed vs FP32 |
|---|---|---|---|---|
| [RF-DETR Base](https://huggingface.co/CoreEpoch/rfdetr-base-int8-onnx) | COCO val2017 | 53.12 vs 53.32 AP | 36.3 MB | 67% faster |
| [RT-DETRv2-S](https://huggingface.co/CoreEpoch/rtdetrv2-s-int8-onnx) | COCO val2017 | 45.67 vs 48.13 AP | 32.3 MB | 70% faster |
| [EdgeNeXt-S](https://huggingface.co/CoreEpoch/edgenext-small-int8-imagenet) | ImageNet-1K | 81.535% vs 81.565% top-1 | 6.97 MB | 32% faster |
| [XCiT-Tiny-12/P8](https://huggingface.co/CoreEpoch/xcit-tiny12-p8-int8-imagenet) | ImageNet-1K | 81.16% vs 81.22% top-1 | 8.37 MB | 36% faster |
| [TinyViT-5M](https://huggingface.co/CoreEpoch/tinyvit-5m-int8-imagenet) | ImageNet-1K | 80.53% vs 80.87% top-1 | 8.99 MB | about the same |

All models are standard `.onnx` files that run directly in ONNX Runtime and OpenVINO on CPU (speeds measured on a CPU with AVX-VNNI, 1 thread).

Benchmarks and contact: [coreepoch.dev/kenosis](https://coreepoch.dev/kenosis/) · contact@coreepoch.dev

## License

This index is [Apache-2.0](LICENSE). Each model's MIT or Apache-2.0 license covers the model files only and grants no rights in Kenosis, which remains proprietary to Core Epoch LLC.
