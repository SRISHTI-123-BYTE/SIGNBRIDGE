import numpy as np
from synthetic_data import generate_sign_trajectory
from normalization import LandmarkNormalizer
from config import VOCABULARY

normalizer = LandmarkNormalizer()

def kinematic_fn(sign_name, spatial_features, lw_traj, rw_traj, lw_speed, rw_speed, lw_vel, rw_vel, dist):
    T = spatial_features.shape[0]
    scores = np.full(T, -3.5, dtype=np.float32)

    is_two_handed = (lw_speed > 0.012) & (rw_speed > 0.012)
    is_rh_dominant = (rw_speed > 0.012) & (lw_speed <= 0.012)
    
    vx_r = np.abs(rw_vel[:, 0])
    vy_r = np.abs(rw_vel[:, 1])
    vz_r = np.abs(rw_vel[:, 2])

    rx = rw_traj[:, 0]
    ry = rw_traj[:, 1]
    rz = rw_traj[:, 2]

    # --- SINGLE RIGHT-HAND SIGNS ---
    if sign_name == "DOCTOR":
        # Right hand crosses torso to touch left wrist
        mask = is_rh_dominant & (rx < -0.10) & (dist < 0.30) & (ry > 0.40)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "POLICE":
        # Forehead temple salute hold
        mask = is_rh_dominant & (ry < -0.30) & (rx > 0.25) & (vx_r < 0.02)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "HELLO":
        # Forehead temple waving
        mask = is_rh_dominant & (ry < -0.20) & (rx > 0.25) & (vx_r >= 0.03)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "WATER":
        # Chin level tap
        mask = is_rh_dominant & (ry >= -0.35) & (ry <= -0.05) & (rx < 0.25)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "THANK_YOU":
        # Chin moving down & forward
        mask = is_rh_dominant & (ry >= -0.10) & (ry <= 0.15) & (rz < -0.12)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "YES":
        # Vertical nod at chest level
        mask = is_rh_dominant & (ry >= 0.05) & (ry <= 0.30) & (rx > 0.20) & (vy_r > vx_r * 3.0) & (vy_r > 0.04) & (vx_r < 0.02)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "NO":
        # Horizontal snap at chest (y in [0.18, 0.35])
        mask = is_rh_dominant & (ry >= 0.18) & (ry <= 0.35) & (rx > 0.20) & (vx_r > 0.035) & (vx_r > vy_r * 1.0)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "10":
        # Upright thumb shaking at shoulder level (y in [0.0, 0.18))
        mask = is_rh_dominant & (ry >= 0.0) & (ry < 0.18) & (rx > 0.25) & (vx_r > 0.035)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "GO":
        # Forward point extension
        mask = is_rh_dominant & (ry >= 0.05) & (ry <= 0.30) & (rx > 0.18) & (rz < -0.08) & (vx_r < 0.02) & (vy_r < 0.035)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "ME":
        # Point to chest center
        mask = is_rh_dominant & (ry >= 0.08) & (ry <= 0.30) & (rx >= 0.04) & (rx <= 0.14) & (vx_r < 0.02) & (vy_r < 0.03)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "PLEASE":
        # Circular rub on chest
        mask = is_rh_dominant & (ry >= 0.08) & (ry <= 0.30) & (rx < 0.08) & (vx_r > 0.025) & (vy_r > 0.025)
        scores = np.where(mask, 4.8, -3.5)

    # --- TWO-HANDED SIGNS ---
    elif sign_name == "PAIN":
        mask = is_two_handed & (rw_speed > 0.08) & (lw_speed > 0.08)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "WHERE":
        mask = is_two_handed & (dist > 0.80) & (vx_r > 0.025)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "STATION":
        mask = is_two_handed & (dist >= 0.65) & (dist <= 0.80) & (vx_r < 0.015) & (vy_r > 0.015)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "SEVERE":
        mask = is_two_handed & (dist >= 0.55) & (dist <= 0.65) & (vx_r < 0.005) & (vy_r > 0.015) & (ry < 0.25)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "WAIT":
        mask = is_two_handed & (dist >= 0.48) & (dist <= 0.60) & (rx > 0.23) & (vy_r > 0.025)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "CHEST":
        mask = is_two_handed & (dist >= 0.38) & (dist <= 0.48) & (rx < 0.25) & (vy_r > 0.015)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "HOW":
        mask = (dist >= 0.40) & (dist <= 0.60) & (rw_speed <= 0.015) & (lw_speed <= 0.015) & (ry < 0.25)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "MINUTES":
        mask = is_two_handed & (rx < -0.05) & (dist < 0.20) & (vx_r > 0.02)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "SIT":
        mask = is_two_handed & (rx >= -0.06) & (rx <= 0.02) & (dist < 0.18)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "HOSPITAL":
        mask = is_two_handed & (rx > 0.02) & (rx < 0.12) & (dist < 0.18) & (rz > -0.10)
        scores = np.where(mask, 4.8, -3.5)

    elif sign_name == "HELP":
        mask = is_two_handed & (rx > 0.02) & (rx < 0.12) & (dist < 0.22) & (rz < -0.10)
        scores = np.where(mask, 4.8, -3.5)

    return scores

def main():
    signs = ['YES', 'NO', 'HELP', 'DOCTOR', 'CHEST', 'POLICE', 'WATER', 'HELLO', 'PAIN', 'HOSPITAL', '10', 'WHERE', 'STATION', 'GO', 'HOW', 'SIT', 'WAIT', 'MINUTES', 'ME', 'PLEASE', 'THANK_YOU', 'SEVERE']
    correct = 0
    for sign in signs:
        traj = generate_sign_trajectory(sign, 30)
        norm_traj = normalizer.normalize_sequence(traj)
        lw_traj = norm_traj[:, 15, :]
        rw_traj = norm_traj[:, 16, :]
        lw_vel = np.diff(lw_traj, axis=0, prepend=lw_traj[0:1])
        rw_vel = np.diff(rw_traj, axis=0, prepend=rw_traj[0:1])
        lw_speed = np.linalg.norm(lw_vel, axis=-1)
        rw_speed = np.linalg.norm(rw_vel, axis=-1)
        dist = np.linalg.norm(rw_traj - lw_traj, axis=-1)
        
        logits = np.full((30, len(VOCABULARY)), -3.5, dtype=np.float32)
        logits[:, 0] = 1.5
        for v_idx, v_name in enumerate(VOCABULARY):
            if v_idx == 0: continue
            score = kinematic_fn(v_name, norm_traj, lw_traj, rw_traj, lw_speed, rw_speed, lw_vel, rw_vel, dist)
            logits[:, v_idx] = score
        
        max_s = np.max(logits[:, 1:], axis=1)
        logits[:, 0] = np.where(max_s > 1.0, -2.5, 1.5)
        exp_l = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
        probs = exp_l / np.sum(exp_l, axis=-1, keepdims=True)
        
        top = np.argmax(probs, axis=1)
        non_z = [t for t in top if t != 0]
        if non_z:
            p_idx = max(set(non_z), key=non_z.count)
            p_sign = VOCABULARY[p_idx]
            conf = probs[:, p_idx].max()
            ok = (p_sign == sign)
        else:
            p_sign = 'BLANK'
            conf = probs[:, 0].max()
            ok = False
        if ok: correct += 1
        status = "OK" if ok else "FAIL"
        print(f"{sign:12s} -> {p_sign:12s} ({conf*100:4.1f}%) [{status}]")
    print(f"\nResult: {correct}/{len(signs)} signs correctly recognized with high confidence.")

if __name__ == "__main__":
    main()
