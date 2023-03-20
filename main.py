import gradio as gr
import webbrowser
import argparse
from parse import Parse
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=str, default='cpu')
    parser.add_argument('--api', action="store_true", default=False)
    parser.add_argument("--share", action="store_true", default=False, help="share gradio app")
    parser.add_argument("--colab", action="store_true", default=False, help="share gradio app")
    args = parser.parse_args()
    ps = Parse()
    with gr.Blocks() as app:
        gr.Markdown(
            "# <center> chat with Elysia\n"
            "### <center> base on chat gpt3.5 and vits\n"
        )
        with gr.Row():
            with gr.Column():
                textbox = gr.TextArea(label="对话内容",
                                        placeholder="Type your sentence here",
                                        value="你好?", elem_id=f"tts-input")
            with gr.Column():
                text_output = gr.Textbox(label="回复信息")
                audio_output = gr.Audio(label="音频信息", elem_id="tts-audio")
                btn = gr.Button("生成对话")
                btn.click(ps.PipeChat,
                            inputs=[textbox],
                            outputs=[text_output, audio_output])
    webbrowser.open("http://127.0.0.1:7860")
    app.launch(share=args.share)