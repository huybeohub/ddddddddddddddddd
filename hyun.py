from flask import Flask, jsonify
import requests, time, random, os

app = Flask(__name__)

PLACE_ID = 2753915549

cache = []
last_scan = 0

headers = {
    "User-Agent": "Mozilla/5.0"
}

def scan_servers():
    global cache, last_scan

    cache = []
    cursor = None

    for _ in range(5):
        url = f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public?limit=100"
        if cursor:
            url += f"&cursor={cursor}"

        try:
            res = requests.get(url, headers=headers, timeout=10)
            data = res.json()
        except:
            break

        for s in data.get("data", []):
            cache.append({
                "id": s["id"],
                "players": s["playing"]
            })

        cursor = data.get("nextPageCursor")
        if not cursor:
            break

        time.sleep(1)

    last_scan = time.time()


def get_cache():
    global last_scan

    if time.time() - last_scan > 60 or not cache:
        scan_servers()

    return cache


@app.route("/")
def home():
    return "API OK"


@app.route("/hop")
def hop():
    servers = get_cache()

    if not servers:
        return jsonify({"success": False})

    pick = random.choice(servers[:20])

    return jsonify({
        "success": True,
        "jobId": pick["id"]
    })


# ✅ QUAN TRỌNG
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
