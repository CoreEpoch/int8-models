"""The exact ONNX Runtime static-quantization baseline invocation used for the
comparison row in this repo's model card.

Usage: python quantize_baseline.py <fp32_model.onnx> <calib_dir> <out.onnx>
Deps:  pip install onnxruntime numpy pillow onnx

Configuration: QDQ format, per-channel weights, quant_pre_process, and
onnxruntime's default MinMax calibration. onnxruntime also offers Percentile
and Entropy calibration, reduce_range, and per-node exclusion lists; none of
those are applied here, so this is a standard static configuration rather than
an exhaustively tuned one.

Preprocessing mirrors the eval transform stated on the card: bicubic resize of
the shorter side to size/CROP_PCT, center crop to the model's input size,
/255, ImageNet mean/std. onnxruntime version used for the published row: 1.27.
"""

import glob
import os
import sys

import numpy as np
from PIL import Image

CROP_PCT = 0.95  # this model's eval crop fraction (see the model card)
MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)


def preprocess(path, size):
    img = Image.open(path).convert("RGB")
    scale_size = int(round(size / CROP_PCT))
    w, h = img.size
    if w < h:
        nw, nh = scale_size, int(round(h * scale_size / w))
    else:
        nw, nh = int(round(w * scale_size / h)), scale_size
    img = img.resize((nw, nh), Image.BICUBIC)
    left, top = (nw - size) // 2, (nh - size) // 2
    img = img.crop((left, top, left + size, top + size))
    x = ((np.asarray(img, np.float32) / 255.0 - MEAN) / STD).transpose(2, 0, 1)[None]
    return x.astype(np.float32)


def main():
    fp32_path, calib_dir, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

    import onnxruntime as ort
    from onnxruntime.quantization import (
        CalibrationDataReader, QuantFormat, QuantType, quantize_static,
    )
    from onnxruntime.quantization.shape_inference import quant_pre_process

    sess = ort.InferenceSession(fp32_path, providers=["CPUExecutionProvider"])
    size = sess.get_inputs()[0].shape[-1]
    del sess

    class Reader(CalibrationDataReader):
        def __init__(self):
            self.files = sorted(glob.glob(os.path.join(calib_dir, "*.jpg")))
            self.i = 0

        def get_next(self):
            if self.i >= len(self.files):
                return None
            x = preprocess(self.files[self.i], size)
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
