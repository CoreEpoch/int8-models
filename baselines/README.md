# Baseline invocations

Each model card compares the published INT8 artifact against ONNX Runtime's
own static quantizer, given the same base model and the same 128 calibration
images. These are the exact scripts that produced those comparison rows.

They are here so the comparison can be re-run. A collapse claim nobody can
reproduce is worth nothing.

| Model | Base checkpoint | ONNX Runtime static result | Published INT8 |
|---|---|---|---|
| EdgeNeXt-S | `timm/edgenext_small.usi_in1k` | 33.74% top-1 | 81.53% |
| XCiT-Tiny-12/P8 | `timm/xcit_tiny_12_p8_224.fb_dist_in1k` | 64.95% top-1 | 81.16% |
| TinyViT-5M | `timm/tiny_vit_5m_224.dist_in22k_ft_in1k` | 3.12% top-1 | 80.53% |
| RT-DETRv2-S | `PekingU/rtdetr_v2_r18vd` | 4.2 AP | 45.7 AP |

## Running one

```
pip install onnxruntime numpy pillow onnx
python quantize_baseline.py <fp32_model.onnx> <calib_dir> <out.onnx>
```

Then evaluate the output with the `eval_imagenet.py` or `eval_coco.py` script
shipped in that model's Hugging Face repo, using the same evaluation set
described in [../PROTOCOL.md](../PROTOCOL.md).

## Notes

The configuration is QDQ format, per-channel weights, UInt8 activations, Int8
weights, `quant_pre_process` where the export accepts it (the EdgeNeXt and
XCiT exports fail its symbolic shape inference, and the scripts fall back to
quantizing the raw export), and onnxruntime's default MinMax calibration.
onnxruntime also offers Percentile and Entropy calibration and per-node
exclusion lists; none are applied, so this is the tool's standard static
invocation rather than a per-model tuned one. Preprocessing in each script
mirrors that model's evaluation transform, so the calibration data is not
disadvantaged relative to the published artifact.

The EdgeNeXt and XCiT scripts are byte-identical because both models evaluate
at a crop fraction of 1.0. TinyViT uses 0.95, and RT-DETRv2 uses detector
preprocessing with no mean/std normalization.

These results are specific to these architectures. Static post-training
quantization handles many convolutional networks without difficulty. These
four are architectures where it does not.
