if old_expiry > now:
                start_date = old_expiry

        expiry = start_date + timedelta(days=plan["days"])

        con.execute(
            "UPDATE orders SET status='PAID' WHERE order_id=?",
            (order_id,)
        )

        con.execute("""
            INSERT INTO members VALUES(?,?,?)
            ON CONFLICT(user_id) DO UPDATE SET
            plan_code=excluded.plan_code,
            expires_at=excluded.expires_at
        """, (
            order["user_id"],
            order["plan_code"],
            expiry.isoformat()
        ))

    if CHANNEL_ID:
        invite = create_invite()
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": order["user_id"],
                "text": f"Payment verified!\nYour invite:\n{invite}"
            },
            timeout=20
        )

    return "Payment verified", 200

except Exception:
    logging.exception("Payment verification error")
    return "Verification error", 500
START BOT
def run_bot():
global bot_app
bot_app = Application.builder().token(BOT_TOKEN).build()

bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("admin", admin_command))
bot_app.add_handler(CommandHandler("plans", plans_command))
bot_app.add_handler(CommandHandler("addplan", addplan))
bot_app.add_handler(CommandHandler("disableplan", disableplan))
bot_app.add_handler(CommandHandler("stats", stats))
bot_app.add_handler(CallbackQueryHandler(buttons))

bot_app.run_polling(drop_pending_updates=True, stop_signals=None)
if name == "main":
import threading
setup_database()

threading.Thread(
    target=run_bot,
    daemon=True
).start()

import os
app.run(
    host="0.0.0.0",
    port=int(os.getenv("PORT", 10000))
)
