from motion_planner import plan_trapezoid
from sim_servo import SimServo


def main():
    axis = SimServo(axis_id=1)

    start_position = 0
    target_position = 10000
    velocity_limit = 2000
    acceleration_limit = 500

    axis.enable()

    print(f"Planning move: {start_position} -> {target_position} counts")

    profile = plan_trapezoid(
        start_pos=start_position,
        target_pos=target_position,
        max_velocity=velocity_limit,
        max_acceleration=acceleration_limit,
        dt=0.1,
    )

    axis.move_profile(profile)


if __name__ == "__main__":
    main()
