#  This file is part of the VIDEOconvertor distribution.
#  Copyright (c) 2021 vasusen-code ; All rights reserved. 
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#
#  License can be found in < https://github.com/vasusen-code/VIDEOconvertor/blob/public/LICENSE> .

from telethon import events, Button
from ethon.teleutils import mention
from ethon.mystarts import vc_menu

from .. import Drone, ACCESS_CHANNEL, AUTH_USERS

from main.plugins.actions import set_thumbnail, rem_thumbnail, heroku_restart
from LOCAL.localisation import START_TEXT as st
from LOCAL.localisation import info_text, spam_notice, help_text, DEV, source_text, SUPPORT_LINK



@Drone.on(events.NewMessage(incoming=True, pattern="/start"))
async def start(event):
    await event.reply(f'{st}', 
                      buttons=[
                              [Button.inline("ᴍᴇɴᴜ.", data="menu")]
                              ])
    tag = f'[{event.sender.first_name}](tg://user?id={event.sender_id})'
    await Drone.send_message(int(ACCESS_CHANNEL), f'{tag} started the BOT')
    
CT_NOOB = "ᴠɪᴅᴇᴏ ᴄᴏɴᴠᴇʀᴛᴇʀ ʙᴏᴛ\n\nᴍᴀᴅᴇ ʙʏ @TamilBots"

@Drone.on(events.callbackquery.CallbackQuery(data="menu"))
async def menu(event):
    await event.edit(CT_NOOB,
                          buttons = [[
                   Button.inline("ɪɴғᴏ", data="info"),
                   Button.inline("ɴᴏᴛɪᴄᴇ", data="notice")],
                   [
                      Button.inline("sᴜᴘᴘᴏʀᴛ", data="source"),
                      Button.inline("ʜᴇʟᴘ", data="help")],
                   [
                    Button.inline("ʙᴀᴄᴋ", data="plugins")]])
    
@Drone.on(events.callbackquery.CallbackQuery(data="info"))
async def info(event):
    await event.edit(f'**ɪɴғᴏ:**\n\n{info_text}',
                    buttons=[[
                         Button.inline("ᴍᴇɴᴜ", data="menu")]])
    
@Drone.on(events.callbackquery.CallbackQuery(data="notice"))
async def notice(event):
    await event.answer(f'{spam_notice}', alert=True)
    
@Drone.on(events.callbackquery.CallbackQuery(data="source"))
async def source(event):
    await event.edit(source_text,
                    buttons=[[
                         Button.url("sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url="https://t.me/tamilsupport"),
                         Button.url("ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ", url="https://t.me/tamilbots")],
                         [Button.inline("ʙᴀᴄᴋ", data="menu")]])
                    
@Drone.on(events.callbackquery.CallbackQuery(data="help"))
async def help(event):
    await event.edit('**👥HELP & SETTINGS**',
                    buttons=[[
                         Button.inline("SET THUMB", data="sett"),
                         Button.inline("REM THUMB", data='remt')],
                         [
                         Button.inline("PLUGINS", data="plugins"),
                         Button.inline("RESTART", data="restart")],
                         [Button.url("SUPPORT", url="https://t.me/tamilsupport")],
                         [
                         Button.inline("BACK", data="menu")]])
    
@Drone.on(events.callbackquery.CallbackQuery(data="plugins"))
async def plugins(event):
    await event.edit(f'{help_text}',
                    buttons=[[Button.inline("Menu.", data="menu")]])
                   
 #-----------------------------------------------------------------------------------------------                            
    
@Drone.on(events.callbackquery.CallbackQuery(data="sett"))
async def sett(event):    
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    async with Drone.conversation(event.chat_id) as conv: 
        xx = await conv.send_message("Send me any image for thumbnail as a `reply` to this message.")
        x = await conv.get_reply()
        if not x.media:
            xx.edit("No media found.")
        mime = x.file.mime_type
        if not 'png' in mime:
            if not 'jpg' in mime:
                if not 'jpeg' in mime:
                    return await xx.edit("No image found.")
        await set_thumbnail(event, x.media)
        await xx.delete()
        
@Drone.on(events.callbackquery.CallbackQuery(data="remt"))
async def remt(event):  
    await event.delete()
    await rem_thumbnail(event)
    
@Drone.on(events.callbackquery.CallbackQuery(data="restart"))
async def res(event):
    if not f'{event.sender_id}' == f'{int(AUTH_USERS)}':
        return await event.edit("Only authorized user can restart!")
    result = await heroku_restart()
    if result is None:
        await event.edit("You have not filled `HEROKU_API` and `HEROKU_APP_NAME` vars.")
    elif result is False:
        await event.edit("An error occured!")
    elif result is True:
        await event.edit("Restarting app, wait for a minute.")
