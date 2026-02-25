import torch

from unlearning.unlearning_methods.GUIDE.guide import _resolve_guide_device


def test_resolve_guide_device_cpu_for_negative_cuda(monkeypatch):
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    monkeypatch.setattr(torch.cuda, "device_count", lambda: 2)

    device = _resolve_guide_device(-1)

    assert device.type == "cpu"


def test_resolve_guide_device_cpu_for_out_of_range_cuda(monkeypatch):
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    monkeypatch.setattr(torch.cuda, "device_count", lambda: 1)

    device = _resolve_guide_device(3)

    assert device.type == "cpu"


def test_resolve_guide_device_cuda_for_valid_index(monkeypatch):
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    monkeypatch.setattr(torch.cuda, "device_count", lambda: 2)

    device = _resolve_guide_device(1)

    assert device.type == "cuda"
    assert device.index == 1
