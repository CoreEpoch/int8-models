# Core Epoch Kenosis Models

Core Epoch builds [Kenosis](https://coreepoch.dev/kenosis/), a Rust quantizer. Quantized models often shrink file size at the cost of accuracy or speed. Kenosis models are smaller than the originals, keep accuracy near the original, and run **faster** on CPU with no retraining. Each ships as an open-weight standard `.onnx` file that runs on CPU in both ONNX Runtime and OpenVINO.

| Model | Task | Accuracy vs. Original | Size (Kenosis vs. Original) | ONNX Runtime speed (1t / 4t) | OpenVINO speed (1t / 4t) |
|---|---|---|---|---|---|
| [RF-DETR Base Kenosis](https://huggingface.co/CoreEpoch/rfdetr-base-int8-onnx) | COCO val2017 | 53.12 vs. 53.32 AP | 36.3 vs. 115.1 MB | 69% / 44% faster | 93% / 91% faster |
| [EdgeNeXt-S Kenosis](https://huggingface.co/CoreEpoch/edgenext-small-int8-imagenet) | ImageNet-1K | 81.535% vs. 81.565% top-1 | 6.97 vs. 22.5 MB | 30% / 8% faster | 66% / 46% faster |
| [XCiT-Tiny-12/P8 Kenosis](https://huggingface.co/CoreEpoch/xcit-tiny12-p8-int8-imagenet) | ImageNet-1K | 81.16% vs. 81.22% top-1 | 8.37 vs. 27.0 MB | 36% / 14% faster | 79% / 70% faster |
| [tiny-voca Kenosis](https://huggingface.co/CoreEpoch/tiny-voca-kenosis) | English TTS (24 kHz) | 1.12% vs. 1.00% WER | 5.39 vs. 21.39 MB | 57% / 80% faster | 43% / 43% faster |

Speeds are measured against the original model on a CPU with AVX-VNNI. Accuracy above is measured in ONNX Runtime (each model card also lists OpenVINO).

Benchmarks and contact: [coreepoch.dev/kenosis](https://coreepoch.dev/kenosis/) · contact@coreepoch.dev

## License

This index is [Apache-2.0](LICENSE). Each repository's licenses (see its `LICENSE`, any `NOTICE` file, and any bundled third-party license files) cover the published repository files only and grant no rights in Kenosis, which remains proprietary to Core Epoch LLC.
