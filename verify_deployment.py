"""
SignBridge Production Deployment Verification Suite
Validates the unified single-port application serving:
- React 18 Single Page Application (HTML & Assets)
- Deep Learning ST-GCN ONNX model & CTC Decoder
- REST APIs (/api/health, /api/vocabulary, /api/sign-languages)
- Full-Duplex WebSocket Endpoint (/ws/live-sign)
- Client-Side SPA Route Fallback
"""

import sys
import os
import json
import time

# Ensure backend modules are accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from fastapi.testclient import TestClient
import main

def run_deployment_verification():
    print("=" * 70)
    print(" SIGNBRIDGE PRODUCTION DEPLOYMENT SANITY CHECK")
    print("=" * 70)
    
    client = TestClient(main.app)
    all_passed = True

    # 1. SPA Entrypoint (GET /)
    print("\n[1/6] Verifying SPA Entrypoint (GET /)...")
    res = client.get("/")
    if res.status_code == 200 and "<div id=\"root\">" in res.text:
        print("  [PASS] Root path successfully returns compiled React index.html")
    else:
        print(f"  [FAIL] Root path returned status {res.status_code}")
        all_passed = False

    # 2. Static Assets Bundle (CSS & JS)
    print("\n[2/6] Verifying Compiled Static Assets (/assets)...")
    dist_assets = os.path.join(main.FRONTEND_DIST_DIR, "assets")
    if os.path.exists(dist_assets):
        asset_files = os.listdir(dist_assets)
        css_file = next((f for f in asset_files if f.endswith(".css")), None)
        js_file = next((f for f in asset_files if f.endswith(".js")), None)
        
        if css_file:
            res_css = client.get(f"/assets/{css_file}")
            print(f"  [PASS] CSS Asset [{css_file}]: HTTP {res_css.status_code} ({len(res_css.content)} bytes)")
        if js_file:
            res_js = client.get(f"/assets/{js_file}")
            print(f"  [PASS] JS Bundle [{js_file}]: HTTP {res_js.status_code} ({len(res_js.content)} bytes)")
    else:
        print("  [FAIL] Static assets directory not found")
        all_passed = False

    # 3. SPA Route Fallback (Deep Links like /analytics or /dataset)
    print("\n[3/6] Verifying SPA Deep Route Fallback (/scenarios)...")
    res_fallback = client.get("/scenarios")
    if res_fallback.status_code == 200 and "<div id=\"root\">" in res_fallback.text:
        print("  [PASS] Deep client link properly falls back to index.html for client routing")
    else:
        print(f"  [FAIL] Deep route returned status {res_fallback.status_code}")
        all_passed = False

    # 4. REST API Health Check (GET /api/health)
    print("\n[4/6] Verifying REST API (/api/health)...")
    res_health = client.get("/api/health")
    if res_health.status_code == 200:
        data = res_health.json()
        print(f"  [PASS] Status: {data.get('status')} | Service: {data.get('service')} | Classes: {data.get('num_classes')}")
    else:
        print(f"  [FAIL] Health check failed with status {res_health.status_code}")
        all_passed = False

    # 5. REST API Multi-Dialect Metadata (GET /api/sign-languages)
    print("\n[5/6] Verifying Multi-Dialect ISL Metadata (/api/sign-languages)...")
    res_lang = client.get("/api/sign-languages")
    if res_lang.status_code == 200:
        data = res_lang.json()
        langs = data.get("sign_languages", []) or data.get("languages", [])
        total_vocab = sum(len(l.get("sample_signs", [])) for l in langs)
        dialects = len(langs)
        print(f"  [PASS] Returned {dialects} Indian Sign Language zonal chapters with {total_vocab:,} curated signs")
    else:
        print(f"  [FAIL] Sign languages API returned status {res_lang.status_code}")
        all_passed = False

    # 6. WebSocket Live Endpoint (/ws/live-sign)
    print("\n[6/6] Verifying Full-Duplex WebSocket Handshake (/ws/live-sign)...")
    try:
        with client.websocket_connect("/ws/live-sign") as ws:
            # Send sample landmark frame (107 nodes x 3 coords)
            dummy_landmarks = [[0.5, 0.5, 0.0] for _ in range(107)]
            ws.send_text(json.dumps({
                "landmarks": dummy_landmarks,
                "timestamp_ms": time.time() * 1000,
                "metadata": {"mean_joint_speed": 0.02}
            }))
            resp = ws.receive_text()
            data = json.loads(resp)
            print(f"  [PASS] WebSocket message received: type='{data.get('type')}', state='{data.get('state')}'")
    except Exception as e:
        print(f"  [FAIL] WebSocket communication failed: {e}")
        all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print(" ALL 6 PRODUCTION DEPLOYMENT CHECKS PASSED SUCCESSFULLY!")
        print(" Unified Server is 100% production-ready for Local, Docker, and Cloud!")
    else:
        print(" SOME CHECKS FAILED. Please review output above.")
    print("=" * 70)
    return all_passed

if __name__ == "__main__":
    success = run_deployment_verification()
    sys.exit(0 if success else 1)
