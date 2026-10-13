# 🎛 Player UI helpers: Thumbnail ON/OFF sender + live button label refresh
from SHIVMUSIC.utils.database import is_thumb_on, autoplay_label, thumb_label


async def send_player(client, chat_id=None, photo=None, caption=None, reply_markup=None, **kwargs):
    """Thumbnail ON -> photo card, OFF -> sirf text + buttons."""
    if await is_thumb_on(chat_id):
        try:
            return await client.send_photo(chat_id=chat_id, photo=photo, caption=caption, reply_markup=reply_markup, **kwargs)
        except Exception:
            pass  # photo fail -> text fallback
    return await client.send_message(
        chat_id=chat_id, text=caption or "\u200b", reply_markup=reply_markup, disable_web_page_preview=True
    )


async def refresh_player_buttons(CallbackQuery, chat_id):
    """Message ke existing keyboard me Autoplay / Thumbnail labels update karo."""
    try:
        markup = CallbackQuery.message.reply_markup
        if not markup or not getattr(markup, "inline_keyboard", None):
            return
        changed = False
        for row in markup.inline_keyboard:
            for btn in row:
                cb = getattr(btn, "callback_data", None) or ""
                if isinstance(cb, bytes):
                    cb = cb.decode(errors="ignore")
                if cb.startswith("ADMIN Autoplay|"):
                    btn.text = autoplay_label(chat_id); changed = True
                elif cb.startswith("ADMIN Thumbnail|"):
                    btn.text = thumb_label(chat_id); changed = True
        if changed:
            await CallbackQuery.edit_message_reply_markup(reply_markup=markup)
    except Exception:
        pass
