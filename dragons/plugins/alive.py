import random
import re
import time
from platform import python_version
from telethon import version
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery
from dragons import StartTime, drgub, drgversion

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import drgalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import mention

plugin_category = "utils"


@drgub.drg_cmd(
    pattern="alive$",
    command=("alive", plugin_category),
    info={
        "header": "To check bot's alive status",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details"
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  ✥ "
    CUSTOM_ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "✮ MY BOT IS RUNNING SUCCESSFULLY ✮"
    DRG_IMG = gvarstatus("ALIVE_PIC")
    if DRG_IMG:
        DRAGONS = [x for x in DRG_IMG.split()]
        A_IMG = list(DRAGONS)
        PIC = random.choice(A_IMG)
        drg_caption = f"**{CUSTOM_ALIVE_TEXT}**\n\n"
        drg_caption += f"**{EMOJI} Database :** `{check_sgnirts}`\n"
        drg_caption += f"**{EMOJI} Telethon version :** `{version.__version__}\n`"
        drg_caption += f"**{EMOJI} Dragons-userbot Version :** `{drgversion}`\n"
        drg_caption += f"**{EMOJI} Python Version :** `{python_version()}\n`"
        drg_caption += f"**{EMOJI} Uptime :** `{uptime}\n`"
        drg_caption += f"**{EMOJI} Master:** {mention}\n"
        try:
            await event.client.send_file(event.chat_id, PIC, caption=drg_caption, reply_to=reply_to_id)
            await event.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(
                event,
                f"**Media Value Error!!**\n__Change the link by __`.setdv`\n\n**__Can't get media from this link :-**__ `{PIC}`",
            )
    else:
        await edit_or_reply(
            event,
            f"**{CUSTOM_ALIVE_TEXT}**\n\n"
            f"**{EMOJI} Database :** `{check_sgnirts}`\n"
            f"**{EMOJI} Telethon Version :** `{version.__version__}\n`"
            f"**{EMOJI} Dragons-userbot Version :** `{drgversion}`\n"
            f"**{EMOJI} Python Version :** `{python_version()}\n`"
            f"**{EMOJI} Uptime :** `{uptime}\n`"
            f"**{EMOJI} Master:** {mention}\n",
        )


@drgub.drg_cmd(
    pattern="ialive$",
    command=("ialive", plugin_category),
    info={
        "header": "To check bot's alive status via inline mode",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details by your inline bot"
    reply_to_id = await reply_id(event)
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  ✥ "
    drg_caption = f"**Dragons-userbot is Up and Running**\n"
    drg_caption += f"**{EMOJI} Telethon version :** `{version.__version__}\n`"
    drg_caption += f"**{EMOJI} Dragons-userbot Version :** `{drgversion}`\n"
    drg_caption += f"**{EMOJI} Python Version :** `{python_version()}\n`"
    drg_caption += f"**{EMOJI} Master:** {mention}\n"
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, drg_caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@drgub.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await drgalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
