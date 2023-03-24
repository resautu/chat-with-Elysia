# coding=utf-8
from scipy.io.wavfile import write
import time
import os
import gradio as gr
import utils
import argparse
import commons
from models import SynthesizerTrn
from text import text_to_sequence
import torch
from torch import no_grad, LongTensor
import logging
logging.getLogger('numba').setLevel(logging.ERROR)
limitation = os.getenv("SYSTEM") == "spaces"  # limit text and audio length in huggingface spaces

def get_text(text, hps):
    text_norm, clean_text = text_to_sequence(text, hps.symbols, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm, clean_text

def vits(text, language, speaker_id, noise_scale, noise_scale_w, length_scale, device, hps_ms, net_g_ms):
    start = time.perf_counter()
    if not len(text):
        return "输入文本不能为空", None, None
    text = text.replace('\n', ' ').replace('\r', '').replace(" ", "")
    if len(text) > 100 and limitation:
        return f"输入文字过长！{len(text)}>100", None, None
    if language == 0:
        text = f"[ZH]{text}[ZH]"
    elif language == 1:
        text = f"[JA]{text}[JA]"
    else:
        text = f"{text}"
    stn_tst, clean_text = get_text(text, hps_ms)
    with no_grad():
        x_tst = stn_tst.unsqueeze(0).to(device)
        x_tst_lengths = LongTensor([stn_tst.size(0)]).to(device)
        speaker_id = LongTensor([speaker_id]).to(device)
        #audio = net_g_ms.infer(x_tst, x_tst_lengths, sid=speaker_id, noise_scale=noise_scale, noise_scale_w=noise_scale_w,
        #                    length_scale=length_scale)[0][0, 0].data.cpu().float().numpy()
        audio = net_g_ms.infer(x_tst, x_tst_lengths, sid=speaker_id, noise_scale=noise_scale, noise_scale_w=noise_scale_w,
                               length_scale=length_scale)[0][0, 0].data.float().detach().cpu().numpy()

    return audio

def generateSound(text, store_path):
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=str, default='cpu')
    parser.add_argument('--api', action="store_true", default=False)
    parser.add_argument("--share", action="store_true", default=False, help="share gradio app")
    parser.add_argument("--colab", action="store_true", default=False, help="share gradio app")
    args = parser.parse_args()
    #device = torch.device(args.device)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    hps_ms = utils.get_hparams_from_file(r'./model/config.json')
    net_g_ms = SynthesizerTrn(
        len(hps_ms.symbols),
        hps_ms.data.filter_length // 2 + 1,
        hps_ms.train.segment_size // hps_ms.data.hop_length,
        n_speakers=hps_ms.data.n_speakers,
        **hps_ms.model)
    _ = net_g_ms.eval().to(device)
    speakers = hps_ms.speakers
    model, optimizer, learning_rate, epochs = utils.load_checkpoint(r'./model/G_953000.pth', net_g_ms.to(device), None)
    ns = 0.6
    nsw = 0.668
    ls = 1.2
    result = vits(text, 0, 226, ns, nsw, ls, device, hps_ms, net_g_ms)
    #write('./demo.wav', hps_ms.data.sampling_rate, result)
    write(store_path, 22050, result)
    return result
#if __name__ == '__main__':
#    generateSound('你好，我是爱莉希雅，很高兴见到你', './demo2.wav')
