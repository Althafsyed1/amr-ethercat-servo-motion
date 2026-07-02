from dataclasses import dataclass
from math import sqrt


@dataclass
class MotionPoint:
    time_s: float
    position_counts: int
    velocity_counts_s: float


def plan_trapezoid(start_pos, target_pos, max_velocity, max_acceleration, dt=0.1):
    if max_velocity <= 0 or max_acceleration <= 0:
        raise ValueError("Velocity and acceleration must be positive.")

    if start_pos == target_pos:
        return [MotionPoint(0.0, int(start_pos), 0.0)]

    direction = 1 if target_pos > start_pos else -1
    distance = abs(target_pos - start_pos)

    t_accel = max_velocity / max_acceleration
    d_accel = 0.5 * max_acceleration * t_accel**2

    if 2 * d_accel > distance:
        t_accel = sqrt(distance / max_acceleration)
        t_flat = 0.0
        peak_velocity = max_acceleration * t_accel
        d_accel = 0.5 * max_acceleration * t_accel**2
    else:
        d_flat = distance - 2 * d_accel
        t_flat = d_flat / max_velocity
        peak_velocity = max_velocity

    total_time = 2 * t_accel + t_flat
    points = []
    t = 0.0

    while t <= total_time:
        if t < t_accel:
            moved = 0.5 * max_acceleration * t**2
            velocity = max_acceleration * t
        elif t < t_accel + t_flat:
            moved = d_accel + peak_velocity * (t - t_accel)
            velocity = peak_velocity
        else:
            t_dec = t - t_accel - t_flat
            moved = d_accel + peak_velocity * t_flat + peak_velocity * t_dec - 0.5 * max_acceleration * t_dec**2
            velocity = peak_velocity - max_acceleration * t_dec

        position = start_pos + direction * moved
        points.append(MotionPoint(round(t, 3), int(round(position)), direction * velocity))
        t += dt

    points.append(MotionPoint(round(total_time, 3), int(target_pos), 0.0))
    return points
