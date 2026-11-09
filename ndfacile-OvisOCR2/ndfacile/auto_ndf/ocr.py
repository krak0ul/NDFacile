from PIL import ImageFile, Image
from openai import OpenAI

class Océaire():
    def __init__(self, model_name: str, vllm_url: str):
        """
        Setup class - model to use, vllm url
        """
        self.url = vllm_url
        self.model = model_name

        self.prompt = '\nExtract all readable content from the image in natural human reading order and output the result as a single Markdown document. For charts or images, represent them using an HTML image tag: <' + 'img src="images/bbox_{left}_{top}_{right}_{bottom}.jpg" />, where left, top, right, bottom are bounding box coordinates scaled to [0, 1000). Format formulas as LaTeX. Format tables as HTML: <table>...</table>. Transcribe all other text as standard Markdown. Preserve the original text without translation or paraphrasing.'
        # TODO
        # self.prompt = self.model.get_tokenizer().apply_chat_template(
        #     [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": prompt}]}],
        #     tokenize=False,
        #     add_generation_prompt=True,
        #     enable_thinking=False
        # )

        self.max_tokens=16384
        self.temperature=0.0
        self.thinking=False

        self.client = OpenAI(
            base_url=self.url,
            api_key="EMPTY",
            timeout=10000,
            max_retries=3
        )

    def _clean_truncated_repeats(
        self,
        text: str,
        min_text_len: int = 8000,
        max_period: int = 200,
        min_period: int = 1,
        min_repeat_chars: int = 100,
        min_repeat_times: int = 5
    ) -> str:
        """
        Credit: https://huggingface.co/ATH-MaaS/OvisOCR2
        """
        n = len(text)
        if n < min_text_len:
            return text

        max_period = min(max_period, n - 1)
        for unit_len in range(min_period, max_period + 1):
            if text[n - 1] != text[n - 1 - unit_len]:
                continue

            match_len = 1
            idx = n - 2
            while idx >= unit_len and text[idx] == text[idx - unit_len]:
                match_len += 1
                idx -= 1

            total_len = match_len + unit_len
            repeat_times = total_len // unit_len
            tail_len = total_len % unit_len

            if repeat_times >= min_repeat_times and total_len >= min_repeat_chars:
                return text[: n - total_len + unit_len] + text[n - tail_len:]

        return text

    def parse(self, base64_image: str, filter_imgtags: bool = True) -> str:
        """
        Calls vllm API to extract text from an image supplied as a b64 string.
        """
        messages = [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                {"type": "text", "text": self.prompt}
            ]
        }]

        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=messages,
            extra_body={"chat_template_kwargs": {"enable_thinking": self.thinking}}
        )
        
        # vllm_input = [
        #     {
        #         "prompt": self.prompt,
        #         "multi_modal_data": {"image": image},
        #         "mm_processor_kwargs": {
        #             "images_kwargs": {
        #                 "min_pixels": 448 * 448,
        #                 "max_pixels": 2880 * 2880
        #             }
        #         }
        #     }
        # ]

        text = response.choices[0].message.content.strip()

        # outputs = self.model.generate(vllm_input, self.sampling_params)

        # markdowns = []
        # for output in outputs:
        #     text = output.outputs[0].text.strip()
        if filter_imgtags:
            text = "\n\n".join(
                block
                for block in text.split("\n\n")
                if not block.strip().startswith('<img src="images/bbox_')
            )
            # markdowns.append(self._clean_truncated_repeats(text))

        # return markdowns[0]
        return self._clean_truncated_repeats(text)


if __name__ == "__main__":
    parser = Océaire("ovisocr2", "http://auto-ndf-vllm:8000/v1")
    images = [Image.open("test1.jpg"), Image.open("test2.jpg")]
    markdowns = parser.parse(images)
    print(markdowns[0])
