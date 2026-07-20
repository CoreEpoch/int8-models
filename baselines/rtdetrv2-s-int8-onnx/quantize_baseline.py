"""The exact ONNX Runtime static-quantization baseline invocation used for the
comparison row in this repo's model card.

Usage: python quantize_baseline.py <fp32_model.onnx> <calib_dir> <out.onnx>
Deps:  pip install onnxruntime numpy pillow onnx

Configuration: QDQ format, per-channel weights, quant_pre_process, and
onnxruntime's default MinMax calibration. onnxruntime also offers Percentile
and Entropy calibration, reduce_range, and per-node exclusion lists; none of
those are applied here, so this is a standard static configuration rather than
an exhaustively tuned one.

Preprocessing matches this model's pipeline: square 640x640 bilinear resize,
/255, no mean/std normalization. onnxruntime version used for the published
row: 1.27.
"""

import glob
import os
import sys

import numpy as np
from PIL import Image

SIZE = 640


def preprocess(path):
    img = Image.open(path).convert("RGB").resize((SIZE, SIZE), Image.BILINEAR)
    x = (np.asarray(img, np.float32) / 255.0).transpose(2, 0, 1)[None]
    return x.astype(np.float32)


def main():
    fp32_path, calib_dir, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

    from onnxruntime.quantization import (
        CalibrationDataReader, QuantFormat, QuantType, quantize_static,
    )
    from onnxruntime.quantization.shape_inference import quant_pre_process

    class Reader(CalibrationDataReader):
        def __init__(self):
            self.files = sorted(glob.glob(os.path.join(calib_dir, "*.jpg")))[:128]
            self.i = 0

        def get_next(self):
            if self.i >= len(self.files):
                return None
            x = preprocess(self.files[self.i])
            self.i += 1
            return {"input": x}

    pre_path = out_path + ".preprocessed.tmp.onnx"
    try:
        quant_pre_process(fp32_path, pre_path)
        src = pre_path
    except Exception as e:
        # Same fallback as the pipeline that produced the published row: on
        # some exports (EdgeNeXt, XCiT) onnxruntime 1.27's symbolic shape
        # inference fails here, and the baseline quantizes the raw export.
        print(f"quant_pre_process failed ({type(e).__name__}) -> quantizing the raw export", flush=True)
        src = fp32_path
    try:
        quantize_static(
            src, out_path, Reader(),
            quant_format=QuantFormat.QDQ, per_channel=True,
            activation_type=QuantType.QUInt8, weight_type=QuantType.QInt8,
        )
    finally:
        if os.path.exists(pre_path):
            os.remove(pre_path)
    print(f"wrote {out_path} ({os.path.getsize(out_path):,} bytes)")


if __name__ == "__main__":
    main()
