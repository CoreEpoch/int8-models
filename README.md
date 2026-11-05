# Core Epoch INT8 ONNX & CEPKv5 Models

INT8 ONNX models quantized with [Kenosis](https://coreepoch.dev/kenosis/) by [Core Epoch](https://coreepoch.dev) and packaged as `.cepk` (`CEPK0005`) encrypted runtime vaults.

| Model | Task | Accuracy vs FP32 | `.cepk` Vault Size | Speed vs FP32 |
|---|---|---|---|---|
| [RF-DETR Base](https://huggingface.co/CoreEpoch/rfdetr-base-int8-onnx) | COCO val2017 | 53.12 vs 53.32 AP | 36.3 MB | 67% faster |
| [RT-DETRv2-S](https://huggingface.co/CoreEpoch/rtdetrv2-s-int8-onnx) | COCO val2017 | 45.67 vs 48.13 AP | 32.3 MB | 70% faster |
| [EdgeNeXt-S](https://huggingface.co/CoreEpoch/edgenext-small-int8-imagenet) | ImageNet-1K | 81.535% vs 81.565% top-1 | 7.0 MB | 32% faster |
| [XCiT-Tiny-12/P8](https://huggingface.co/CoreEpoch/xcit-tiny12-p8-int8-imagenet) | ImageNet-1K | 81.16% vs 81.22% top-1 | 8.4 MB | 36% faster |
| [TinyViT-5M](https://huggingface.co/CoreEpoch/tinyvit-5m-int8-imagenet) | ImageNet-1K | 80.53% vs 80.87% top-1 | 9.0 MB | about the same |

All models execute on CPU through the native Rust `kenosis_cepk` runtime (`kenosis_cepk.dll` / `libkenosis_cepk.so`) with no GPU required. Evaluation downloads on Hugging Face require manual review approval.

For SDK runtime licensing, `.cepk` encrypted vault packaging, or strategic inquiries: [coreepoch.dev/kenosis](https://coreepoch.dev/kenosis/#licensing) · licensing@coreepoch.dev

## License

This index is [Apache-2.0](LICENSE). None of these licenses grants rights in Kenosis or the `CEPKv5` runtime, which remain proprietary to Core Epoch LLC.
