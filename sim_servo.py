class SimServo:
    def __init__(self, axis_id=1):
        self.axis_id = axis_id
        self.position_counts = 0
        self.enabled = False
        self.fault = False
        self.status = "disabled"

    def enable(self):
        if self.fault:
            raise RuntimeError("Cannot enable servo while faulted.")
        self.enabled = True
        self.status = "enabled"
        print(f"Axis {self.axis_id} enabled")

    def disable(self):
        self.enabled = False
        self.status = "disabled"
        print(f"Axis {self.axis_id} disabled")

    def reset_fault(self):
        self.fault = False
        self.status = "disabled"
        print(f"Axis {self.axis_id} fault reset")

    def move_profile(self, profile):
        if not self.enabled:
            raise RuntimeError("Servo must be enabled before motion.")

        self.status = "moving"
        print("Moving...")

        print_step = max(1, len(profile) // 10)

        for index, point in enumerate(profile):
            self.position_counts = point.position_counts

            if index % print_step == 0 or index == len(profile) - 1:
                print(
                    f"t={point.time_s:>5.2f}s | "
                    f"position={point.position_counts:>6} counts | "
                    f"velocity={point.velocity_counts_s:>7.1f} counts/s"
                )

        self.status = "target reached"
        print("Target reached")
