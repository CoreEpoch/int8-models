# Core Epoch INT8 models

The INT8 ONNX computer-vision models published by [Core Epoch](https://coreepoch.dev).
Each Hugging Face page carries the model file, its measured accuracy table, and
run instructions.

| Model | Task | Accuracy | Size |
|---|---|---|---|
| [EdgeNeXt-S](https://huggingface.co/CoreEpoch/edgenext-small-int8-imagenet) | ImageNet-1K | 81.53% top-1 | 7.2 MB |
| [XCiT-Tiny-12/P8](https://huggingface.co/CoreEpoch/xcit-tiny12-p8-int8-imagenet) | ImageNet-1K | 81.16% top-1 | 8.6 MB |
| [TinyViT-5M](https://huggingface.co/CoreEpoch/tinyvit-5m-int8-imagenet) | ImageNet-1K | 80.53% top-1 | 9.2 MB |
| [RT-DETRv2-S](https://huggingface.co/CoreEpoch/rtdetrv2-s-int8-onnx) | COCO val2017 | 45.7 AP | 32.7 MB |

All four run on both ONNX Runtime and OpenVINO from the same file, with no GPU
required. Quantized with Kenosis, Core Epoch's proprietary post-training quantizer.
For licensing inquiries or custom model quantization: [coreepoch.dev/kenosis](https://coreepoch.dev/kenosis/) · licensing@coreepoch.dev

## License

This index is [Apache-2.0](LICENSE).

Notice: The open-source license applies strictly to the published model weights and ONNX inference graph. Core Epoch LLC explicitly reserves all proprietary rights, including patent, copyright, and trade secret rights, in the Kenosis quantization software, graph compilation toolchain, and underlying algorithmic optimization processes. No compiler license is granted or implied.

[coreepoch.dev](https://coreepoch.dev) · licensing@coreepoch.dev
