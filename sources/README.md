# Sources

This folder stores local copies of source documents used to ground Foundry Stack entries.

## Semiconductor Supply Chain Report - Final[1].pdf

**Full title:** U.S. Department of Energy, *Semiconductor Supply Chain Deep Dive Assessment*, response to Executive Order 14017, February 24, 2022.

**Scope:** Energy-sector semiconductor supply chains. This report is useful, but it is not a general-purpose foundry-business primer. It focuses heavily on:

- conventional semiconductors needed by the energy sector,
- wide bandgap (WBG) power electronics,
- silicon carbide (SiC),
- gallium nitride (GaN),
- EVs, charging, renewables, industrial power, grid stabilization, and HVDC,
- WBG supply-chain steps such as raw materials, SiC/GaN substrates, epi-wafers, device fabrication, and power-module packaging.

**Best for Foundry Stack topics:**

- `market-structure/foundry.md` only as broad supply-chain context, not detailed foundry economics.
- `market-structure/fabless-company.md`, `market-structure/idm.md` for basic design/fabrication/OSAT structure.
- `fab-system/wafer.md`, `fab-system/tool.md`, `fab-system/toolset.md` for general supply-chain context.
- `process-stack/mature-node.md` and power-device context, but not leading-edge logic node economics.
- `process-stack/yield.md` only indirectly.
- `operating-model/capacity-expansion.md`, `operating-model/bottleneck-tool.md` for WBG bottleneck examples.
- Any future WBG-specific entries, e.g. `wide-bandgap-semiconductor`, `silicon-carbide`, `gallium-nitride`, `power-module-packaging`, `epi-wafer`, `substrate`.

**Not best for:**

- TSMC-style foundry revenue, application mix, node mix, utilization, wafer ASP, capex, gross margin, or fab P&L.
- EUV/DUV leading-edge logic bottlenecks.
- Customer allocation for AI accelerators.

For those, prefer foundry filings, ASML/AMAT/Lam/KLA disclosures, SEMI/SIA/IRDS, and company earnings materials.

## Useful excerpts

- The report states that it focuses on “semiconductors, both conventional and wide bandgap (WBG) power electronics.”
- It says semiconductors are essential for “every electric vehicle, recharging station, and wind turbine as well as the entire electrical grid.”
- It defines WBG examples as “SiC and gallium nitride (GaN)” for power-flow control/conversion in EVs, industrial technologies, wind, and solar.
- It notes WBG power devices were about 0.1% of the total semiconductor market in 2020 but expected to grow with decarbonization.
- It distinguishes GaN and SiC applications: GaN is more consumer-electronics/low-voltage oriented, while SiC has stronger automotive, energy, and industrial applications.
- It identifies WBG supply-chain issues around SiC substrates, thick SiC epi-wafers, GaN-on-silicon wafers, bulk GaN substrates, and DBC insulator substrates for high-voltage modules.
