#pip install git+https://github.com/openai/glide-text2im
#pip uninstall googletrans
#pip install googletrans==4.0.0-rc1
from PIL import Image
from IPython.display import display
import torch as th
import os
import hashlib
import time
from glide_text2im.download import load_checkpoint
from glide_text2im.model_creation import (
    create_model_and_diffusion,
    model_and_diffusion_defaults,
    model_and_diffusion_defaults_upsampler
)
from googletrans import Translator as Tr

def save_images(batch: th.Tensor):
    new_path = "data"
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    """ Display a batch of images inline. """
    scaled = ((batch + 1)*127.5).round().clamp(0,255).to(th.uint8).cpu()
    batch = scaled.permute(0,2,3,1).numpy()
    hs1 = hashlib.sha256(str(time.time()).encode()).hexdigest()
    hs2 = hashlib.sha256(str(time.time()).encode()).hexdigest()
    spath1 = hs1+'.jpg'
    spath2 = hs2+'.jpg'
    spath1=str(os.path.join('data',spath1))
    spath2=str(os.path.join('data',spath2))
    Image.fromarray(batch[0]).save(spath1, quality=95)
    Image.fromarray(batch[1]).save(spath2, quality=95)
    return spath1,spath2


class text2im:
    def __init__(self):
        # Create base model.
        has_cuda = th.cuda.is_available()
        device = th.device('cpu' if not has_cuda else 'cuda')
        self.device=device
        options = model_and_diffusion_defaults()
        options['use_fp16'] = has_cuda
        options['timestep_respacing'] = '100' # use 100 diffusion steps for fast sampling
        self.options=options
        model, diffusion = create_model_and_diffusion(**options)
        model.eval()
        if has_cuda:
            model.convert_to_fp16()
        model.to(device)
        model.load_state_dict(load_checkpoint('base', device))
        print('total base parameters', sum(x.numel() for x in model.parameters()))
        self.model=model
        self.diffusion=diffusion
        # Create upsampler model.
        options_up = model_and_diffusion_defaults_upsampler()
        options_up['use_fp16'] = has_cuda
        options_up['timestep_respacing'] = 'fast27' # use 27 diffusion steps for very fast sampling
        self.options_up=options_up
        model_up, diffusion_up = create_model_and_diffusion(**options_up)
        model_up.eval()
        if has_cuda:
            model_up.convert_to_fp16()
        model_up.to(device)
        model_up.load_state_dict(load_checkpoint('upsample', device))
        print('total upsampler parameters', sum(x.numel() for x in model_up.parameters()))
        self.model_up=model_up
        self.diffusion_up=diffusion_up
        self.tr=Tr()

    def generate(self,prompt,batch_size=2):
        """
        prompt:１テキスト入力(日本語)

        出力:jpgファイルへのpath２つ
        """

        #翻訳処理
        prompt=self.tr.translate(text=prompt, src="ja", dest="en").text

        # Sampling parameters
        guidance_scale = 3.0
        # Tune this parameter to control the sharpness of 256x256 images.
        # A value of 1.0 is sharper, but sometimes results in grainy artifacts.
        upsample_temp = 0.997
        ##############################
        # Sample from the base model #
        ##############################
        model=self.model
        options=self.options
        device=self.device

        # Create the text tokens to feed to the model.
        tokens = model.tokenizer.encode(prompt)
        tokens, mask = model.tokenizer.padded_tokens_and_mask(
            tokens, options['text_ctx']
        )

        # Create the classifier-free guidance tokens (empty)
        full_batch_size = batch_size * 2
        uncond_tokens, uncond_mask = model.tokenizer.padded_tokens_and_mask(
            [], options['text_ctx']
        )

        # Pack the tokens together into model kwargs.
        model_kwargs = dict(
            tokens=th.tensor(
                [tokens] * batch_size + [uncond_tokens] * batch_size, device=device
            ),
            mask=th.tensor(
                [mask] * batch_size + [uncond_mask] * batch_size,
                dtype=th.bool,
                device=device,
            ),
        )
        # Create a classifier-free guidance sampling function
        def model_fn(x_t, ts, **kwargs):
            half = x_t[: len(x_t) // 2]
            combined = th.cat([half, half], dim=0)
            model_out = model(combined, ts, **kwargs)
            eps, rest = model_out[:, :3], model_out[:, 3:]
            cond_eps, uncond_eps = th.split(eps, len(eps) // 2, dim=0)
            half_eps = uncond_eps + guidance_scale * (cond_eps - uncond_eps)
            eps = th.cat([half_eps, half_eps], dim=0)
            return th.cat([eps, rest], dim=1)

        # Sample from the base model.
        diffusion=self.diffusion
        model.del_cache()
        samples = diffusion.p_sample_loop(
            model_fn,
            (full_batch_size, 3, options["image_size"], options["image_size"]),
            device=device,
            clip_denoised=True,
            progress=True,
            model_kwargs=model_kwargs,
            cond_fn=None,
        )[:batch_size]
        model.del_cache()

        ##############################
        # Upsample the 64x64 samples #
        ##############################
        model_up=self.model_up
        options_up=self.options_up

        tokens = model_up.tokenizer.encode(prompt)
        tokens, mask = model_up.tokenizer.padded_tokens_and_mask(
            tokens, options_up['text_ctx']
        )

        # Create the model conditioning dict.
        model_kwargs = dict(
            # Low-res image to upsample.
            low_res=((samples+1)*127.5).round()/127.5 - 1,

            # Text tokens
            tokens=th.tensor(
                [tokens] * batch_size, device=device
            ),
            mask=th.tensor(
                [mask] * batch_size,
                dtype=th.bool,
                device=device,
            ),
        )

        # Sample from the base model.
        diffusion_up=self.diffusion_up
        model_up.del_cache()
        up_shape = (batch_size, 3, options_up["image_size"], options_up["image_size"])
        up_samples = diffusion_up.ddim_sample_loop(
            model_up,
            up_shape,
            noise=th.randn(up_shape, device=device) * upsample_temp,
            device=device,
            clip_denoised=True,
            progress=True,
            model_kwargs=model_kwargs,
            cond_fn=None,
        )[:batch_size]
        model_up.del_cache()

        # Show the output
        return save_images(up_samples)