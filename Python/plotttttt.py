import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

folder = Path(__file__).resolve().parent
file_path = folder / "Inverter.txt"

print("Python script location:", folder)
print("Looking for data at:", file_path)
print("File exists:", file_path.exists())

data = pd.read_csv(file_path, sep=r"\s+")

vin = data["Vin"]
vout = data["V(vout)"]

vm = None

for i in range(len(vout) - 1):
    if vout.iloc[i] >= 2.5 and vout.iloc[i + 1] < 2.5:
        vm = vin.iloc[i] + (
            (2.5 - vout.iloc[i])
            * (vin.iloc[i + 1] - vin.iloc[i])
            / (vout.iloc[i + 1] - vout.iloc[i])
        )
        break

plt.figure(figsize=(9, 6))

plt.plot(vin, vout, linewidth=2, label="VTC")

# Mark switching threshold
plt.axhline(2.5, linestyle="--", label="VDD/2 = 2.5 V")

if vm is not None:
    plt.axvline(vm, linestyle=":", label=f"VM = {vm:.4f} V")
    plt.scatter(vm, 2.5, zorder=3)


plt.title("Voltage Transfer Characteristic of CMOS Inverter")
plt.xlabel("Input Voltage VIN (V)")
plt.ylabel("Output Voltage VOUT (V)")

plt.xlim(0, 5)
plt.ylim(0, 5.2)
plt.grid(True)
plt.legend()


plt.tight_layout()
plt.savefig("CMOS_Inverter_VTC.png", dpi=300)

plt.show()

print(f"Switching threshold VM = {vm:.6f} V")
