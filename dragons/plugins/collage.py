# collage plugin for catuserbot by @sandy1709
# Dragons - Userbot

# Copyright (C) 2020 Alfiananda P.A
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.import os

import os

from dragons import drgub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import _drgutils, reply_id
from . import make_gif

plugin_category = "utils"


@drgub.drg_cmd(
    pattern="collage(?:\s|$)([\s\S]*)",
    command=("collage", plugin_category),
    info={
        "header": "To create collage from still images extracted from video/gif.",
        "description": "Shows you the grid image of images extracted from video/gif. you can customize the Grid size by giving integer between 1 to 9 to cmd by default it is 3",
        "usage": "{tr}collage <1-9>",
    },
)
async def collage(event):
    "To create collage from still images extracted from video/gif."
    drginput = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    drgid = await reply_id(event)
    event = await edit_or_reply(
        event, "```collaging this may take several minutes too..... 😁```"
    )
    if not (reply and (reply.media)):
        await event.edit("`Media not found...`")
        return
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    drgsticker = await reply.download_media(file="./temp/")
    if not drgsticker.endswith((".mp4", ".mkv", ".tgs")):
        os.remove(drgsticker)
        await event.edit("`Media format is not supported...`")
        return
    if drginput:
        if not drginput.isdigit():
            os.remove(drgsticker)
            await event.edit("`You input is invalid, check help`")
            return
        drginput = int(drginput)
        if not 0 < drginput < 10:
            os.remove(drgsticker)
            await event.edit(
                "`Why too big grid you cant see images, use size of grid between 1 to 9`"
            )
            return
    else:
        drginput = 3
    if drgsticker.endswith(".tgs"):
        hmm = await make_gif(event, drgsticker)
        if hmm.endswith(("@tgstogifbot")):
            os.remove(drgsticker)
            return await event.edit(hmm)
        collagefile = hmm
    else:
        collagefile = drgsticker
    endfile = "./temp/collage.png"
    drgcmd = f"vcsi -g {drginput}x{drginput} '{collagefile}' -o {endfile}"
    stdout, stderr = (await _drgutils.runcmd(drgcmd))[:2]
    if not os.path.exists(endfile):
        for files in (drgsticker, collagefile):
            if files and os.path.exists(files):
                os.remove(files)
        return await edit_delete(
            event, f"`media is not supported or try with smaller grid size`", 5
        )
    await event.client.send_file(
        event.chat_id,
        endfile,
        reply_to=drgid,
    )
    await event.delete()
    for files in (drgsticker, collagefile, endfile):
        if files and os.path.exists(files):
            os.remove(files)
